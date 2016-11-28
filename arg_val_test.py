#!/usr/bin/env python


import sys
import datetime


print sys.argv[1]
print sys.argv[2]

date= datetime.datetime.now().date()

date = str(date)
print date
split = date.find("-", 5)

day = date[split+1::]
month =  date[5:split]
print  month + "_" + day
