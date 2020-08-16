from business_trips import find_trips
from external_students import how_much_man
from random2 import randint


def main():
    print('''
         Здравствуйте! Вас приветствует планировщик команды разработчиков PlanE.
         Для максимально эффективного планирования, пожалуйста введите программы подготовки
         в приоритетном для Вас порядке. При прочих равных, предпочтение будет отдаваться программе подготовки,
         стоящей выше в списке. Пожалуйста, введите все или часть из номеров существующих учебных программ. 
         Для остановки ввода введите STOP.
        ''')
    priorities = list()
    buf = input()
    while buf != 'STOP':
        priorities.append(int(buf))
        buf = input()
    least = list({i for i in range(1, 41)} - set(priorities))
    for i in range(len(least)):
        index = randint(i, len(least) - 1)
        least[i], least[index] = least[index], least[i]
    priorities += least
    find_trips(priorities, 'High')
    print(how_much_man(priorities))


if __name__ == "__main__":
    main()
