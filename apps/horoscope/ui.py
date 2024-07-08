from pathlib import Path

import os
import datetime

import random
import numpy as np
import pandas as pd

import gradio as gr
from gradio_calendar import Calendar


wkdir = Path(__file__).parents[0]
print(wkdir)

CAN = pd.read_csv(wkdir / "WeAcKn/Can.csv")
CHI = pd.read_csv(wkdir / "WeAcKn/Chi.csv")


with gr.Blocks(css=None, analytics_enabled=False) as gui:

    gr.Markdown("# Thông tin cá nhân")

    with gr.Row():
        name = gr.Textbox(label="Họ tên", placeholder="Họ tên đầy đủ")
        gender = gr.Dropdown(label="Giới tính", choices=['Nam','Nữ'], value="Nam", interactive=True)

    with gr.Row(equal_height=True):

        with gr.Column(scale=3):
            gr.Markdown("## <b>Sinh thần bát tự</b> (theo lịch Gregory)")
            with gr.Row():
                gr_D = gr.Dropdown(label="Ngày", choices=list(range(1, 32)), interactive=True)
                gr_M = gr.Dropdown(label="Tháng", choices=list(range(1, 13)), interactive=True)
                gr_Y = gr.Number(label="Năm", value=2000, interactive=True)

        with gr.Column(scale=4):
            gr.Markdown("## <b>Sinh thần bát tự</b> (theo Âm Dương lịch)")
            with gr.Row():
                ls_D = gr.Dropdown(label="Ngày", choices=list(range(1, 32)), interactive=True)
                ls_M = gr.Dropdown(label="Tháng", choices=list(range(1, 14)), interactive=True)
                ls_Y_Can = gr.Dropdown(label="Năm (Can)", choices=CAN['Value'].values.tolist(), interactive=True)
                ls_Y_Chi = gr.Dropdown(label="Năm (Chi)", choices=CHI['Value'].values.tolist(), interactive=True)

    with gr.Blocks():
        gr.Markdown("# <b>Lá số Tử vi</b>")
        min_width = 10

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


# def is_weekday(date: datetime.datetime):
#     return date.weekday() < 5


# gui = gr.Interface(is_weekday, 
#     [Calendar(type="datetime", label="Select a date", info="Click the calendar icon to bring up the calendar.")], 
#     gr.Label(label="Is it a weekday?"),
#     examples=["2023-01-01", "2023-12-11"],
#     cache_examples=True,
#     title="Is it a weekday?")


if __name__ == "__main__":
    gui.launch()


