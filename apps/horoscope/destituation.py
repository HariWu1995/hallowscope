"""
Mệnh (Destiny) vs. Cục (Situation)

Reference: 
    https://hocvienlyso.org/chuong-8-sinh-khac-giua-cuc-va-ban-menh.html
"""
from pathlib import Path

import numpy as np
import pandas as pd


wk_dir = Path(__file__).parents[0]
wak_dir = wk_dir / "WeAcKn"

WeAcKn = {
        fn.upper(): pd.read_csv(wak_dir / f"{fn}.csv")
    for fn in ['Mệnh','Cục','Can','Chi','Ngũ Hành','Cung Mệnh','Cung Thân']
}

WeAcKn['NGŨ HÀNH'] = WeAcKn['NGŨ HÀNH'].fillna('Unavailable')

WeAcKn['CỤC'] = WeAcKn['CỤC'].ffill(axis=0, limit=1)\
                             .ffill(axis=1, limit=1)

Mapping = dict()
Mapping['CỤC'] = {
    "Thủy" : "Thủy Nhị Cục",
     "Mộc" :  "Mộc Tam Cục",
     "Kim" :   "Kim Tứ Cục",
     "Thổ" :  "Thổ Ngũ Cục",
     "Hỏa" :  "Hỏa Lục Cục",
}


def determine_destiny_and_situation(yh: str, ye: str, yy: str, 
                                    mm: int, he: str):

    # Mệnh
    destiny_df = WeAcKn['MỆNH'][
                (WeAcKn['MỆNH']['Can'] == yh) & \
                (WeAcKn['MỆNH']['Chi'] == ye)]
    
    destiny = destiny_df['Ngũ hành'].values[0]

    dst_pos = WeAcKn['CUNG MỆNH'].set_index('Tháng \ Giờ').at[mm, he]
    yinyang = WeAcKn['CHI'].set_index('Value').at[dst_pos, 'Âm Dương']
    yinyang = 'Dương' if yinyang else 'Âm'

    # Cục
    situation = WeAcKn['CỤC'].set_index('Cung Mệnh').at[dst_pos, yh]

    # Tương sinh / khắc / hòa
    corr_val = WeAcKn['NGŨ HÀNH'].set_index('Tương quan').at[destiny, situation]
    if corr_val != 'Unavailable':
        corr_src = 'Mệnh'
        corr_dst = 'Cục'
    else:
        corr_val = WeAcKn['NGŨ HÀNH'].set_index('Tương quan').at[situation, destiny]
        if corr_val == 'Unavailable':
            raise ValueError(f"Cannot find correlation for destiny = {destiny} and situation = {situation}")
        corr_src = 'Cục'
        corr_dst = 'Mệnh'

    if corr_val == 'Tương hòa':
        correlation = "Mệnh Cục tương hòa"
    else:
        correlation = f"{corr_src} {corr_val.split(' ')[-1]} {corr_dst}"

    # Âm Dương thuận / nghịch
    favoreverse = 'Thuận' if yinyang == yy else 'Nghịch'
    favoreverse = f"Âm Dương {favoreverse} Lý"

    # Full text
    destiny = destiny_df['Ngũ hành Nạp Âm'].values[0]
    situation = Mapping['CỤC'][situation]

    return destiny, dst_pos, situation, correlation, favoreverse


if __name__ == "__main__":

    destiny, dst_position, situation, \
    correlation, \
    favoreverse = determine_destiny_and_situation(yh='Bính', ye='Tuất', yy='Dương', mm=5, he='Thìn')

    print("Mệnh:", destiny, 'tại', dst_position)
    print("Cục:", situation)
    print(correlation)
    print(favoreverse)
