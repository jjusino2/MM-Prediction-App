import dash_bootstrap_components as dbc
from dash import html, dcc

def navbar(img_path):
    return dbc.Navbar(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.A(
                            dbc.NavbarBrand(
                                [
                                    html.Img(
                                        src=img_path,
                                        height="55px",
                                        style={
                                            "margin-left":"1rem",
                                            "margin-right":".5rem",
                                            "maxWidth":"4vw",
                                            "display":"inline-block",
                                            "width":"100%",
                                            "height":"auto"
                                        }
                                    ),
                                    html.Span(
                                        [
                                            html.Strong(
                                                "| March Madness Prediction Tool",
                                                style={"fontSize":"min(2vw, 2rem)"}
                                            )
                                        ],
                                        style={
                                            "display":"inline-block",
                                            "verticalAlign":"middle"
                                        }
                                    ),
                                ],
                                style={
                                    "color":"#000000",
                                    "font-family":"Verdana",
                                    "pointer-events":"none"
                                }
                            ),
                            id="home_button"
                        ),
                        style={
                            "flex":"1"
                        }
                    ),
                ],
                className="g-0",
                style={
                    "width":"100%",
                }
            )
        ],
        color="#FDFDFD",
        style={
            "padding-left":"0px",
            "border-bottom":"3px solid #000000",
            "height":"9%"
        }
    )