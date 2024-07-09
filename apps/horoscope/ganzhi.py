"""
Thiên Can vs. Địa Chi

Reference: 
    https://vi.wikipedia.org/wiki/Can_Chi
"""
import datetime
from pathlib import Path

import numpy as np
import pandas as pd


wk_dir = Path(__file__).parents[0]
wak_dir = wk_dir / "WeAcKn"

WeAcKn = {
        fn.upper(): pd.read_csv(wak_dir / f"{fn}.csv")
    for fn in ['Can','Chi','Year','Month','Hour']
}


def find_ganzhi_of_lunar_year(year: int):
    year_ganzhi = WeAcKn['YEAR'].copy(deep=True)
    year_ganzhi = year_ganzhi[
                  year_ganzhi['ID'] == (year % 60)]

    assert len(year_ganzhi) == 1, \
        f"Cannot find ganzhi for year = {year}.\n{year_ganzhi}"
    
    return year_ganzhi['Can'].values[0], \
           year_ganzhi['Chi'].values[0]


def find_ganzhi_of_month(month: int, heaven_of_year: str):
    month_ganzhi = WeAcKn['MONTH'].copy(deep=True)
    month_ganzhi = month_ganzhi[
                   month_ganzhi['Tháng'] == month]
    month_ganzhi = month_ganzhi[heaven_of_year]

    assert len(month_ganzhi) == 1, \
        f"Cannot find ganzhi for month = {month} of CAN(year) = {heaven_of_year}.\n{month_ganzhi}"

    ganzhi = month_ganzhi.values[0]
    return ganzhi.split(' ')
    

def find_ganzhi_of_day(day: int, month: int, year: int):

    # Pick a certain date to represent GIÁP TÝ (the start of Sexagenary Cycle of Ganzhi)
    # milestone = datetime.date(day=7, month=3, year=2000)
    milestone = datetime.date(day=17, month=5, year=1918)

    # Find the positive day-difference to count
    query_date = datetime.date(day=day, month=month, year=year)
    offset = (query_date - milestone).days

    # Find Ganzhi
    can = WeAcKn['CAN']['Value'].values[offset % 10]
    chi = WeAcKn['CHI']['Value'].values[offset % 12]

    return can, chi


def find_ganzhi_of_hour(hour: float, heaven_of_day: str, 
                      minute: int = 0, 
                      second: int = 0, ):
    if minute > 0:
        hour = hour + minute / 60.
    if second > 0:
        hour = hour + second / 3600.
    hour += 1.
        
    hour_ganzhi = WeAcKn['HOUR'].copy(deep=True).replace(dict(Start={23: -1}))
    hour_ganzhi['Start'] = hour_ganzhi['Start'] + 1
    hour_ganzhi[ 'End' ] = hour_ganzhi[ 'End' ] + 1

    hour_ganzhi = hour_ganzhi[
                 (hour_ganzhi['Start'] < hour) & \
                 (hour_ganzhi['End'] >= hour)
                ]

    assert len(hour_ganzhi) == 1, \
        f"Cannot find ganzhi for hour = {hour}.\n{hour_ganzhi}"

    heavn = heaven_of_day
    return hour_ganzhi[heavn].values[0], \
           hour_ganzhi['Giờ'].values[0]


def find_ganzhi_of_time(day: int, month: int, year: int, 
                        hour: int, minute: int = 0, second: int = 0):

    from .time_libs import convert_date_from_universal_to_lunisolar

    ls_day, ls_month, \
    ls_year, is_leap = convert_date_from_universal_to_lunisolar(day, month, year)

    # Find GanZhi
    Y4_h, Y4_e = find_ganzhi_of_lunar_year(ls_year)
    MM_h, MM_e = find_ganzhi_of_month(ls_month, heaven_of_year=Y4_h)
    DD_h, DD_e = find_ganzhi_of_day(day, month, year)
    hh_h, hh_e = find_ganzhi_of_hour(hour, DD_h, minute, second)

    # Find Yin-Yang
    Y4_y = WeAcKn['CHI'][
           WeAcKn['CHI']['Value'] == Y4_e]['Âm Dương'].values[0]
    Y4_y = 'Dương' if Y4_y else 'Âm'

    return ls_day, DD_h, DD_e,       \
         ls_month, MM_h, MM_e,       \
          ls_year, Y4_h, Y4_e, Y4_y, \
                   hh_h, hh_e


if __name__ == "__main__":

    from time_libs import (
        convert_date_from_universal_to_lunisolar,
    )

    u_day, u_month, u_year = 19, 5, 1995
    ls_day, ls_month, ls_year, is_leap = convert_date_from_universal_to_lunisolar(u_day, u_month, u_year)

    can, chi = find_ganzhi_of_lunar_year(ls_year)
    print("Năm:", ls_year, can, chi)

    can, chi = find_ganzhi_of_month(ls_month, heaven_of_year=can)
    print("Tháng:", ls_month, can, chi)

    can, chi = find_ganzhi_of_day(u_day, u_month, u_year)
    print("Ngày:", ls_day, can, chi)

    hour, minute, second = 1, 2, 3
    can, chi = find_ganzhi_of_hour(hour, can, minute, second)
    print(f"Giờ: {hour:02d}:{minute:02d}:{second:02d}", can, chi)

