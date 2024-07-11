# -*- coding: utf-8 -*-
# rewrite from https://github.com/isee15/Lunar-Solar-Calendar-Converter/python
import datetime
from ._compact import unicode_compatible
from ._offset import lunar_month_days, solar_1_1


class DateNotExist(Exception):
    '''
    eg. datetime.date(2017, 2, 29) doesn't exist.
    '''


def GetBitInt(data, length, shift):
    return (data & (((1 << length) - 1) << shift)) >> shift


def SolarToInt(y, m, d):
    m = (m + 9) % 12
    y -= m // 10
    return 365 * y + y // 4 - y // 100 + y // 400 + (m * 306 + 5) // 10 + (d - 1)


def SolarFromInt(g):
    y = (10000 * g + 14780) // 3652425
    ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
    if ddd < 0:
        y -= 1
        ddd = g - (365 * y + y // 4 - y // 100 + y // 400)
    mi = (100 * ddd + 52) // 3060
    mm = (mi + 2) % 12 + 1
    y += (mi + 2) // 12
    dd = ddd - (mi * 306 + 5) // 10 + 1
    solar = Solar(y, mm, dd)
    return solar


# ##########################################

@unicode_compatible
class Solar(object):

    def __init__(self, year, month, day):
        self.day = day
        self.month = month
        self.year = year
        try:
            assert 1 <= month <= 12
            assert 1 <= day <= 31
            if month in [1, 3, 5, 7, 8, 10, 12]:
                assert 1 <= day <= 31
            elif month in [4, 6, 9, 11]:
                assert 1 <= day <= 30
            else:  # month == 2
                if (year % 400 == 0) if (year % 100 == 0) else (year % 4 == 0):
                    assert 1 <= day <= 29
                else:
                    assert 1 <= day <= 28
        except AssertionError:
            raise DateNotExist("Solar({}, {}, {}) doesn't exist".format(year, month, day))

    def __eq__(self, other):
        _other = Converter.Lunar2Solar(other) if isinstance(other, Lunar) else other
        if not isinstance(_other, Solar):
            raise NotImplemented
        return (self.year == _other.year and
                self.month == _other.month and
                self.day == _other.day)

    def __ne__(self, other):  # only PY2
        return not self.__eq__(other)

    def __str__(self):
        return "Solar(year={year}, month={month}, day={day})".format(**vars(self))

    def __repr__(self):
        return "Solar(year={year}, month={month}, day={day})".format(**vars(self))

    def to_date(self):
        ''' convert to datetime.date '''
        return datetime.date(self.year, self.month, self.day)

    @classmethod
    def from_date(cls, that):
        ''' generate from datetime.date '''
        return Solar(that.year, that.month, that.day)


@unicode_compatible
class Lunar(object):

    def __init__(self, year, month, day, isleap=False, check=True):
        self.isleap = isleap
        self.day = day
        self.month = month
        self.year = year
        if check:
            _solar = Converter.Lunar2Solar(self)
            if self != Converter.Solar2Lunar(_solar):
                raise DateNotExist("Lunar({}, {}, {}, {}) doesn't exist".format(year, month, day, isleap))

    def __eq__(self, other):
        _other = Converter.Solar2Lunar(other) if isinstance(other, Solar) else other
        if not isinstance(_other, Lunar):
            raise NotImplemented
        return (self.year == _other.year and
                self.month == _other.month and
                self.day == _other.day and
                self.isleap == _other.isleap)

    def __ne__(self, other):  # only PY2
        return not self.__eq__(other)

    def __str__(self):
        return "Lunar(year={year}, month={month}, day={day}, isleap={isleap})".format(**vars(self))

    def __repr__(self):
        return "Lunar(year={year}, month={month}, day={day}, isleap={isleap})".format(**vars(self))

    def to_date(self):
        ''' convert to datetime.date '''
        solar = Converter.Lunar2Solar(self)
        return datetime.date(solar.year, solar.month, solar.day)

    @classmethod
    def from_date(cls, that):
        ''' generate from datetime.date '''
        return Converter.Solar2Lunar(Solar(that.year, that.month, that.day))


class Converter(object):

    @staticmethod
    def Lunar2Solar(lunar):
        days = lunar_month_days[lunar.year - lunar_month_days[0]]
        leap = GetBitInt(days, 4, 13)
        offset = 0
        loopend = leap
        if not lunar.isleap:
            if lunar.month <= leap or leap == 0:
                loopend = lunar.month - 1
            else:
                loopend = lunar.month

        for i in range(0, loopend):
            offset += GetBitInt(days, 1, 12 - i) == 1 and 30 or 29
        offset += lunar.day
        solar11 = solar_1_1[lunar.year - solar_1_1[0]]

        y = GetBitInt(solar11, 12, 9)
        m = GetBitInt(solar11, 4, 5)
        d = GetBitInt(solar11, 5, 0)

        return SolarFromInt(SolarToInt(y, m, d) + offset - 1)

    @staticmethod
    def Solar2Lunar(solar):
        lunar = type('Auto', (), dict(year=0, month=0, day=0, isleap=False))
        index = solar.year - solar_1_1[0]
        data = (solar.year << 9) | (solar.month << 5) | solar.day
        if solar_1_1[index] > data:
            index -= 1

        solar11 = solar_1_1[index]
        y = GetBitInt(solar11, 12, 9)
        m = GetBitInt(solar11, 4, 5)
        d = GetBitInt(solar11, 5, 0)
        offset = SolarToInt(solar.year, solar.month, solar.day) - SolarToInt(y, m, d)

        days = lunar_month_days[index]
        leap = GetBitInt(days, 4, 13)

        lunarY = index + solar_1_1[0]
        lunarM = 1
        offset += 1

        for i in range(0, 13):
            dm = GetBitInt(days, 1, 12 - i) == 1 and 30 or 29
            if offset > dm:
                lunarM += 1
                offset -= dm
            else:
                break

        lunarD = int(offset)
        lunar.year = lunarY
        lunar.month = lunarM
        lunar.day = lunarD
        lunar.isleap = False
        if leap != 0 and lunarM > leap:
            lunar.month = lunarM - 1
            if lunarM == leap + 1:
                lunar.isleap = True

        return Lunar(lunar.year, lunar.month, lunar.day, lunar.isleap, check=False)


