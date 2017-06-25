#-*- coding:utf-8
""" my test file in the titanic data
Author : bob zhang 
Date : 18th 6 2016

"""

import sys
import csv as csv
import numpy as np
import pandas as pd

csv_file_object = csv.reader(open('train.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                             # Skip the fist line as it is a header
data=[]                                                     # Create a variable to hold the data

for row in csv_file_object:                 # Skip through each row in the csv file
    data.append(row)                        # adding each row to the data variable
data = np.array(data)                       # Then convert from a list to an array

#print  data[0:5,5].astype(np.float)
#print type(data[0:15,5])

df = pd.read_csv('train.csv',header=0)
'''
print df.head(3)
print type(df)
print df.info()
print df.describe()

print df['Age'][0:10]
print df['Age'][0:10].mean()
print df['Age'].median()
'''
#df['Gender'] = df['Sex'] .map(lambda x:x[0].upper())
df['Gender'] = df['Sex'] .map({'female':0,'male':1}).astype(int)


#print df[ ['Sex', 'Pclass', 'Age'] ]

#print df[df['Age'] > 60][['Sex', 'Pclass', 'Age', 'Survived']]

#print df[df['Age'].isnull()][['Sex', 'Pclass', 'Age']]

median_age = np.zeros((2,3))
for i in range(0,2):
    for j in range(0,3):
        median_age[i,j] = df[(df['Gender']==i) & (df['Pclass']== j+1)]['Age'].dropna().median()
df['AgeFill'] =df['Age']
print median_age
print df.head()
print df[df['Age'].isnull()][['Gender','Pclass','Age','AgeFill']].head(10)
for i in range(0,2):
    for j in range(0,3):
        df.loc[(df.Age.isnull()) & (df.Gender ==i )& (df.Pclass==j+1),'AgeFill']=median_age[i,j]
df['AgeIsNull'] = pd.isnull(df.Age).astype(int)
print df.describe()
print df[df['Age'].isnull()][['Gender','Pclass','Age','AgeFill']].head(10)
sys.exit(0)
for i in range(1,4):
    print i,len(df[ (df['Sex'] == 'male') & (df['Pclass'] == i) ])


    
import pylab as P

#df['Age'].hist()
df['Age'].dropna().hist(bins=6, range=(0,80), alpha = .5) #bins 代表分多少类

P.show()