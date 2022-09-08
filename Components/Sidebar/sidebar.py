import dash_bootstrap_components as dbc
from dash import html, dcc 
import pandas as pd

def sidebar():
    return dbc.Col(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.Span(
                                'Item 1: ',
                                style={
                                    "display":"inline",
                                    "color":"#4f2d7f",
                                }
                            ),
                    html.Div(
                        dbc.Button(
                            "Download",
                            color="dark",
                            outline=True,
                            id="item_1"
                        ),
                        style={
                            "borderRadius":"5px",
                            "backgroundColor":"white"
                        }
                    ),
                    dcc.Download(id="download_item1")
                        ],
                        style={
                            "display":"flex",
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