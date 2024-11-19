from functools import partial
from pathlib import Path

from shiny import reactive, req
from shiny.ui import page_navbar
from shiny.express import input, render, ui

from mainpanel import panel_a
from include import markdown

ui.page_opts(
    title="Wooldridge datasets",  
    page_fn=partial(page_navbar, id="page"),  
)

with ui.nav_panel("Playground"):  
    panel_a("main")

with ui.nav_panel("Documentation"): 
    markdown("documentation", Path(__file__).parent / "static" / "readme.md")
