import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
from shiny import reactive, req
from shiny.express import input, render, ui
import wooldridge
from stargazer.stargazer import Stargazer

from woo import datasets, describe, info

ui.page_opts(
    title="Wooldridge datasets",
)

ui.p(ui.a("https://pypi.org/project/wooldridge/", href="https://pypi.org/project/wooldridge/", target="_blank"))

ui.input_select("data", "Data", datasets)


@reactive.calc
def name():
    return input.data()

@reactive.calc
def df():
    return wooldridge.data(name())


with ui.navset_card_pill(id="tab"):  

    # Tab 1: Data Description 
    with ui.nav_panel("Description"):
        @render.express
        def description():
            ui.h3(name())
            ui.pre(describe(name()))

    # Tab 2: DataFrame 
    with ui.nav_panel("Data"):
        @render.data_frame
        def data_frame():
            return df()

    # Tab 3: Plot
    with ui.nav_panel("Plot"):

        with ui.layout_sidebar():

            with ui.sidebar():
                ui.input_select("x", "X", [])
                ui.input_select("y", "Y", [])
            
            @reactive.effect
            @reactive.event(df)
            def update_column_list():
                ui.update_select("x", choices=list(df().columns))
                ui.update_select("y", choices=list(df().columns))

            @render.plot
            def plot():
                req(input.x, input.y)
                return sns.relplot(x=input.x(), y=input.y(), data=df())


    # Tab 4: Regression with statsmodels
    with ui.nav_panel("Regression"):
        
        with ui.layout_columns(col_widths=(4, 8)):
            
            with ui.card():

                ui.p("Use ", ui.a("R-style formula", href="https://www.statsmodels.org/stable/examples/notebooks/generated/formulas.html",
                                  target="_blank"), 
                     " to specify the regression model.")
                
                ui.input_text("formula1", "Model (1)", width="100%")
                ui.input_text("formula2", "Model (2)", width="100%")

                @render.data_frame
                def variables():
                    return info(name())

            with ui.card():
                
                @render.express
                def result():
                    _ = req(len(input.formula1()) > 0 or len(input.formula2()) > 0)

                    est = []
                    if len(input.formula1()) > 0:
                        est.append(smf.ols(formula=input.formula1(), data=df()).fit())
                    
                    if len(input.formula2()) > 0:
                        est.append(smf.ols(formula=input.formula2(), data=df()).fit())

                    Stargazer(est)


@reactive.effect
@reactive.event(input.data)
def clear_formula():
    ui.update_text("formula1", value="")
    ui.update_text("formula2", value="")

