"""
Star Stationary - An Sao

Reference:
    https://lichngaytot.com/tu-vi/cac-buoc-lap-la-so-tu-vi-304-217457.html
"""
import os
from pathlib import Path
from collections import OrderedDict

import numpy as np
import pandas as pd


wk_dir = Path(__file__).parents[0]
wak_dir = wk_dir / "WeAcKn"

WeAcKn = {
        fn.upper(): pd.read_csv(wak_dir / f"{fn}.csv")
    for fn in ['Overview','Interpretation','Destiny','Đắc Tinh']
}

WeAcKn['OVERVIEW']        = WeAcKn['OVERVIEW'].dropna(subset=['Tên'], axis=0)
WeAcKn['OVERVIEW']['Tên'] = WeAcKn['OVERVIEW']['Tên'].apply(lambda x: x.title())

WeAcKn.update({
        fn[:-4].upper(): pd.read_csv(wak_dir / fn)
    for fn in os.listdir(wak_dir)
     if fn.startswith('An')
})


PalaceNames = [
    'Mệnh','Phụ mẫu','Phúc đức','Điền trạch','Quan lộc','Nô bộc',
    'Thiên di','Tật ách','Tài bạch','Tử tức','Phu thê','Huynh đệ',
]

HeavenTable = pd.DataFrame.from_records(
    columns = ['id','Chi','row','col'],
       data = [( 1,  'Tý', 4, 3),
               ( 2, 'Sửu', 4, 2),
               ( 3, 'Dần', 4, 1),
               ( 4, 'Mão', 3, 1),
               ( 5,'Thìn', 2, 1),
               ( 6,  'Tỵ', 1, 1),
               ( 7, 'Ngọ', 1, 2),
               ( 8, 'Mùi', 1, 3),
               ( 9,'Thân', 1, 4),
               (10, 'Dậu', 2, 4),
               (11,'Tuất', 3, 4),
               (12, 'Hợi', 4, 4)],
)


def get_available_stars_and_states():

    stars = WeAcKn['OVERVIEW']['Tên'].values.tolist()
    states = [None, 'M', 'V', 'Đ', 'B', 'H']

    ststts = []
    for st in stars:
        for stt in states:
            if stt is None:
                ststts.append(st)
            else:
                ststts.append(f"{st} [{stt}]")
    return ststts


def locate_all_stars_and_states(
   destiny: str, destiny_pos: str, situation: str, 
        dd: int, 
        mm: int, 
        he: str,
        yh: str,
        ye: str, 
    gender: str,
):
    # Khởi tạo Thiên Bàn
    thable = HeavenTable.copy(deep=True)

    # An Cung: Mệnh -> Phụ Mẫu -> ... -> Huynh Đệ
    earthlings = HeavenTable['Chi'].values.tolist()
    destiny_idx = earthlings.index(destiny_pos)
    if destiny_idx > 0:
        temp = earthlings + earthlings
        earthlings = temp[destiny_idx:destiny_idx+12]
    palaces_order = pd.DataFrame({ 'Cung': PalaceNames, 
                                    'Chi': earthlings, })
    thable = thable.merge(palaces_order, on=['Chi'], how='left')
    thable = thable.sort_values(by=['Cung'], 
                                key=lambda x: x.map({p: pi 
                                                    for pi, p in enumerate(PalaceNames)}))
    # An Sao: Chính tinh
    thable = locate_main_stars(thable, day=dd, situation=situation)

    # An Sao: Phụ tinh
    thable = thable.set_index('Chi')
    thable = locate_aux_stars(thable, hour=he, month=mm, yr_e=ye, yr_h=yh, 
                                    gender=gender, situation=situation)
    print(thable.drop(columns=['id','row','col']))
    return thable


def locate_star_TuVi(day: int, situation: str):

    situation = situation.title()
    coord = WeAcKn['AN SAO TỬ VI'].set_index('Ngày sinh').at[day, situation]

    return coord


def locate_main_stars(thable: pd.DataFrame, 
                      day: int, situation: str) -> pd.DataFrame:

    e_idx = locate_star_TuVi(day=day, situation=situation)

    m_stars = WeAcKn['AN CHÍNH TINH'].set_index('Cung Tử Vi').loc[e_idx]
    m_stars = m_stars.to_frame().reset_index(drop=False)\
                                .rename(columns={'index': 'Chi', e_idx: 'Chính tinh'})\
                                .replace({'Chính tinh': {'Vô chính diệu': ''}})
    
    thable = thable.merge(m_stars, on=['Chi'], how='left')
    return thable


def locate_aux_stars(thable: pd.DataFrame, 
                     hour: str, month: int, 
                     yr_e: str, yr_h: str, 
                   gender: str, 
                situation: str, **kwargs) -> pd.DataFrame:

    thable['Phụ tinh'] = '' * len(thable)

    # 1. An Sao theo Giờ sinh:
    #       Văn Xương, Văn Khúc, Thai Phụ, Phong Cáo, Địa Không, Địa Kiếp
    stars = WeAcKn['AN PHỤ TINH - GIỜ'][['Sao', hour]].rename(columns={hour: 'Chi'})
    for _, (s, e) in stars.iterrows():
        s = add_status_to_star(s, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 2. An Sao theo Tháng sinh: 
    #       Hữu Bật, Tả Phù, Thiên Giải, Thiên Y, Thiên Riêu, Thiên Hình
    month = str(month)
    stars = WeAcKn['AN PHỤ TINH - THÁNG'][['Sao', month]].rename(columns={month: 'Chi'})
    for _, (s, e) in stars.iterrows():
        s = add_status_to_star(s, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 3. An Sao theo CAN Năm sinh
    stars = WeAcKn['AN PHỤ TINH - NĂM (CAN)'][['Sao', yr_h]].rename(columns={yr_h: 'Chi'})
    stbrs = stars[stars['Sao'].isin(['Triệt Không'])]
    stcrs = stars[stars['Sao'].isin(['Hóa Lộc','Hóa Quyền','Hóa Khoa','Hóa Kỵ'])]
    stars = stars[~stars['Sao'].isin(['Hóa Lộc','Hóa Quyền','Hóa Khoa','Hóa Kỵ','Triệt Không'])]

    # 3a. Phụ tinh đi theo Cung:
    #       Đà La, Lộc Tồn, Kình Dương, Quốc Ấn, Đường Phù, Văn Tinh,
    #       Thiên Khôi, Thiên Việt, Thiên Quan, Thiên Phúc, Lưu Hà, Thiên Trù
    for _, (s, e) in stars.iterrows():
        s = add_status_to_star(s, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 3b. Phụ tinh đi theo Cung Đôi:
    #       Triệt Không
    S, es = stbrs.T.values
    S = S[0]
    for e in es[0].split(' + '):
        s = add_status_to_star(S, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 3c. Phụ tinh đi theo Chính tinh:
    #       Hóa Lộc, Hóa Quyền, Hóa Khoa, Hóa Kị]
    for _, (s, m) in stcrs.iterrows():
        m = m[1:]
        df = thable[thable['Chính tinh'].str.contains(m, case=True, na=False)]
        e = df.index.values[0]
        s = add_status_to_star(s, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 4. An Sao theo CHI Năm sinh: 
    #       Thiên Mã, Hoa Cái, Kiếp Sát, Đào Hoa, Phá Toái, Cô Thần, Quả Tú,
    #       Thiên Không, Thiên Khốc, Thiên Hư, Thiên Đức, Nguyệt Đức, 
    #       Hồng Loan, Thiên Hỷ, Long Trì, Phượng Các, Giải Thần
    stars = WeAcKn['AN PHỤ TINH - NĂM (CHI)'][['Sao', yr_e]].rename(columns={yr_e: 'Chi'})
    for _, (s, e) in stars.iterrows():
        s = add_status_to_star(s, e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s 

    # 5. An Sao: Tuần Không
    es = WeAcKn['AN SAO TUẦN KHÔNG'].set_index('Cung Mệnh').at[yr_e, yr_h]
    es = es.split(', ')
    for e in es:
        s = add_status_to_star('Tuần Không', e)
        thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 6. An Sao: Hỏa Tinh
    df = WeAcKn['AN SAO HỎA TINH'].copy(deep=True)
    df = df[(df['Năm sinh'] == yr_e) & \
            (df['Dương Nam - Âm Nữ'] == (gender in ['Dương Nam','Âm Nữ']))]
    e = df[hour].values[0]
    s = add_status_to_star('Hỏa Tinh', e)
    thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 7. An Sao: Linh Tinh
    df = WeAcKn['AN SAO LINH TINH'].copy(deep=True)
    df = df[(df['Năm sinh'] == yr_e) & \
            (df['Dương Nam - Âm Nữ'] == (gender in ['Dương Nam','Âm Nữ']))]
    e = df[hour].values[0]
    s = add_status_to_star('Linh Tinh', e)
    thable.loc[e, 'Phụ tinh'] = thable.loc[e, 'Phụ tinh'] + ' - ' + s

    # 8. An Sao: vòng Thái Tuế
    extremities = ['Thái Tuế','Thiếu Dương','Tang Môn','Thiếu Âm','Quan Phù','Tử Phù',
                   'Tuế Phá','Long Đức','Bạch Hổ','Phúc Đức','Điếu Khách','Trực Phù']
    
    earthlings = HeavenTable['Chi'].values.tolist()
    start_idx = earthlings.index(yr_e)
    if start_idx > 0:
        temp = earthlings + earthlings
        earthlings = temp[start_idx:start_idx+12]

    col = 'Vòng Thái Tuế'
    extremity_circle = pd.DataFrame({col : extremities, 
                                    'Chi': earthlings, })
    extremity_circle[col] = extremity_circle.apply(lambda x: add_status_to_star(*x.values), axis=1)

    thable = thable.merge(extremity_circle, on=['Chi'], how='left')

    # 9. An Sao: vòng Bác Sỹ / Lộc Tồn
    fortunities = ['Bác Sỹ','Lực Sỹ','Thanh Long','Tiểu Hao','Tướng Quân','Tấu Thư',
                   'Phi Liêm','Hỷ Thần','Bệnh Phù','Đại Hao','Phục Binh','Quan Phủ']
    start_pos = thable[
                thable['Phụ tinh'].str.contains('Lộc Tồn', case=True, na=False)]['Chi'].values[0]

    earthlings = HeavenTable['Chi'].values.tolist()
    if gender not in ['Dương Nam','Âm Nữ']:
        earthlings = earthlings[::-1]

    start_idx = earthlings.index(start_pos)
    if start_idx > 0:
        temp = earthlings + earthlings
        earthlings = temp[start_idx:start_idx+12]

    col = 'Vòng Bác Sỹ'
    fortunity_circle = pd.DataFrame({col : fortunities, 
                                    'Chi': earthlings, })
    fortunity_circle[col] = fortunity_circle.apply(lambda x: add_status_to_star(*x.values), axis=1)

    thable = thable.merge(fortunity_circle, on=['Chi'], how='left')

    # 10. An Sao: vòng Trường Sinh
    eternities = ['Trường Sinh','Mộc Dục','Quan Đới','Lâm Quan','Đế Vượng',
                  'Suy','Bệnh','Tử','Mộ','Tuyệt','Thai','Dưỡng']

    if situation.startswith('Thủy'):
        start_pos = 'Thân'
    elif situation.startswith('Mộc'):
        start_pos = 'Hợi'
    elif situation.startswith('Kim'):
        start_pos = 'Tỵ'
    elif situation.startswith('Thổ'):
        start_pos = 'Thân'
    elif situation.startswith('Hỏa'):
        start_pos = 'Dần'

    earthlings = HeavenTable['Chi'].values.tolist()
    if gender not in ['Dương Nam','Âm Nữ']:
        earthlings = earthlings[::-1]

    start_idx = earthlings.index(start_pos)
    if start_idx > 0:
        temp = earthlings + earthlings
        earthlings = temp[start_idx:start_idx+12]

    col = 'Vòng Trường Sinh'
    eternity_circle = pd.DataFrame({col : eternities, 
                                   'Chi': earthlings, })
    eternity_circle[col] = eternity_circle.apply(lambda x: add_status_to_star(*x.values), axis=1)

    thable = thable.merge(eternity_circle, on=['Chi'], how='left')

    # 11. An Sao:
    #       Ân Quang, Thiên Quý, Tam Thai, Bát Tọa, Đẩu Quân, Thiên Tài, Thiên Thọ,
    #       Thiên Thương, Thiên Sứ, Thiên La, Địa Võng

    # 12. An Sao lưu niên

    return thable


def add_status_to_star(star: str, earthling: str):

    if star in WeAcKn['ĐẮC TINH']['Sao'].values:
        stt = WeAcKn['ĐẮC TINH'].set_index('Sao').at[star, earthling]
        if isinstance(stt, str):
            star += f' [{stt}]'
    return star


if __name__ == "__main__":

    destiny = "Sơn đầu hỏa"
    destiny_pos = "Thìn"
    situation = "Kim tứ cục"

    hour = 'Sửu'
    day = 20
    month = 4
    year = 1995
    yh, ye = 'Ất Hợi'.split(' ')
    gender = 'Âm Nam'

    # destiny = "Ốc thượng thổ"
    # destiny_pos = "Dần"
    # situation = "Mộc tam cục"

    # hour = 'Thìn'
    # day = 15
    # month = 5
    # year = 1946
    # yh, ye = 'Bính Tuất'.split(' ')
    # gender = 'Dương Nam'

    thable = locate_all_stars_and_states(
        destiny, destiny_pos, situation,
        day, month, 
        hour, 
        yh, ye,
        gender
    )

    thable.to_csv('draft/thable.csv', index=False)

