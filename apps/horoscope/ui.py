import os
import datetime

import numpy as np

import gradio as gr
from gradio_calendar import Calendar


# Load data
from .ganzhi import WeAcKn as WeAcKn_GanZhi
from .startionary import get_available_stars_and_states

Heavenly_Stems   = WeAcKn_GanZhi['CAN']['Value'].values.tolist()
Earthly_Branches = WeAcKn_GanZhi['CHI']['Value'].values.tolist()

Stars_States = get_available_stars_and_states()


# Process data
from .ganzhi import find_ganzhi_of_time
from .destituation import determine_destiny_and_situation
from .startionary import locate_all_stars_and_states

def read_the_destiny(dd: int, dh: str, de: str,
                     mm: int, mh: str, me: str,
                     y4: int, yh: str, ye: str, yy: str,
                              hh: str, he: str, 
                     uh: int, um: int, gd: str, ):

    # Center of Table
    destiny, destiny_pos, \
        situation, \
        correlation, \
        favoreverse = determine_destiny_and_situation(yh=yh, ye=ye, yy=yy, mm=mm, he=he)

    # Heavenly Table - Thable
    thable = locate_all_stars_and_states(destiny, destiny_pos, situation,
                                         dd, mm, he, yh, ye, gender=gd)

    return (
        # Center of Table
        f"{mm} - {mh} {me}", 
        f"{dd} - {dh} {de}", 
        f"{uh:02d}:{um:02d} - {hh} {he}", 
        f"{yy} {gd}", 
        destiny, situation, correlation, 
        destiny_pos, favoreverse,

        # Heavenly Table - Thable
        ["Tử Vi [Đ]","Thiên Tướng [H]","Tham Lang"]
    )

# Define UI settings & layout
min_width = 25

with gr.Blocks(css=None, analytics_enabled=False) as gui:

    gr.Markdown("# 🛈 Thông tin cá nhân")
    with gr.Row():
        with gr.Column(scale=3, variant='panel', min_width=min_width):
            name = gr.Textbox(label="Họ tên", placeholder="Họ tên đầy đủ")
        with gr.Column(scale=1, variant='panel', min_width=min_width):
            gender = gr.Dropdown(label="Giới tính", choices=['Nam','Nữ'], interactive=True)
        with gr.Column(scale=1):
            gr.Markdown("")

    gr.Markdown("## <b>Sinh nhật</b> (theo Dương lịch)")
    with gr.Row(variant='panel'):
        with gr.Column(scale=3, min_width=min_width):
            gr_DD = gr.Number(label="Ngày", value=1, minimum=1, maximum=31, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            gr_MM = gr.Number(label="Tháng", value=1, minimum=1, maximum=12, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            gr_Y4 = gr.Number(label="Năm", value=2000, minimum=1888, maximum=2111, interactive=True)
        with gr.Column(scale=1, min_width=min_width):
            gr.Markdown("")
        with gr.Column(scale=3, min_width=min_width):
            gr_hh = gr.Number(label="Giờ", value=0, minimum=0, maximum=23, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            gr_mm = gr.Number(label="Phút", value=0, minimum=0, maximum=59, interactive=True)
        
    with gr.Row():
        with gr.Column(scale=1, min_width=min_width):
            u2ls_button = gr.Button(value="⇩ Convert", variant="primary")
        with gr.Column(scale=1, min_width=min_width):
            ls2u_button = gr.Button(value="⇧ Revert", variant="secondary")
        with gr.Column(scale=5, min_width=min_width):
            gr.Markdown("")

    gr.Markdown("")
    gr.Markdown("## <b>Sinh thần bát tự</b> (theo Âm Dương lịch)")
    with gr.Row(variant='panel'):
        with gr.Column(scale=3, min_width=min_width):
            ls_DD = gr.Number(label="Ngày", value=1, minimum=1, maximum=30, interactive=True)
            ls_Dh = gr.Dropdown(label="Can", choices=Heavenly_Stems, interactive=True)
            ls_De = gr.Dropdown(label="Chi", choices=Earthly_Branches, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            ls_MM = gr.Number(label="Tháng", value=1, minimum=1, maximum=12, interactive=True)
            ls_Mh = gr.Dropdown(label="Can", choices=Heavenly_Stems, interactive=True)
            ls_Me = gr.Dropdown(label="Chi", choices=Earthly_Branches, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            ls_Y4 = gr.Number(label="Năm", value=2000, minimum=765, maximum=2200, interactive=True)
            ls_Yh = gr.Dropdown(label="Can", choices=Heavenly_Stems, interactive=True)
            ls_Ye = gr.Dropdown(label="Chi", choices=Earthly_Branches, interactive=True)
        with gr.Column(scale=1, min_width=min_width):
            gr.Markdown("")
        with gr.Column(scale=3, min_width=min_width):
            ls_He = gr.Dropdown(label="Giờ", choices=Earthly_Branches, interactive=True)
            ls_Hh = gr.Dropdown(label="Can", choices=Heavenly_Stems, interactive=True)
        with gr.Column(scale=3, min_width=min_width):
            ls_Yy = gr.Dropdown(label="Âm Dương", choices=['Âm','Dương'], interactive=True)

    with gr.Row():
        with gr.Column(scale=1, min_width=min_width):
            read_button = gr.Button(value="☯︎ Read", variant="primary")
        with gr.Column(scale=6, min_width=min_width):
            gr.Markdown("")

    variant = 'compact'  # 'panel'
    style = dict(show_label=False, container=False, interactive=False)
    ststtyle = dict(choices=Stars_States, multiselect=True, interactive=False, min_width=min_width)
    
    gr.Markdown("")
    gr.Markdown("# 🔮 <b>Lá số Tử vi</b>")
    
    with gr.Blocks():
    
        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b11_ord = gr.Textbox(placeholder="Tỵ", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b11_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b11_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b11_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b11_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b11_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b11_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b11_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b11_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b11_data = [b11_ord, b11_plc, 
                        b11_main, b11_aux, b11_xtr, b11_ftn, b11_etn, 
                        b11_karMa, b11_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b12_ord = gr.Textbox(placeholder="Ngọ", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b12_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b12_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b12_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b12_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b12_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b12_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b12_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b12_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b12_data = [b12_ord, b12_plc, 
                        b12_main, b12_aux, b12_xtr, b12_ftn, b12_etn, 
                        b12_karMa, b12_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b13_ord = gr.Textbox(placeholder="Mùi", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b13_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b13_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b13_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b13_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b13_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b13_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b13_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b13_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b13_data = [b13_ord, b13_plc, 
                        b13_main, b13_aux, b13_xtr, b13_ftn, b13_etn, 
                        b13_karMa, b13_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b14_ord = gr.Textbox(placeholder="Thân", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b14_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b14_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b14_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b14_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b14_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b14_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b14_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b14_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b14_data = [b14_ord, b14_plc, 
                        b14_main, b14_aux, b14_xtr, b14_ftn, b14_etn, 
                        b14_karMa, b14_karma]

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b21_ord = gr.Textbox(placeholder="Thìn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b21_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b21_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b21_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b21_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b21_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b21_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b21_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b21_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b21_data = [b21_ord, b21_plc, 
                        b21_main, b21_aux, b21_xtr, b21_ftn, b21_etn, 
                        b21_karMa, b21_karma]

            with gr.Column(min_width=min_width):
                gr.Markdown("### Tháng:")
                disp_M = gr.Textbox(placeholder="Tháng:", **style)
                gr.Markdown("### Ngày:")
                disp_D = gr.Textbox(placeholder="Ngày:", **style)
                gr.Markdown("### Giờ:")
                disp_h = gr.Textbox(placeholder="Giờ:", **style)

            with gr.Column(min_width=min_width):
                gr.Markdown("### Mệnh chủ:")
                disp_dest_star = gr.Textbox(placeholder="Mệnh chủ:", **style)
                gr.Markdown("### Thân chủ:")
                disp_body_star = gr.Textbox(placeholder="Thân chủ:", **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b24_ord = gr.Textbox(placeholder="Dậu", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b24_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b24_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b24_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b24_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b24_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b24_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b24_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b24_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b24_data = [b24_ord, b24_plc, 
                        b24_main, b24_aux, b24_xtr, b24_ftn, b24_etn, 
                        b24_karMa, b24_karma]

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b31_ord = gr.Textbox(placeholder="Mão", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b31_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b31_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b31_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b31_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b31_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b31_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b31_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b31_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b31_data = [b31_ord, b31_plc, 
                        b31_main, b31_aux, b31_xtr, b31_ftn, b31_etn, 
                        b31_karMa, b31_karma]

            with gr.Column(min_width=min_width):
                gr.Markdown("### Mệnh:")
                disp_dest = gr.Textbox(placeholder="Mệnh:", **style)
                gr.Markdown("### Cục:")
                disp_sitt = gr.Textbox(placeholder="Cục:", **style)
                gr.Markdown("### Tương quan:")
                disp_corr = gr.Textbox(placeholder="Tương quan:", **style)

            with gr.Column(min_width=min_width):
                gr.Markdown("### Cung Mệnh:")
                disp_dstp = gr.Textbox(placeholder="Cung Mệnh:", **style)
                gr.Markdown("### Âm Dương:")
                disp_yygd = gr.Textbox(placeholder="Âm Dương:", **style)
                gr.Markdown("### Thuận nghịch:")
                disp_fvrv = gr.Textbox(placeholder="Thuận nghịch:", **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b34_ord = gr.Textbox(placeholder="Tuất", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b34_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b34_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b34_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b34_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b34_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b34_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b34_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b34_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b34_data = [b34_ord, b34_plc, 
                        b34_main, b34_aux, b34_xtr, b34_ftn, b34_etn, 
                        b34_karMa, b34_karma]

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b41_ord = gr.Textbox(placeholder="Dần", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b41_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b41_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b41_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b41_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b41_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b41_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b41_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b41_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b41_data = [b41_ord, b41_plc, 
                        b41_main, b41_aux, b41_xtr, b41_ftn, b41_etn, 
                        b41_karMa, b41_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b42_ord = gr.Textbox(placeholder="Sửu", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b42_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b42_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b42_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b42_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b42_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b42_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b42_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b42_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b42_data = [b42_ord, b42_plc, 
                        b42_main, b42_aux, b42_xtr, b42_ftn, b42_etn, 
                        b42_karMa, b42_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b43_ord = gr.Textbox(placeholder="Tý", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b43_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b43_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b43_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b43_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b43_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b43_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b43_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b43_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b43_data = [b43_ord, b43_plc, 
                        b43_main, b43_aux, b43_xtr, b43_ftn, b43_etn, 
                        b43_karMa, b43_karma]

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b44_ord = gr.Textbox(placeholder="Hợi", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b44_plc = gr.Textbox(placeholder="Cung", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                    with gr.Column(scale=5, min_width=min_width):
                        b44_main = gr.Dropdown(label="Chính tinh", **ststtyle)
                    with gr.Column(scale=1, min_width=min_width):
                        gr.Markdown("")
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b44_aux = gr.Dropdown(label="Phụ tinh", **ststtyle)
                with gr.Row():
                    with gr.Column(scale=1, min_width=min_width):
                        b44_xtr = gr.Textbox(placeholder="Thái Tuế", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b44_ftn = gr.Textbox(placeholder="Lộc tồn", text_align='right', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b44_etn = gr.Textbox(placeholder="Tràng Sinh", text_align='right', **style)
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b44_karMa = gr.Textbox(placeholder="Đại hạn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b44_karma = gr.Textbox(placeholder="Tiểu Hạn", text_align='right', **style)
            b44_data = [b44_ord, b44_plc, 
                        b44_main, b44_aux, b44_xtr, b44_ftn, b44_etn, 
                        b44_karMa, b44_karma]

    with gr.Row():
        with gr.Column(scale=1, min_width=min_width):
            read_button = gr.Button(value="🔎 Explain", variant="primary")
        with gr.Column(scale=6, min_width=min_width):
            gr.Markdown("")
    
    gr.Markdown("")
    gr.Markdown("# 𓍢ִ໋🀦  <b>Luận giải</b>")

    # Group data
    solar_dt_data = [gr_DD, gr_MM, gr_Y4, gr_hh, gr_mm]
    lunisol_dt_data = [ls_DD, ls_Dh, ls_De,
                       ls_MM, ls_Mh, ls_Me,
                       ls_Y4, ls_Yh, ls_Ye, ls_Yy, 
                              ls_Hh, ls_He, ]
    destiny_data = [disp_M, disp_D, disp_h, disp_yygd,
                    disp_dest, disp_sitt, disp_corr, 
                    disp_dstp, disp_fvrv]
    # Order Palaces by Earthlings (Ty)
    palaces_data = b43_data + b42_data + b41_data + b31_data + b21_data + b11_data + \
                   b12_data + b13_data + b14_data + b24_data + b34_data + b44_data

    # Callbacks
    u2ls_button.click(fn = find_ganzhi_of_time, inputs = solar_dt_data, 
                                               outputs = lunisol_dt_data)
    read_button.click(fn = read_the_destiny, inputs = lunisol_dt_data + [gr_hh, gr_mm, gender],
                                            outputs = destiny_data + palaces_data)


if __name__ == "__main__":
    gui.launch()


