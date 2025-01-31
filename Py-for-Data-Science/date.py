from datetime import date, datetime
datetime = datetime(2019,11,27,11,27,22)
print(datetime.strftime("%y/%B/%d %H:%M:%S")) # %B displays month in words

from datetime import date
date_1 = date(1992, 1, 16)
date_2 = date(1991, 2, 5)
print(date_1 - date_2)


import calendar
c = calendar.Calendar()
for weekday in c.iterweekdays():
    print(weekday, end="")


from datetime import timedelta
delta = timedelta(weeks=1, days=7, hours=11)
print(delta*2)


import calendar
calendar.setfirstweekday(calendar.SUNDAY)
print(calendar.weekheader(3))


from datetime import datetime
datetime_1 = datetime(2019,11,27,11,27,22)
datetime_2 = datetime(2019,11,27,0,0,0)
print(datetime_1-datetime_2)