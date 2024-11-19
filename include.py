from shiny import reactive, req
from shiny.express import module, render, ui


@module
def markdown(input, output, session, path):
    with open(path) as f:
        md = f.read()

    ui.markdown(md)