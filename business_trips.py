import pandas as pd
from os import path
from datetime import datetime as dt


def get_teachers_working_types(teachers):
    keys = teachers['Преподаватель'].values.tolist()
    keys = list(map(lambda lst: lst.split()[0], keys))
    vals = teachers['График сменности'].values.tolist()
    return dict(zip(keys, vals))


def extract_courses(value):
    if isinstance(value, int):
        return [value]
    else:
        return list(map(lambda x: int(x), value.split(';')))


def get_courses_teachers(teachers):
    keys = teachers['Преподаватель'].values.tolist()
    keys = list(map(lambda lst: lst.split()[0], keys))
    vals = teachers['Учебные программы'].values.tolist()
    vals = list(map(extract_courses, vals))
    teachers_courses = dict(zip(keys, vals))

    courses_teachers = dict.fromkeys([i for i in range(1, 41)], set())
    for teacher in teachers_courses:
        for course in teachers_courses[teacher]:
            courses_teachers[course].add(teacher)

    return courses_teachers


def is_working_day(line):
    for column in range(0, len(line), 2):
        if not pd.isna(line[column]):
            return True
    return False


def is_teacher_work(line, teacher):
    for column in range(0, len(line), 2):
        if isinstance(line[column], str) and line[column].startswith(teacher):
            return True
    return False


def normalize_date_from_schedule(date):
    months = {
        'января': '01',
        'февраля': '02',
        'марта': '03',
        'апреля': '04',
        'мая': '05',
        'июня': '06',
        'июля': '07',
        'августа': '08',
        'сентября': '09',
        'октября': '10',
        'ноября': '11',
        'декабря': '12',
    }

    date = date.split('\n')[0]
    old_format_month = date.split()[1]
    date = date.replace(old_format_month, months[old_format_month])

    return int(dt.strptime(date, '%d %m').strftime('%j'))


def normalize_date(day, month):
    return int(dt.strptime(f'{day} {month}', '%d %m').strftime('%j'))


def compute_trips_possibilities(teacher, working_type):
    if teacher == 'Некрасова':
        return set()

    schedule_file = path.join('input_data', 'Расписание на неделю 2020.xlsx')
    pages = [page for page in pd.ExcelFile(schedule_file).sheet_names if page.find(' НА') > 0]
    dates_at_work, work_days = set(), set()
    for page in pages:
        schedule = pd.read_excel(schedule_file, sheet_name=page, header=None)
        days = schedule[0].dropna()
        for day_index in days.index[2:]:
            line = schedule.iloc[day_index]
            if is_teacher_work(line, teacher):
                dates_at_work.add(normalize_date_from_schedule(schedule[0][day_index]))
                work_days.add(normalize_date_from_schedule(schedule[0][day_index]))
            elif is_working_day(line):
                work_days.add(normalize_date_from_schedule(schedule[0][day_index]))

    base = work_days if working_type == 'нет' else set(range(1, 367))
    base -= dates_at_work

    vacations_file = path.join('input_data', 'Приложение №5.xls')
    vacations = pd.read_excel(vacations_file, sheet_name='План', header=None)
    people = vacations[1].dropna()
    days_in_month = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    vacations_dates = set()
    for person_id in people.index:
        if people[person_id].startswith(teacher):
            line = vacations.iloc[person_id]
            for month in range(12):
                if not pd.isna(line[3 + 2 * month]):
                    length, decade = int(line[3 + 2 * month]), int(line[4 + 2 * month])
                    chill = {1 + i + (decade - 1) * 10 for i in range(length)}
                    for day in chill:
                        if day <= days_in_month[month]:
                            vacations_dates.add(normalize_date(day, month + 1))
                        else:
                            vacations_dates.add(normalize_date(day - days_in_month[month], month + 1))
            break

    return base - vacations_dates


def delete_time_in_travel(time):
    for person in time:
        count_in_row = 0
        prev_day = -1
        timeline = list(time[person])
        for i, day in enumerate(timeline):
            if day + 1 == prev_day:
                count_in_row += 1
            elif i != 0:
                timeline[i - 1] = -1
                timeline[i - count_in_row - 1] = -1
        time[person] = {i for i in timeline if i > 0}


def find_trips(priorities, frequency):
    data_file = path.join('input_data', 'Приложение №2.xlsx')
    education_programs_data = pd.read_excel(data_file, sheet_name='параметры программ', index_col=0)
    teachers_data = pd.read_excel(data_file, sheet_name='параметры преподавателей')
    courses_teachers = get_courses_teachers(teachers_data)
    teachers_types = get_teachers_working_types(teachers_data)

    if path.isfile(path.join('input_data', 'trips_possibilities.csv')):
        data = pd.read_csv(path.join('input_data', 'trips_possibilities.csv'))
        keys = data['Преподаватель'].values.tolist()
        vals = list(map(extract_courses, data['Дни'].values.tolist()))
        teachers_free_days = dict(zip(keys, vals))
    else:
        teachers_free_days = {
            teacher: compute_trips_possibilities(teacher, teachers_types[teacher]) for teacher in courses_teachers
        }
        data = pd.DataFrame({'Преподаватель': teachers_free_days.keys(), 'Дни': teachers_free_days.values()})
        data.to_csv(path.join('input_data', 'trips_possibilities.csv'))
    delete_time_in_travel(teachers_free_days)

    trips_data = pd.DataFrame(columns=['Учебная программа', 'Преподаватели', 'Начало поездки', 'Конец поездки'])
    for education_program in priorities:
        time_length = education_programs_data['Количество дней очно'][education_program]
        teachers = courses_teachers[education_program]
        timelines = {teacher: teachers_free_days[teacher] for teacher in teachers}
        scan_line(trips_data, timelines, time_length, education_program)
    trips_data.to_excel(path.join('output_data', 'trips.xlsx'), sheet_name='Командировки')


def scan_line(trips_data, segments, length, education_program):
    history = {line: History() for line in segments}
    for pointer in range(1, 366):
        for line in segments:
            if pointer in segments[line]:
                history[line].days += 1
                if history[line].empty() or history[line].lines[-1] != line:
                    history[line].lines.append(line)
                    history[line].starts.append(pointer)
                if history[line].days >= length:
                    history[line].ends.append(pointer)
                    history[line].save(trips_data, education_program)
            else:
                history[line].ends.append(pointer - 1)
        for line in segments:
            if history[line].is_ended_at(pointer - 1):
                continued = False
                for son_line in segments:
                    if not history[son_line].is_ended_at(pointer - 1) and not history[son_line].empty():
                        if history[son_line].days < history[line].days + 1:
                            history[line].move(history[son_line])
                            if history[son_line].days >= length:
                                history[son_line].save(trips_data, education_program)
                            continued = True
                            break
                if not continued:
                    history[line].clear()


class History:
    def __init__(self):
        self.clear()

    def empty(self):
        return False if self.lines else True

    def is_ended_at(self, pointer):
        if self.starts and self.ends and self.starts[-1] == self.ends[-1] + 1:
            return False
        return self.ends and self.ends[-1] == pointer

    def move(self, history):
        history.days = self.days + 1

        line = history.lines[-1]
        history.lines = self.lines
        history.lines.append(line)

        history.starts = self.starts
        history.starts.append(self.ends[-1] + 1)

        history.ends = self.ends

        self.clear()

    def save(self, df, education_program):
        df.loc[len(df)] = [education_program, ', '.join(self.lines), ', '.join(self.starts), ', '.join(self.ends)]
        self.clear()

    def clear(self):
        self.days = 0
        self.lines = []
        self.starts = []
        self.ends = []