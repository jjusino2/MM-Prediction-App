import dash_bootstrap_components as dbc
from dash import html, dcc 
import pandas as pd
from datetime import date

def sidebar():
    current_year = date.today().year
    year1_list = [x for x in range(1939,current_year)]
    year2_list = [x for x in range(1939,(current_year+1))]
    return dbc.Col(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                'Select first year: ',
                                style={
                                    "display":"inline",
                                    "color":"#000000",
                                }
                            ),
                    html.Div(
                        dcc.Dropdown(
                            year1_list,
                            value=(current_year-5),
                            id="range_year1"
                        ),
                        style={
                            "borderRadius":"10px",
                            "backgroundColor":"white"
                        }
                    ),
                        ],
                        style={
                            "flexDirection":"row",
                            "justifyContent":"space-between",
                            "alignItems":"center",
                            "marginBottom":"1rem"
                        }
                    ),
                    html.Div(
                        [
                            html.Span(
                                'Select second year: ',
                                style={
                                    "display":"inline",
                                    "color":"#000000",
                                }
                            ),
                    html.Div(
                        dcc.Dropdown(
                            year2_list,
                            value=current_year,
                            id="range_year2"
                        ),
                        style={
                            "borderRadius":"10px",
                            "backgroundColor":"white"
                        }
                    ),
                        ],
                        style={
                            "flexDirection":"row",
                            "justifyContent":"space-between",
                            "alignItems":"center",
                            "marginBottom":"1rem"
                        }
                    ),
                    html.Div(
                        [
                            html.Div(
                                dbc.Button(
                                    x,
                                    color="dark",
                                    outline=True,
                                    id = x,
                                    type = "reset",
                                    style={
                                        "width":"100%"
                                    }
                                ),
                                    style={
                                        "backgroundColor":"white",
                                        "borderRadius":"5px",
                                        "width":"50%"
                                    }
                                ) for x in ["Reset", "Run"]
                        ],
                        className="d-md-flex gap-2"
                            ),
                    ]
            )
        ],
        width = 3,
        style={
            "padding":"30px 30px",
            "backgroundColor":"#f2f0ee",
            "overflowY":"auto",
            "border-right":"3px solid #333333"
        }
    )