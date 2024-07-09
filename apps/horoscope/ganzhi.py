"""
Thiên Can - Địa Chi

Reference: https://vi.wikipedia.org/wiki/Can_Chi
"""
import datetime
from pathlib import Path

import numpy as np
import pandas as pd


wk_dir = Path(__file__).parents[0]
wak_dir = wk_dir / "WeAcKn"

WeAcKn_GanZhi = {
        fn.upper(): pd.read_csv(wak_dir / f"{fn}.csv")
    for fn in ['Can','Chi','Year','Month','Hour']
}



def find_ganzhi_of_lunar_year(year: int):
    year_ganzhi = WeAcKn_GanZhi['YEAR'].copy(deep=True)
    year_ganzhi = year_ganzhi[
                  year_ganzhi['ID'] == (year % 60)]

    assert len(year_ganzhi) == 1, \
        f"Cannot find ganzhi for year = {year}.\n{year_ganzhi}"
    
    return year_ganzhi['Can'].values[0], \
           year_ganzhi['Chi'].values[0]


def find_ganzhi_of_month(month: int, heaven_of_year: str):
    month_ganzhi = WeAcKn_GanZhi['MONTH'].copy(deep=True)
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
    can = WeAcKn_GanZhi['CAN']['Value'].values[offset % 10]
    chi = WeAcKn_GanZhi['CHI']['Value'].values[offset % 12]

    return can, chi


def find_ganzhi_of_hour(hour: float, heaven_of_day: str, 
                      minute: int = 0, 
                      second: int = 0, ):
    if minute > 0:
        hour = hour + minute / 60.
    if second > 0:
        hour = hour + second / 3600.
    hour += 1.
        
    hour_ganzhi = WeAcKn_GanZhi['HOUR'].copy(deep=True).replace(dict(Start={23: -1}))
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


if __name__ == "__main__":

    from time_algo import (
        convert_date_from_universal_to_lunisolar,
        convert_date_from_universal_to_julian,
    )

    day, month, year = 19, 5, 1895
    day, month, year, is_leap = convert_date_from_universal_to_lunisolar(day, month, year)

    can, chi = find_ganzhi_of_lunar_year(year)
    print("Năm:", can, chi)

    can, chi = find_ganzhi_of_month(month, heaven_of_year=can)
    print("Tháng:", can, chi)

    day, month, year = 19, 5, 1895
    hour, minute, second = 1, 2, 3

    can, chi = find_ganzhi_of_day(day, month, year)
    print("Ngày:", can, chi)

    can, chi = find_ganzhi_of_hour(hour, can, minute, second)
    print("Giờ:", can, chi)

