import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
import pickle
import os

# Directory
curDir = os.getcwd()

# Reading csv file
df = pd.read_csv('cleaned_earthquake.csv')

# Choosing columns
features = df[['depth', 'longitude', 'latitude', 'nst', 'magnitude']]
output = df['alert']

# Pre-model process
x_train, x_test, y_train, y_test = train_test_split(features,
                                                    output,
                                                    test_size= 0.2,
                                                    random_state=42)

# Model
nbmodel = GaussianNB()
nbmodel.fit(x_train, y_train)
y_pred = nbmodel.predict(x_test)
accuracy = accuracy_score(y_pred, y_test)
print(accuracy)

model_path = os.path.join(curDir, 'nbm.pickle')
with open(model_path, 'wb') as nb_pickle:
    pickle.dump(nbmodel, nb_pickle)
    nb_pickle.close()
    
model_path2 = os.path.join(curDir, 'outputnb.pickle')
with open(model_path2, 'wb') as outputnb_pickle:
    pickle.dump(output, outputnb_pickle)
    outputnb_pickle.close()