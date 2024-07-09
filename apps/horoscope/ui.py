import os
import datetime

import numpy as np

import gradio as gr
from gradio_calendar import Calendar


# Load data
from .ganzhi import WeAcKn as WeAcKn_GanZhi

Heavenly_Stems   = WeAcKn_GanZhi['CAN']['Value'].values.tolist()
Earthly_Branches = WeAcKn_GanZhi['CHI']['Value'].values.tolist()


# Process data
from .ganzhi import find_ganzhi_of_time
from .destituation import determine_destiny_and_situation


def read_the_destiny(dd: int, dh: str, de: str,
                     mm: int, mh: str, me: str,
                     y4: int, yh: str, ye: str, yy: str,
            uh: int, um: int, hh: str, he: str, gd: str, ):

    hm = f"{uh:02d}:{um:02d}"
    yy_ = f"{yy} {gd}"

    # Địa bàn
    destiny, destiny_pos, \
        situation, \
        correlation, \
        favoreverse = determine_destiny_and_situation(yh=yh, ye=ye, yy=yy, mm=mm, he=he)

    # Thiên bàn

    return f"{mm} - {mh} {me}", \
           f"{dd} - {dh} {de}", \
           f"{hm} - {hh} {he}", \
           destiny, situation, correlation, \
           destiny_pos, yy_, favoreverse


# Define UI settings & layout
min_width = 25

with gr.Blocks(css=None, analytics_enabled=False) as gui:

    gr.Markdown("# Thông tin cá nhân")
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
            ls_Y4 = gr.Number(label="Năm", value=2000, minimum=1888, maximum=2111, interactive=True)
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
            read_button = gr.Button(value="🔮 Read ☯︎", variant="primary") # 🪬
        with gr.Column(scale=6, min_width=min_width):
            gr.Markdown("")

    variant = 'compact'  # 'panel'
    style = dict(show_label=False, container=False, interactive=False)
    with gr.Blocks():
        gr.Markdown("# <b>Lá số Tử vi</b>")

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b11_chi = gr.Textbox(placeholder="Tỵ", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b11_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b11_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b11_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b11_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b12_chi = gr.Textbox(placeholder="Ngọ", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b12_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b12_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b12_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b12_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b13_chi = gr.Textbox(placeholder="Mùi", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b13_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b13_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b13_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b13_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b14_chi = gr.Textbox(placeholder="Thân", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b14_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b14_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b14_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b14_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b21_chi = gr.Textbox(placeholder="Thìn", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b21_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b21_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b21_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b21_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

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
                        b24_chi = gr.Textbox(placeholder="Dậu", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b24_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b24_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b24_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b24_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b31_chi = gr.Textbox(placeholder="Mão", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b31_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b31_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b31_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b31_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

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
                        b34_chi = gr.Textbox(placeholder="Tuất", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b34_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b34_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b34_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b34_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

        with gr.Row(equal_height=True):

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b41_chi = gr.Textbox(placeholder="Dần", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b41_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b41_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b41_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b41_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b42_chi = gr.Textbox(placeholder="Sửu", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b42_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b42_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b42_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b42_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b43_chi = gr.Textbox(placeholder="Tý", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b43_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b43_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b43_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b43_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)

            with gr.Column(variant=variant, min_width=min_width):
                with gr.Row():
                    with gr.Column(scale=2, min_width=min_width):
                        b44_chi = gr.Textbox(placeholder="Hợi", text_align='left', **style)
                    with gr.Column(scale=3, min_width=min_width):
                        b44_plc = gr.Textbox(placeholder="Cung", text_align='left', **style)
                    with gr.Column(scale=1, min_width=min_width):
                        b44_age = gr.Textbox(placeholder="#", text_align='right', **style)
                with gr.Row():
                    with gr.Column(min_width=min_width):
                        b44_main = gr.Textbox(placeholder="Chính tinh", text_align='left', **style)
                    with gr.Column(min_width=min_width):
                        b44_aux = gr.Textbox(placeholder="Phụ tinh", text_align='left', **style)
                
    # Callbacks
    u2ls_button.click(fn=find_ganzhi_of_time, inputs=[gr_DD, gr_MM, gr_Y4, gr_hh, gr_mm], 
                                             outputs=[ls_DD, ls_Dh, ls_De,
                                                      ls_MM, ls_Mh, ls_Me,
                                                      ls_Y4, ls_Yh, ls_Ye, ls_Yy, 
                                                             ls_Hh, ls_He, ])
    read_button.click(fn=read_the_destiny, inputs=[ls_DD, ls_Dh, ls_De,
                                                   ls_MM, ls_Mh, ls_Me,
                                                   ls_Y4, ls_Yh, ls_Ye, ls_Yy, 
                                            gr_hh, gr_mm, ls_Hh, ls_He, gender, ],
                                          outputs=[disp_M, disp_D, disp_h,
                                                   disp_dest, disp_sitt, disp_corr, 
                                                   disp_dstp, disp_yygd, disp_fvrv, ])


if __name__ == "__main__":
    gui.launch()


