import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import confusion_matrix
import pickle
import os
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.inspection import permutation_importance

# Directory
curDir = os.getcwd()

# Reading csv file
df = pd.read_csv('cleaned_earthquake.csv')

# Choosing columns
features = df[['magnitude', 'mmi', 'tsunami', 'dmin', 'gap', 'depth', 'nst', 'latitude', 'longitude']]
output = df['alert']
output, mapping = pd.factorize(output)

# Pre-model process
x_train, x_test, y_train, y_test = train_test_split(features,
                                                    output,
                                                    test_size=0.2,
                                                    random_state=41)

# # Model
nbmodel = GaussianNB()
nbmodel.fit(x_train, y_train)
y_pred = nbmodel.predict(x_test)
accuracy = accuracy_score(y_pred, y_test)
f1score = f1_score(y_test, y_pred, average='weighted')
cfmatrix = confusion_matrix(y_test, y_pred)
print('Accuracy:', accuracy)
print('f1 score:', f1score)

model_path = os.path.join(curDir, 'nbm.pickle')
with open(model_path, 'wb') as nb_pickle:
    pickle.dump(nbmodel, nb_pickle)
    nb_pickle.close()
    
model_path2 = os.path.join(curDir, 'outputnb.pickle')
with open(model_path2, 'wb') as outputnb_pickle:
    pickle.dump(mapping, outputnb_pickle)
    outputnb_pickle.close()

imp = permutation_importance(nbmodel, x_test, y_test)
fig, ax = plt.subplots() 
ax = sns.barplot(x=imp.importances_mean, y=features.columns) 
plt.title('Which features are the most important for species prediction?') 
plt.xlabel('Importance') 
plt.ylabel('Feature') 
plt.tight_layout() 
fig.savefig('feature_importance.png')

fig2, ax2 = plt.subplots()
ax2 = sns.heatmap(cfmatrix, annot=True, fmt='d', cmap='Blues', cbar=False)
fig2.savefig('confusion_matrix.png')