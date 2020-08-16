import pandas as pd
import os
def min_people(name, mint): 
    p1 = pd.read_excel(os.path.join(r'input_data', 'all days.xlsx'))  
    sotr = p1[name][2]
    days_for_one_team = p1[name][0] 
    program_days = p1[name][1] #в последствии, из разных файлов
    howmuch = mint * program_days / days_for_one_team - sotr
    return (howmuch, program_days / days_for_one_team)