from datetime import datetime
from persiantools.jdatetime import JalaliDate


def jalali_first_day_of_month() -> datetime:
    jalali_date = JalaliDate.today()
    year = jalali_date.year
    month = jalali_date.month
    day = 1
    first_day_of_month = JalaliDate(year, month, day)
    return first_day_of_month.to_gregorian()


def jalali_day_of_month() -> int:
    return JalaliDate.today().day


def jalali_day_in_month() -> int:
    jalali_date = JalaliDate.today()
    year = jalali_date.year
    month = jalali_date.month
    return JalaliDate.days_in_month(month, year)
