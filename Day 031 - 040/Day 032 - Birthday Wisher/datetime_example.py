import datetime as dt

now = dt.datetime.now()
year = now.year
month = now.month
day = now.day
weekday = now.weekday()
print(weekday)

some_birthday = dt.datetime(year=1995, month=12, day= 25)
print(some_birthday.day)