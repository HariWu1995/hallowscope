import gradio as gr


# Define styles
css = """
.gradio-container {width: 95% !important}
"""

# Define texts
title = r"""
<h1 align="center">HallowScope</h1>
"""

description = r"""
<b>Gradio demo</b> for <a href='https://github.com/HariWu1995/hallowscope' target='_blank'><b> HallowScope </b></a>.<br>
"""

tips = r"""
### Usage tips of Face Detection
1. If you're not satisfied, ..."
2. If you feel that ...
"""


if __name__ == "__main__":

    from apps.horoscope.ui import gui as gui_hs

    tabs = [gui_hs]
    names = ["Horoscope"]

    with gr.Blocks(css=css, analytics_enabled=False) as demo:
        
        # Header
        gr.Markdown(title)
        gr.Markdown(description)

        # Body    
        gr.TabbedInterface(interface_list=tabs, tab_names=names)

    demo.launch(share=False)

