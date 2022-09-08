from Components.Data_prep import NCAA_DF
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle
from sklearn import decomposition
from sklearn.model_selection import GridSearchCV
from keras.wrappers.scikit_learn import KerasClassifier

# -------------------------
# DATA PREPROCESSING
# -------------------------

df = NCAA_DF.NCAA_DF()

train_data = df[df['Year'] != 2021]
test_data = df[df['Year'] == 2021]

train_data.set_index(['School', 'Year'])
train_x = train_data.filter(['MP', 'FG', 'FGA', 'FG%', '2P', '2PA', '2P%', '3P','3PA', '3P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL','BLK', 'TOV', 'PF', 'PTS', 'SRS', 'SOS', 'W', 'L', 'W-L%', 'Con-W', 'Con-L','Home-W', 'Home-L', 'Away-W', 'Away-L', 'Team Points', 'Opp. Points','Offensive Rating', 'Defensive Rating', 'Con-W/L%', 'Home-W/L%','Away-W/L%'])
#I will make this a dependent variable to the model
train_y1 = train_data.filter(['Round_1'])
train_y2 = train_data.filter(['Round_2'])
train_y3 = train_data.filter(['Round_3'])
train_y4 = train_data.filter(['Round_4'])
train_y5 = train_data.filter(['Round_5'])
train_y6 = train_data.filter(['Round_6'])

# apply Principal Component Analysis
pca = decomposition.PCA(n_components = 10)
pca.fit(train_x)
X = pca.transform(train_x)

# create a train-test split with ratio 15:85
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, train_y1, test_size = 0.20)

# scale the training and testing data
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# save the scaler for future use
scalerfile = 'scaler.save'
pickle.dump(sc, open(scalerfile, 'wb'))

# -------------------------
# NEURAL NETWORK CREATION
# -------------------------
print("Training Neural Network model...")
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras import optimizers

# create function to build classifier
def build_classifier(optimizer = 'adam'):
    classifier_nn = Sequential()
    classifier_nn.add(Dense(50, input_dim = X_train.shape[1], 
                    kernel_initializer = 'random_uniform', 
                    activation = 'sigmoid'))
    classifier_nn.add(Dropout(0.2))
    classifier_nn.add(Dense(100, activation = 'relu'))
    classifier_nn.add(Dropout(0.5))
    classifier_nn.add(Dense(100, activation = 'relu'))
    classifier_nn.add(Dropout(0.5))
    classifier_nn.add(Dense(25, activation = 'relu'))
    classifier_nn.add(Dropout(0.2))
    classifier_nn.add(Dense(1, kernel_initializer = 'normal', activation = 'sigmoid'))
    classifier_nn.compile(loss = 'binary_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
    return classifier_nn

# convert to sklearn-readable model
classifier_nn = KerasClassifier(build_fn = build_classifier)

# declare search values
batch_size = [5, 20, 50]
epochs = [3, 5, 7]
optimizers = ['adam', 'rmsprop']

# create grid for gridsearch and perform gridsearch
grid = {'epochs': epochs,
        'batch_size': batch_size,
        'optimizer': optimizers}
validator = GridSearchCV(classifier_nn,
                         param_grid = grid,
                         scoring = 'accuracy',
                         n_jobs = 1)
validator.fit(X_train, y_train)

# get the best model from the gridsearch
print('The parameters of the best Neural Network model are: ')
print(validator.best_params_)
classifier_nn = validator.best_estimator_.model

# make predictions using the model
y_pred = classifier_nn.predict(X_test)
y_pred = np.where(y_pred > 0.5, 1, 0)