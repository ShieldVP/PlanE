import pandas as pd
import minimal_count_of_people_in_group as one
import people_on_theme as two
import os
def how_much_man(list1):
    i=0
    m = len(list1)
    howmuchpeople = 0
    for i in range(m):
        a = one.min_band(list1[i])
        howmuchpeople = howmuchpeople + two.min_people(list1[i], a)
    return (howmuchpeople)
