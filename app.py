# from pickle import TRUE
# from sqlite3 import adapt, adapters
# import flask
# import logging
import pandas as pd
# import requests
# import sqlalchemy
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
from Components.Data_prep import NCAA_DF

### Tab Content Import ###
from Components.Component_one import component_one
from Components.Component_two import component_two
from Components.Component_three import component_three

### functions import ###
from Functions import functions
import base64
import io

import pandas as pd
import numpy as np
from sklearn import decomposition
from sklearn.neural_network import MLPClassifier

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
                sidebar.sidebar(),
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
@dash_app1.callback(
    Output("year1_output", "data"),
    Input("range_year1", "value"),
    suppress_callback_exceptions=True
)
def year1_input(year_1):
    return year_1

@dash_app1.callback(
    Output("year2_output", "data"),
    Input("range_year2", "value"),
    suppress_callback_exceptions=True
)
def year1_input(year_2):
    return year_2

@dash_app1.callback(
    Output("bracket_data", "data"),
    Input("year1_output", "data"),
    Input("year2_output", "data"),
    suppress_callback_exceptions=True
)
def creating_bracket(year1, year2):
    df = NCAA_DF.NCAA_DF(year1,year2)
    return  df.to_json()

@dash_app1.callback(
    Output("output-response", "children"),
    Input("team-1-selected", "value"),
    Input("team-2-selected", "value"),
    Input("bracket_data", "data"),
    Input("year2_output", "data"),
    suppress_callback_exceptions=True
)
def output_response(team1, team2, data, year2):
    # -------------------------
    # DATA PREPROCESSING
    # -------------------------
    data = pd.read_json(data)

    train_data = data[data['Year'] != (year2)]
    test_data = data[data['Year'] == (year2)]

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_1'] >= 1:
            train_data.at[index,'Round_1'] = updated_row

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_2'] >= 1:
            train_data.at[index,'Round_2'] = updated_row

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_3'] >= 1:
            train_data.at[index,'Round_3'] = updated_row

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_4'] >= 1:
            train_data.at[index,'Round_4'] = updated_row

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_5'] >= 1:
            train_data.at[index,'Round_5'] = updated_row

    for index, row in train_data.iterrows():
        updated_row = 1
        if row['Round_6'] >= 1:
            train_data.at[index,'Round_6'] = updated_row
            
    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_1'] >= 1:
            test_data.at[index,'Round_1'] = updated_row

    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_2'] >= 1:
            test_data.at[index,'Round_2'] = updated_row

    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_3'] >= 1:
            test_data.at[index,'Round_3'] = updated_row

    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_4'] >= 1:
            test_data.at[index,'Round_4'] = updated_row

    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_5'] >= 1:
            test_data.at[index,'Round_5'] = updated_row

    for index, row in test_data.iterrows():
        updated_row = 1
        if row['Round_6'] >= 1:
            test_data.at[index,'Round_6'] = updated_row
            
    train_data.dropna(inplace=True)
    test_data.dropna(inplace=True)


    train_data = train_data.set_index(['School', 'Year'])
    train_x = train_data.filter(['MP', 'FG', 'FGA', 'FG%', '2P', '2PA', '2P%', '3P','3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL','BLK', 'TOV', 'PF', 'PTS', 'SRS', 'SOS', 'W', 'L', 'W-L%', 'Con-W', 'Con-L','Home-W', 'Home-L', 'Away-W', 'Away-L', 'Team Points', 'Opp. Points','Offensive Rating', 'Defensive Rating', 'Con-W/L%', 'Home-W/L%','Away-W/L%'])
    school = test_data['School'].tolist()
    year = test_data['Year'].tolist()
    test_data = test_data.drop(['School', 'Year'], axis=1)
    test_x = test_data.filter(['MP', 'FG', 'FGA', 'FG%', '2P', '2PA', '2P%', '3P','3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL','BLK', 'TOV', 'PF', 'PTS', 'SRS', 'SOS', 'W', 'L', 'W-L%', 'Con-W', 'Con-L','Home-W', 'Home-L', 'Away-W', 'Away-L', 'Team Points', 'Opp. Points','Offensive Rating', 'Defensive Rating', 'Con-W/L%', 'Home-W/L%','Away-W/L%'])

    #I will make this a dependent variable to the model
    new_train_y1 = train_data.filter(["Round_1"])
    new_train_y2 = train_data.filter(["Round_2"])
    new_train_y3 = train_data.filter(["Round_3"])
    new_train_y4 = train_data.filter(["Round_4"])
    new_train_y5 = train_data.filter(["Round_5"])
    new_train_y6 = train_data.filter(["Round_6"])
    
    new_test_y1 = test_data.filter(["Round_1"])
    new_test_y2 = test_data.filter(["Round_2"])
    new_test_y3 = test_data.filter(["Round_3"])
    new_test_y4 = test_data.filter(["Round_4"])
    new_test_y5 = test_data.filter(["Round_5"])
    new_test_y6 = test_data.filter(["Round_6"])

    #Joining train dfs
    new_train_y = new_train_y1.join(new_train_y2)
    for i in range(3,7):
        exec("new_train_y = new_train_y.join(new_train_y%d)" % i)
        
    new_train_y['Full_Round'] = new_train_y.sum(axis=1)
    full_new_train_y = np.array(new_train_y['Full_Round'])

    #Joining test dfs
    new_test_y = new_test_y1.join(new_test_y2)
    for i in range(3,7):
        exec("new_test_y = new_test_y.join(new_test_y%d)" % i)
        
    new_test_y['Full_Round'] = new_test_y.sum(axis=1)
    full_new_test_y = np.array(new_test_y['Full_Round'])


    # apply Principal Component Analysis
    pca = decomposition.PCA(n_components = 10)
    pca.fit(train_x)
    X = pca.transform(train_x)
    pca1 = decomposition.PCA(n_components = 10)
    pca1.fit(test_x)
    X1 = pca.transform(test_x)

    # -------------------------
    # NEURAL NETWORK CREATION
    # -------------------------    
    classifier_nn = MLPClassifier(
        solver = 'adam',
        activation = 'relu',
        learning_rate = 'adaptive',
        alpha = 1
        )
    classifier_nn.fit(X, new_train_y1.values.ravel())

    y_pred_nn_prob = classifier_nn.predict_proba(X1)
    nn_pred = y_pred_nn_prob.tolist()
    nn_pred_df = []

    for i in nn_pred:
        nn_pred_df.append(i[1])
    test_data['Win_Prob'] = nn_pred_df
    test_data['School'] = school
    test_data['Year'] = year
    res = {school[i]: nn_pred_df[i] for i in range(len(school))}
    
    return f'The first team has a {res[team1]/(res[team1]+res[team2])} probability of winning the game, whereas the second team has a {res[team2]/(res[team1]+res[team2])} of winning the game'

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
    Input('tabs', 'value'),
    Input("bracket_data", "data"),
    Input("year2_output", "data")
)
def update_imp_graph(tab, data, year2):
    if tab == 't1':
        return component_one.component_one(data, year2)
    if tab == 't2':
        return component_two.component_two()
    if tab == 't3':
        return component_three.component_three()

if __name__ == '__main__':
    dash_app1.run_server(host='0.0.0.0', port=8081, debug=True, threaded=True)