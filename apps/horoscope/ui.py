import os
import datetime

import numpy as np

import gradio as gr
from gradio_calendar import Calendar


# Load data


# Process data


# Define UI settings & layout
min_width = 25

with gr.Blocks(css=None, analytics_enabled=False) as gui:

    gr.Markdown("# Thông tin cá nhân")

    with gr.Row():

        with gr.Column(scale=3, variant='panel', min_width=min_width):
            name = gr.Textbox(label="Họ tên", placeholder="Họ tên đầy đủ")

        with gr.Column(scale=1, variant='panel', min_width=min_width):
            gender = gr.Dropdown(label="Giới tính", choices=['Nam','Nữ'], value="Nam", interactive=True)

    with gr.Row(equal_height=True):

        with gr.Column(scale=1, variant='panel', min_width=min_width):
            gr.Markdown("## <b>Sinh nhật</b> (theo lịch Gregory / Universal)")
            with gr.Row():
                gr_DD = gr.Number(label="Ngày", value=1, minimum=1, maximum=31, interactive=True)
                gr_MM = gr.Number(label="Tháng", value=1, minimum=1, maximum=12, interactive=True)
                gr_YYYY = gr.Number(label="Năm", value=2000, interactive=True)
            with gr.Row():
                gr_hh = gr.Number(label="Giờ", value=0, minimum=0, maximum=23, interactive=True)
                gr_mm = gr.Number(label="Phút", value=0, minimum=0, maximum=59, interactive=True)
                g2ls_button = gr.Button(value="Convert", variant="primary", scale=1)

        with gr.Column(scale=1, variant='panel', min_width=min_width):
            gr.Markdown("## <b>Sinh thần bát tự</b> (theo Âm Dương lịch)")
            with gr.Row():
                ls_DD = gr.Number(label="Ngày", value=1, minimum=1, maximum=30, interactive=True)
                ls_MM = gr.Number(label="Tháng", value=1, minimum=1, maximum=12, interactive=True)
                ls_Y_Can = gr.Dropdown(label="Năm (Can)", choices=CAN['Value'].values.tolist(), interactive=True)
                ls_Y_Chi = gr.Dropdown(label="Năm (Chi)", choices=CHI['Value'].values.tolist(), interactive=True)

    with gr.Blocks():
        gr.Markdown("# <b>Lá số Tử vi</b>")

        with gr.Row(equal_height=True):

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B11")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B12")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B13")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B14")

        with gr.Row(equal_height=True):

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B21")

            with gr.Column(min_width=min_width):
                gr.Markdown("B22")

            with gr.Column(min_width=min_width):
                gr.Markdown("B23")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B24")

        with gr.Row(equal_height=True):

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B31")

            with gr.Column(min_width=min_width):
                gr.Markdown("B32")

            with gr.Column(min_width=min_width):
                gr.Markdown("B33")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B34")

        with gr.Row(equal_height=True):

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B41")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B42")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B43")

            with gr.Column(variant='panel', min_width=min_width):
                gr.Markdown("B44")
                
    # Callbacks
    # g2ls_button.click(fn=run_detection, inputs=[img_det_in, detector], outputs=img_det_out)


if __name__ == "__main__":
    gui.launch()


