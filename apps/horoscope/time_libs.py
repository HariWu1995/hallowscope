import pytz
import datetime
import math
import pandas as pd

from ..lunar_calendar import Converter, Solar, Lunar, DateNotExist


def convert_date_from_universal_to_julian(
    day: int, month: int, year: int, 
    hour: int = 0, minute: int = 0, second: int = 0, 
    tz: str = None,
):
    ts = pd.Timestamp(year = year, month = month, day = day,  
                      hour = hour, minute = minute, second = second, tz = tz)
    return ts.to_julian_date()


def convert_date_from_julian_to_universal(day: float, tz: str = None):
    return pd.to_datetime(day - pd.Timestamp(0).to_julian_date(), unit='D')


def convert_date_from_universal_to_lunisolar(
    day: int, month: int, year: int, tz: str = None
):
    u_date = Solar(year=year, month=month, day=day)
    ls_date = Converter.Solar2Lunar(u_date)
    return ls_date.day, ls_date.month, ls_date.year, ls_date.isleap


def convert_date_from_lunisolar_to_universal(
    day: int, month: int, year: int, is_leap: bool, tz: str = None
):
    ls_date = Lunar(year=year, month=month, day=day, isleap=is_leap)
    u_date = Converter.Lunar2Solar(ls_date)
    return u_date.day, u_date.month, u_date.year


if __name__ == "__main__":

    # Error for year < 762
    u_day = dict(
        year = 1995, month = 5, day = 19,  
        hour = 10, minute = 3, second = 16, tz = "Asia/Ho_Chi_Minh"
    )

    j_day = convert_date_from_universal_to_julian(**u_day)
    v_day = convert_date_from_julian_to_universal(j_day)

    print("Pandas:", j_day)
    print("Revert:", v_day)

    del u_day['hour']
    del u_day['minute']
    del u_day['second']
    del u_day['tz']

    solar = Solar(**u_day)
    print(solar)
    lunar = Converter.Solar2Lunar(solar)
    print(lunar)
    solar = Converter.Lunar2Solar(lunar)
    print(solar)
    print(solar.to_date(), type(solar.to_date()))


