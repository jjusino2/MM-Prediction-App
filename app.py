from pickle import TRUE
from sqlite3 import adapt, adapters
import flask
import logging
import pandas as pd
import requests
import sqlalchemy
import dash

from dash import Dash, callback_context, html, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from plotly.validator_cache import ValidatorCache

from Components import Navbar
#https://pythonhosted.org/Flask-Session

### Components Import ###
from Components.Tabs import tabs
from Components.Navbar import navbar
from Components.Sidebar import sidebar

### Tab Content Import ###
from Components.Component_one import component_one
from Components.Component_two import component_two
from Components.Component_three import component_three

### functions import ###
from Functions import functions
import base64
import io

### URL ###
REPLACE_SPACE_WITH_UNDERSCORE = True
url_base_pathname = "/dashapp/"

### INSTANTIATE APP ###
dash_app1 = dash.Dash(
    __name__,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        {
            'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
            'rel': 'stylesheet',
            'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
            'crossorigin': 'anonymous'
        }
    ],
    title='March Madness App',
    meta_tags=[{'name':'viewpoint',
                'content':'width=device-width, initial-scale=1.0'}]
    )
server = dash_app1.server
################

Tabs = tabs.tabs(None)
Navbar = navbar.navbar(dash_app1.get_asset_url('Browser MM Logo.png'))

###################
#### APP LAYOUT ###
###################
dash_app1.layout = dbc.Container(
    children=[
        Navbar,
        dbc.Row(
            [
                #sidebar.sidebar(),
                Tabs,
            ],
            style = {
                "min-height":"91%"
            }
        )
    ],
    fluid=True,
    style={
        "position":"fixed",
        "box-sizing":"border-box",
        "overflowX":"hidden",
        "height":"100%",
        "padding-left":"0px",
        "padding-right":"0px",
        "font-family":"Verdana"
    }
)

###########
###########

########################
#### APP CALLBACKS #####
########################

### HEADER CALLBACK ###
@dash_app1.callback(
    Output("header", "children"),
    Input("tabs", "value"),
)
def update_header_content(tab):
    name = ['Team Prediction', 'Bracket Prediction', 'Model Performance']
    tab_names = [f"{x}" for x in name]
    title = tab_names[int(tab[-1])-1]

    output = [
        dbc.Col(
            [
                html.H3(
                    title,
                    style={
                        "margin-top":"1.5rem",
                        "margin-left":"1.75rem",
                        "margin-bottom":"1rem",
                        "display":"inline-block"
                    }
                ),
                html.Div(
                        style={
                        "backgroundColor":"white",
                        "borderRadius":"5px",
                        "display":"inline-block",
                        "margin-left":".75rem",
                        "position":"relative",
                        "bottom":".3rem",
                }
                )
            ],
            id="tab-title"
        )
    ]
    return output

### COMPONENTS CALLBACKS ###

#Pending to make up these tabs

### NAVBRAND CALLBACKS ###
@dash_app1.callback(
    Output("tabs", "value"),
    Input("home_button", "n_clicks")
)
def navbrand_callback(n_clicks):
    context = callback_context.triggered[0]["prop_id"].split(".")[0]
    if context == 'home_button':
        return 't1'
    return 't1'

### CENTRAL CALLBACK ###
@dash_app1.callback(
    Output('tab_content', 'children'),
    Input('tabs', 'value')
)
def update_imp_graph(tab):
    if tab == 't1':
        return component_one.component_one()
    if tab == 't2':
        return component_two.component_two()
    if tab == 't3':
        return component_three.component_three()

if __name__ == '__main__':
    dash_app1.run_server(host='0.0.0.0', port=8081, debug=True, threaded=True)