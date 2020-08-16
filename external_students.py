import pandas as pd
import minimal_count_of_people_in_group as one
import people_on_theme as two
import os
def how_much_man(list1):
    dict2 = dict()  
    i=0
    m = len(list1)
    howmuchpeople = 0
    for i in range(m):
        a = one.min_band(list1[i])
        e,f = two.min_people(list1[i], a)
        howmuchpeople = howmuchpeople + e
        dict1 = {list1[i]: [f, e]}
        dict2.update(dict1)
        
    return howmuchpeople, dict2