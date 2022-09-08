from dash import dcc, html, dash_table
import dash_bootstrap_components as dbc

def tabs(content):
    name=['Team Prediction', 'Bracket Prediction', 'Model Performance']
    return dbc.Col(
        [
            dcc.Tabs(
                [
                    dcc.Tab(
                        label=name,
                        id=f't{index}',
                        value=f't{index}',
                        selected_style={'borderTop':'1px solid #4F2D7F'},
                    ) for name, index in zip(name, range(1,6))
                ],
            id = "tabs",
            value="t1"
            ),
            dbc.Row(
                content,
                id="header",
            ),
            html.Hr(
                style={
                    "border":"1px solid black",
                    "color":"black",
                    "opacity":"1",
                    "margin-bottom":"10px",
                    "margin":"0px 25px",
                }
            ),
            dcc.Loading(
                children=[
                    html.Div(
                        id="tab_content",
                        style={
                            "padding":"0px 25px",
                            "minHeight":"550px",
                        }
                    ),
                ],
                type="default",
                color="#0079c2",
            ),
        ],
        width=18,
        style={
            "padding-left":"0px",
            "padding-right":"0px",
            "height":"100%"
        },
        id="tab-container"
    )