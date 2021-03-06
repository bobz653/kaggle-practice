#-*- coding:utf-8
""" my test file in the titanic data
Author : bob zhang 
Date : 18th 6 2016

"""

import sys
import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                             # Skip the fist line as it is a header
data=[]                                                     # Create a variable to hold the data

for row in csv_file_object:                 # Skip through each row in the csv file
    data.append(row)                        # adding each row to the data variable
data = np.array(data)                       # Then convert from a list to an array

fare_ceiling =40

data[data[0::,9].astype(np.float)>=fare_ceiling,9]=fare_ceiling -1.0

fare_bracket_size = 10
number_of_price_brackets = fare_ceiling / fare_bracket_size

number_of_classes =len(np.unique(data[0::,2]))

survival_table=np.zeros((2,number_of_classes,number_of_price_brackets))

for i in xrange(number_of_classes):
    for j in xrange(number_of_price_brackets):
        women_only_stats = data[                \
                                (data[0::,4]=='female') \
                                &(data[0::,2].astype(np.float)==i+1) \
                                &(data[0::,9].astype(np.float)>=j*fare_bracket_size) \
                                &(data[0::,9].astype(np.float)<(j+1)*fare_bracket_size) \
                                ,1]
        men_only_stats = data[                \
                                (data[0::,4]!='female') \
                                &(data[0::,2].astype(np.float)==i+1) \
                                &(data[0::,9].astype(np.float)>=j*fare_bracket_size) \
                                &(data[0::,9].astype(np.float)<(j+1)*fare_bracket_size) \
                                ,1]
        survival_table[0,i,j]=np.mean(women_only_stats.astype(np.float))#女人每种情况下活下来的均值
        survival_table[1,i,j] =np.mean(men_only_stats.astype(np.float))#男人每种情况下活下来的均值
        
survival_table[ survival_table != survival_table ] = 0.

survival_table[ survival_table < 0.5 ] = 0
survival_table[ survival_table >= 0.5 ] = 1 

test_file =open ('test.csv','rb')
test_file_object = csv.reader(test_file)
header = test_file_object .next()

prediction_file =open('mygenderclassmodel.csv','wb')
prediction_file_object = csv.writer(prediction_file)
bin_fare=0
for row in test_file_object :
    for x in xrange(number_of_price_brackets):
        try:
            row[8]=float(row[8])
        except:
            bin_fare = 3-float(row[1])
            break;
        if row[8]>fare_ceiling:
            bin_fare = number_of_price_brackets -1
            break;
        if row[8]>j*fare_bracket_size and row[8]<(j+1)*fare_bracket_size:
            bin_fare = j
            break;
    if row[3]=='female':
        prediction_file_object.writerow([row[0],"%d" %int(survival_table[0,float(row[1])-1,bin_fare])])
    else:
        prediction_file_object.writerow([row[0],"%d" %int(survival_table[1,float(row[1])-1,bin_fare])])

test_file.close()
prediction_file.close()

print survival_table
