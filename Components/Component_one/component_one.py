from dash import html, dcc, dash_table
import pandas as pd
import numpy as np
from sklearn import decomposition
from sklearn.neural_network import MLPClassifier

def component_one(data, year2):
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
    return html.Div(
        [
            html.P('Please select the two teams playing against each other.'),
            dcc.Dropdown(
                test_data['School'],
                id='team-1-selected',
                style={
                    'max-width':'450px',
                    'margin':'5px'
                }),
            dcc.Dropdown(
                test_data['School'],
                id='team-2-selected',
                style={
                    'max-width':'450px',
                    'margin':'5px'
                }),
            html.P(id='output-response')
        ]
    )
