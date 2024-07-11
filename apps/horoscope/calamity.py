"""
Vận hạn

Reference:
    https://en.wikipedia.org/wiki/Yakudoshi
"""
from copy import deepcopy

import pandas as pd

from .ganzhi import WeAcKn as WeAcKn_GanZhi


Heavenly_Stems   = WeAcKn_GanZhi['CAN']['Value'].values.tolist()
Earthly_Branches = WeAcKn_GanZhi['CHI']['Value'].values.tolist()


def find_calamity_of_decade(situation: str, gender: str):
    """
    Tính Đại hạn
    """
    if situation.title() == 'Thủy Nhị Cục':
        start_age = 2
    elif situation.title() == 'Mộc Tam Cục':
        start_age = 3
    elif situation.title() == 'Kim Tứ Cục':
        start_age = 4
    elif situation.title() == 'Thổ Ngũ Cục':
        start_age = 5
    elif situation.title() == 'Hỏa Lục Cục':
        start_age = 6
    
    ages = [(start_age + d*10) for d in range(12)]

    from .startionary import PalaceNames

    palaces = deepcopy(PalaceNames)
    if gender not in ['Dương Nam','Âm Nữ']:
        palaces = palaces[:1] + palaces[1:][::-1]

    df = pd.DataFrame({'Cung': palaces, 'Đại hạn': ages})
    return df


def find_calamity_of_year(ye: str, gender: str):
    """
    Tính Tiểu hạn
    """
    ages = deepcopy(Earthly_Branches)

    start_idx = ages.index(ye)
    if start_idx > 0:
        temp = ages + ages
        ages = temp[start_idx:start_idx+12]

    earthlings = deepcopy(Earthly_Branches)
    if gender.lower().endswith('nữ'):
        earthlings = earthlings[::-1]

    if ye in ['Thân','Tỵ','Thìn']:
        e = 'Tuất'
    elif ye in ['Hợi','Mão','Mùi']:
        e = 'Sửu'
    elif ye in ['Dần','Ngọ','Tuất']:
        e = 'Thìn'
    elif ye in ['Tý','Dậu','Sửu']:
        e = 'Mùi'

    start_idx = earthlings.index(e)
    if start_idx > 0:
        temp = earthlings + earthlings
        earthlings = temp[start_idx:start_idx+12]

    df = pd.DataFrame({'Chi': earthlings, 'Tiểu hạn': ages})
    return df


def find_calamity_of_month(situation: str, gender: str):
    """
    Tính Nguyệt hạn
    """
    pass


def find_calamity_of_day(situation: str, gender: str):
    """
    Tính Thời hạn
    """
    pass


if __name__ == "__main__":

    # situation = 'Kim Tứ Cục'
    # gender = 'Âm Nam'
    # yh, ye = 'Ất Hợi'.split(' ')

    # situation = 'Thổ Ngũ Cục'
    # gender = 'Âm Nam'
    # yh, ye = 'Ất Mùi'.split(' ')

    situation = 'Hỏa Lục Cục'
    gender = 'Âm Nữ'
    yh, ye = 'Ất Mão'.split(' ')

    # df = find_calamity_of_decade(situation, gender)
    df = find_calamity_of_year(ye, gender)
    print(df)

