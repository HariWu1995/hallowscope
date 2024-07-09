"""
(c) 2006 Ho Ngoc Duc.
Astronomical algorithms
    from the book "Astronomical Algorithms" by Jean Meeus, 1998

Reference: 
    https://github.com/doanguyen/lasotuvi/blob/master/lasotuvi/Lich_HND.py
"""
import pytz
import datetime
import math


def convert_date_from_universal_to_julian(
    day: int, month: int, year: int, 
    hour: int = 0, minute: int = 0, second: int = 0, 
):
    # march_on will be 1 for January and February, and 0 for others.
    march_on = int((14 - month) / 12)
    year = year + 4800 - march_on

    # And 'month' will be 0 for March and 11 for February. 0 - 11 months
    month = month + 12 * march_on - 3

    quarter = int(year / 4)
    jd = day + int((month * 153 + 2) / 5) + 365 * year + quarter \
             + int(year / 100) - int(quarter / 100) - 32045

    # Check whether Julian or Gregorian calendar
    if jd < 2299161:
        jd = day + int((month * 153 + 2) / 5) + 365 * year + quarter - 32083
    
    return jd


def convert_date_from_julian_to_universal(jd: float):

    # Since 5/10/1582, Gregorian calendar
    is_gregorian = jd > 2299160
    if is_gregorian:
        a = jd + 32044
        b = int((4 * a + 3) / 146097.)
        c = a - int((b * 146097) / 4.)
    
    else:
        b = 0
        c = jd + 32082
        
    d = int((4 * c + 3) / 1461.)
    e = c - int((1461 * d) / 4.)
    m = int((5 * e + 2) / 153.)

    day = e - int((153 * m + 2) / 5.) + 1
    month = m + 3 - 12 * int(m / 10.)
    year = b * 100 + d - 4800 + int(m / 10.)
    return day, month, year


def get_tz_offset(day: datetime.datetime, tz: str):
    tz = pytz.timezone(tz)
    day = day.replace(tzinfo=tz)
    tz = day.utcoffset().total_seconds() / 3600.
    return tz


def get_sun_longitude(jd: float, tz: float):        

    T = (jd - 2451545.5 - tz / 24.) / 36525.
    T2 = T**2
    dr = math.pi / 180.
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2
    DL = (1.914600 - 0.004817*T - 0.000014*T2) * math.sin(dr*M)
    DL = DL + (0.019993 - 0.000101*T) * math.sin(dr*2*M) + 0.000290 * math.sin(dr*3*M)
    L = L0 + DL
    omega = 125.04 - 1934.136 * T
    L = L - 0.00569 - 0.00478 * math.sin(omega * dr)
    L = L*dr
    L = L - math.pi * 2 * (math.floor(L / (math.pi*2)))
    return int(L / math.pi*6)


def compute_new_moon(k):
    '''
    Compute the time of the k-th new moon after the new moon of 1/1/1900 13:52 UCT, 
        measured as the number of days since 1/1/4713 BC noon UCT, 
        e.g., 2451545.125 is 1/1/2000 15:00 UTC.

    Returns a floating number, 
        e.g., 2415079.9758617813 for k=2 or
              2414961.935157746 for k=-2.
    '''
    # Time in Julian centuries from 1900 January 0.5
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180.
    Jd = 2415020.75933 + 29.53058868 * k \
        + 0.0001178 * T2 - 0.000000155 * T3
    Jd = Jd + 0.00033 * math.sin(
        (166.56 + 132.87 * T - 0.009173 * T2) * dr)

    # Mean new moon
    M = 359.2242 + 29.10535608 * k \
        - 0.0000333 * T2 - 0.00000347 * T3

    # Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806 * k \
        + 0.0107306 * T2 + 0.00001236 * T3

    # Moon's mean anomaly
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 \
        - 0.00000239 * T3

    # Moon's argument of latitude
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) \
        + 0.0021 * math.sin(2 * dr * M)
    C1 = C1 - 0.4068 * math.sin(Mpr * dr) \
        + 0.0161 * math.sin(dr * 2 * Mpr)
    C1 = C1 - 0.0004 * math.sin(dr * 3 * Mpr)
    C1 = C1 + 0.0104 * math.sin(dr * 2 * F) \
        - 0.0051 * math.sin(dr * (M + Mpr))
    C1 = C1 - 0.0074 * math.sin(dr * (M - Mpr)) \
        + 0.0004 * math.sin(dr * (2 * F + M))
    C1 = C1 - 0.0004 * math.sin(dr * (2 * F - M)) \
        - 0.0006 * math.sin(dr * (2 * F + Mpr))
    C1 = C1 + 0.0010 * math.sin(dr * (2 * F - Mpr)) \
        + 0.0005 * math.sin(dr * (2 * Mpr + M))

    if T < -11:
        delta = 0.001 + 0.000839 * T + 0.0002261 * T2 \
                - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        delta = -0.000278 + 0.000265 * T + 0.000262 * T2

    return Jd + C1 - delta


def get_new_moon_day(k: int, tz: float):
    return int(compute_new_moon(k) + 0.5 + tz / 24.)


def get_lunar_month_11(year: int, tz: float):
    '''
    Find the day that starts the lunar month 11 
        of the given year 
        for the given timezone.
    '''
    offset = convert_date_from_universal_to_julian(day=31, month=12, year=year) - 2415021.
    k = int(offset / 29.530588853)
    new_moon = get_new_moon_day(k, tz)
    sunLong = get_sun_longitude(new_moon, tz)

    # sun longitude at local midnight
    if sunLong >= 9:
        new_moon = get_new_moon_day(k-1, tz)
    return new_moon


def get_leap_month_offset(day: float, tz: float):
    '''
    Find the index of the leap month
        after the month starting on the day.
    '''
    k = int((day - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1  # start with month following lunar month 11
    arc = get_sun_longitude(
            get_new_moon_day(k+i, tz), tz)

    last = 0
    while True:
        last = arc
        i += 1
        arc = get_sun_longitude(
            get_new_moon_day(k+i, tz), tz)
        if not (arc != last and i < 14):
            break

    return i - 1


def convert_date_from_universal_to_lunisolar(day: int, 
                                           month: int, 
                                            year: int, 
                                              tz: float = 7):

    day_number = convert_date_from_universal_to_julian(day=day, month=month, year=year)
    
    k = int((day_number - 2415021.076998695) / 29.530588853)
    month_start = get_new_moon_day(k+1, tz)
    if (month_start > day_number):
        month_start = get_new_moon_day(k, tz)
    # alert(day_number + " -> " + month_start)
    
    a11 = get_lunar_month_11(year, tz)
    b11 = a11
    if (a11 >= month_start):
        lunar_year = year
        a11 = get_lunar_month_11(year-1, tz)
    else:
        lunar_year = year + 1
        b11 = get_lunar_month_11(year+1, tz)

    lunar_day = day_number - month_start + 1
    diff = int((month_start - a11) / 29.)

    lunar_leap = False
    lunar_month = diff + 11

    if b11 - a11 > 365:
        leap_month_diff = get_leap_month_offset(a11, tz)
        if diff >= leap_month_diff:
            lunar_month = diff + 10
            if diff == leap_month_diff:
                lunar_leap = True

    if lunar_month > 12:
        lunar_month = lunar_month - 12
    if lunar_month >= 11 and diff < 4:
        lunar_year -= 1

    return lunar_day, lunar_month, lunar_year, lunar_leap


def convert_date_from_lunisolar_to_universal(lunar_day: int, 
                                             lunar_month: int, 
                                             lunar_year: int, 
                                             lunar_leap: bool, 
                                             tz: float = 7):
    if lunar_month < 11:
        a11 = get_lunar_month_11(lunar_year-1, tz)
        b11 = get_lunar_month_11(lunar_year, tz)
    else:
        a11 = get_lunar_month_11(lunar_year, tz)
        b11 = get_lunar_month_11(lunar_year+1, tz)

    k = int(0.5 + (a11 - 2415021.076998695) / 29.530588853)
    offset = lunar_month - 11
    if offset < 0:
        offset += 12
    if b11 - a11 > 365:
        leap_offset = get_leap_month_offset(a11, tz)
        leap_month = leap_offset - 2
        if leap_month < 0:
            leap_month += 12
        if lunar_leap and lunar_month != leap_month:
            return [0, 0, 0]
        elif lunar_leap or offset >= leap_offset:
            offset += 1

    month_start = get_new_moon_day(k + offset, tz)
    return convert_date_from_julian_to_universal(month_start + lunar_day - 1)


if __name__ == "__main__":

    u_day = dict(
        year = 1700, month = 5, day = 19,  
        # hour = 10, minute = 3, second = 16, 
        # tz = "Asia/Ho_Chi_Minh"
    )

    j_day = convert_date_from_universal_to_julian(**u_day)
    v_day = convert_date_from_julian_to_universal(j_day)

    print("Original:", u_day)
    print("Convert:", j_day)
    print("Revert:", v_day)
    


