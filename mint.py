import pandas as pd
import os
def min_band(name):
    p1 = pd.read_excel(os.path.join(r'input_data', 'min_group.xlsx'))  
    p2 = pd.read_excel(os.path.join(r'input_data', 'predmetes.xlsx'), sheet_name='параметры аудиторий')
    i=0
    min=10000
    a=1
    a=p1[name].shape[0]
    for i in range(a):
        s1=p1[name][i]
        print(p1['Аудитрия'][0])
        if s1==p2['Аудитрия'][0]:
            if p2['Количество мест'][0]<min:
                print(p2['Количество мест'][0])
                min=p2['Количество мест'][0]
        if s1==p2['Аудитрия'][1]:
            if p2['Количество мест'][1]<min:
                min=p2['Количество мест'][1]
        if s1==p2['Аудитрия'][2]:
            if p2['Количество мест'][2]<min:
                min=p2['Количество мест'][2]
        if s1==p2['Аудитрия'][3]:
            if p2['Количество мест'][3]<min:
                min=p2['Количество мест'][3]
        if s1==p2['Аудитрия'][4]:
            if p2['Количество мест'][4]<min:
                min=p2['Количество мест'][4]
        if s1==p2['Аудитрия'][5]:
            if p2['Количество мест'][5]<min:
                min=p2['Количество мест'][5]
        if s1==p2['Аудитрия'][6]:
            if p2['Количество мест'][6]<min:
                min=p2['Количество мест'][6]
        if s1==p2['Аудитрия'][7]:
            if p2['Количество мест'][7]<min:
                min=p2['Количество мест'][7]
        if s1==p2['Аудитрия'][8]:
            if p2['Количество мест'][8]<min:
                min=p2['Количество мест'][8]
        if s1==p2['Аудитрия'][9]:
            if p2['Количество мест'][9]<min:
                min=p2['Количество мест'][9]
        if s1==p2['Аудитрия'][10]:
            if p2['Количество мест'][10]<min:
                min=p2['Количество мест'][10]
    return (min)

