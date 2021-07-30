# -*- coding: utf-8 -*-
"""clothes desafio

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZnqdNs9C7pyCdNa5iOECvDpkZDnU_15n
"""

import math
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import drive
drive.mount('/content/drive')
import seaborn as sns

df = pd.read_csv('/content/drive/My Drive/kaggle desafios/clothes/final_test.csv')

df.head(10)

df.isna().sum()

df.shape

sns.pairplot(data=df, hue='size', height=7)
plt.show()

"""## Removendo outliers usando zscore, de acordo com https://towardsdatascience.com/ways-to-detect-and-remove-the-outliers-404d16608dba"""

dfs = []
sizes = []
for size_type in df['size'].unique():
    print('size type:',size_type)
    sizes.append(size_type)
    ndf = df[['age','height','weight']][df['size'] == size_type]
    zscore = ((ndf - ndf.mean())/ndf.std())
    #print(zscore)
    dfs.append(zscore)

for i in range(len(dfs)):
    print(sizes[i])
    dfs[i]['age'] = dfs[i]['age'][(dfs[i]['age']>-3) & (dfs[i]['age']<3)]
    dfs[i]['height'] = dfs[i]['height'][(dfs[i]['height']>-3) & (dfs[i]['height']<3)]
    dfs[i]['weight'] = dfs[i]['weight'][(dfs[i]['weight']>-3) & (dfs[i]['weight']<3)]
    dfs[i]['size'] = sizes[i]

"""Eu decidi deletar valores NaN porque a quantidade não é muito grande em relação ao total dos dados, mas uma opção seria preencher com a media com base no "size" que esta classificado o valor faltante"""

df = pd.concat(dfs)

df.dropna(inplace = True)

from sklearn.preprocessing import LabelEncoder
from sklearn.neural_network import MLPClassifier

from sklearn.tree import DecisionTreeClassifier

from sklearn.model_selection import train_test_split

"""transformando os tamanhos em dados numericos e criando novas features"""

labelEncoder = LabelEncoder()

size_enconder = labelEncoder.fit_transform(df['size'])

df['size_enc'] = size_enconder

df['imc'] = df['weight'] / (df['height']/100 * df['height']/100)

df['weight2'] = df['weight'] * df['weight']

"""separando o df de treino"""

df_train = df.copy()

df_train.isna().sum()

df_train.drop(columns= ['size'], inplace = True, axis = 1)

df_labels = df_train['size_enc']
df_train.drop(columns = ['size_enc'], inplace = True, axis = 1)

x_train, x_test, y_train, y_test = train_test_split(df_train, df_labels, test_size=0.2, random_state=0)

rede_neural = MLPClassifier(max_iter = 1000, 
                            verbose = True,
                            tol = 0.00001,
                            solver = 'adam',
                            activation = 'relu',
                            hidden_layer_sizes = (6,6))

from sklearn.metrics import accuracy_score, classification_report

rede_neural = MLPClassifier(max_iter = 1000, 
                        tol = 0.00001,
                        solver = 'adam',
                        activation = 'tanh',
                        hidden_layer_sizes = (20,20))

rede_neural.fit(x_train, y_train)
prev = rede_neural.predict(x_test)
print(accuracy_score(y_test, prev))

for s in ['adam', 'sgd']:
  for act in ['identity', 'logistic', 'tanh', 'relu']:
    
    print('\n ----------------\n ',s)
    print(act)
    rede_neural = MLPClassifier(max_iter = 1000, 
                            tol = 0.00001,
                            solver = s,
                            activation = act,
                            hidden_layer_sizes = (5,5))
    rede_neural.fit(x_train, y_train)
    prev = rede_neural.predict(x_test)
    print(accuracy_score(y_test, prev))
    #print(classification_report(y_test, prev))

"""#Random Forest"""

from sklearn.ensemble import RandomForestClassifier

for n in range(20, 300, 20):
  RFC = RandomForestClassifier(n_estimators= n, criterion = 'entropy')
  RFC.fit(x_train, y_train)
  prev = RFC.predict(x_test)
  ac = accuracy_score(y_test, prev)
  print(n, ac)