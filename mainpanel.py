from shiny import reactive, req
from shiny.express import module, render, ui

import numpy as np
import seaborn as sns
import statsmodels.formula.api as smf
from stargazer.stargazer import Stargazer

import wooldridge
import woo


@module
def panel_a(input, output, session):

    ui.input_select("data", "Data", woo.datasets)


    @reactive.calc
    def name():
        return input.data()

    @reactive.calc
    def df():
        return wooldridge.data(name())
    
    @reactive.calc
    def dataset():
        return woo.info(name())


    with ui.navset_card_pill(id="tab"):  

        # Tab 1: Data Description 
        with ui.nav_panel("Description"):

            @render.express
            def description():
                ui.h3(name())
                ui.p(dataset()['src'])
                ui.p(f"nvars={dataset()['nvars']}, nobs={dataset()['nobs']}")
            
            @render.data_frame
            def variable_definition():
                return dataset()["vars"]

        # Tab 2: View Data
        with ui.nav_panel("View"):
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
                        return dataset()['vars']

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

