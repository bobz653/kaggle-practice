#-*- coding:utf-8
""" my test file in the titanic data
Author : bob zhang 
Date : 18th 6 2016
"""

import pandas as pd
import sys
import csv as csv
import numpy as np
from sklearn.ensemble import RandomForestClassifier

train_df= pd.read_csv('train.csv',header =0 )

train_df['Gender'] = train_df['Sex'].map( {'female':0,'male':1} ).astype(int)

if len(train_df.Embarked[train_df.Embarked.isnull()]) >0:
    train_df.Embarked[train_df.Embarked.isnull()] = train_df.Embarked.dropna().mode().values

Ports = list(enumerate(np.unique(train_df['Embarked'])))
Ports_dict = { name:i for i,name in Ports }
train_df.Embarked = train_df.Embarked.map(lambda x:Ports_dict[x]).astype(int)

median_age = train_df['Age'].dropna().median()
if len(train_df.Age[train_df.Age.isnull()])>0:
    train_df.loc[ (train_df.Age.isnull()), 'Age'] = median_age

if len(train_df.Fare[ train_df.Fare.isnull() ]) > 0:
    print 'train fare null'
    median_fare = np.zeros(3)
    for f in range(0,3):                                              # loop 0 to 2
        median_fare[f] = train_df[ train_df.Pclass == f+1 ]['Fare'].dropna().median()
    for f in range(0,3):                                              # loop 0 to 2
        train_df.loc[ (train_df.Fare.isnull()) & (train_df.Pclass == f+1 ), 'Fare'] = median_fare[f]

        
train_df = train_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 

test_df = pd.read_csv('test.csv', header=0)        # Load the test file into a dataframe

test_df['Gender'] = test_df['Sex'].map( {'female': 0, 'male': 1} ).astype(int)

#Embarked from 'C', 'Q', 'S'
# All missing Embarked -> just make them embark from most common place
if len(test_df.Embarked[ test_df.Embarked.isnull() ]) > 0:
    test_df.Embarked[ test_df.Embarked.isnull() ] = test_df.Embarked.dropna().mode().values
# Again convert all Embarked strings to int
test_df.Embarked = test_df.Embarked.map( lambda x: Ports_dict[x]).astype(int)

median_age = test_df['Age'].dropna().median()
if len(test_df.Age[ test_df.Age.isnull() ]) > 0:
    test_df.loc[ (test_df.Age.isnull()), 'Age'] = median_age

    
if len(test_df.Fare[ test_df.Fare.isnull() ]) > 0:
    print 'hello'
    median_fare = np.zeros(3)
    for f in range(0,3):                                              # loop 0 to 2
        median_fare[f] = test_df[ test_df.Pclass == f+1 ]['Fare'].dropna().median()
    for f in range(0,3):                                              # loop 0 to 2
        test_df.loc[ (test_df.Fare.isnull()) & (test_df.Pclass == f+1 ), 'Fare'] = median_fare[f]

# Collect the test data's PassengerIds before dropping it
ids = test_df['PassengerId'].values
# Remove the Name column, Cabin, Ticket, and Sex (since I copied and filled it to Gender)
test_df = test_df.drop(['Name', 'Sex', 'Ticket', 'Cabin', 'PassengerId'], axis=1) 

# The data is now ready to go. So lets fit to the train, then predict to the test!
# Convert back to a numpy array
train_data = train_df.values
test_data = test_df.values

print 'Training...'
forest = RandomForestClassifier(n_estimators=100)
forest = forest.fit( train_data[0::,1::], train_data[0::,0] )

print 'Predicting...'
output = forest.predict(test_data).astype(int)


predictions_file = open("bobmyfirstforest.csv", "wb")
open_file_object = csv.writer(predictions_file)
open_file_object.writerow(["PassengerId","Survived"])
open_file_object.writerows(zip(ids, output))
predictions_file.close()
print 'Done.'





