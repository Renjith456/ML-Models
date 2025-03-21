# -*- coding: utf-8 -*-
"""mlmodel_titanic

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12jpXHxB_Cvl5u7Neg6BMDvfLejdXdjtT
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

df=sns.load_dataset('titanic')
print(df)

df.head()
df.tail()
df.sample(5)
df.shape
df.isnull()
df.isnull().sum()
df.value_counts('survived')
df.groupby('survived').mean(numeric_only=True)
df.count()
df.describe()#all the mean,max,min,standard deviations,etcc..in a single function

df.dtypes

from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='most_frequent')
df['age'] = imputer.fit_transform(df[['age']])

df.isnull().sum()

from sklearn.preprocessing import LabelEncoder
label_enc = LabelEncoder()
df['deck'] = label_enc.fit_transform(df['deck'])
df['embark_town'] = label_enc.fit_transform(df['embark_town'])
df['embarked'] = label_enc.fit_transform(df['embarked'])

df.isnull().sum()

features = ['pclass', 'sex', 'age', 'sibsp', 'parch', 'fare', 'embarked','class','who','adult_male','deck','embark_town','alive','alone']
target = 'survived'

# Create a ColumnTransformer to apply different preprocessing to different columns
numeric_features = ['age', 'fare']
categorical_features = ['pclass', 'sex', 'embarked', 'class', 'who', 'adult_male', 'deck', 'embark_town', 'alive', 'alone', 'sibsp', 'parch'] # Include other categorical features

numeric_transformer=Pipeline(steps=[
    ('imputer',SimpleImputer(strategy='median')),
    ('scaler',StandardScaler())
])
categorical_transformer=Pipeline(steps=[
    ('imputer',SimpleImputer(strategy='most_frequent')),
    ('onehot',OneHotEncoder(handle_unknown='ignore'))
])

preprocessor=ColumnTransformer(
    transformers=[
        ('num',numeric_transformer,numeric_features),
        ('cat',categorical_transformer,categorical_features)
    ])

# Create a pipeline that includes preprocessing and the model
pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression())
])

from sklearn.model_selection import train_test_split
X= df[features]
y = df[target]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_train[['age', 'fare']] = scaler.fit_transform(X_train[['age', 'fare']])
X_test[['age', 'fare']] = scaler.transform(X_test[['age', 'fare']])

# Fit the pipeline to the training data
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)

# Evaluate model
from sklearn.metrics import accuracy_score, classification_report
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.4f}')
print(classification_report(y_test, y_pred))