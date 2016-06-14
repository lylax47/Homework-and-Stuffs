# with open('event_info.csv', 'r', encoding = 'utf-8') as cv:
# 	info = cv.read()


import pandas 
df = pandas.read_csv("event_info.csv", sep = '\t')