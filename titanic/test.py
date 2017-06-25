""" my test file in the titanic data
Author : bob zhang 
Date : 18th 6 2016

"""


import csv as csv
import numpy as np

csv_file_object = csv.reader(open('train.csv', 'rb'))       # Load in the csv file
header = csv_file_object.next()                             # Skip the fist line as it is a header
data=[]                                                     # Create a variable to hold the data

for row in csv_file_object:                 # Skip through each row in the csv file
    data.append(row)                        # adding each row to the data variable
data = np.array(data)                       # Then convert from a list to an array

numbmer_passenger = np.size(data[0::,1].astype(np.float))
numbmer_survived =  np.sum(data[0::,1].astype(np.float))
proportion_survivors = numbmer_survived/numbmer_passenger
print '{0:.2}'.format(proportion_survivors)

women_only_stats = data[0::,4] =='female'
men_only_stats = data[0::,4] !='female'
print type(women_only_stats)

women_onboard = data[women_only_stats,1].astype(np.float)
men_onboard = data[men_only_stats,1].astype(np.float)

proportion_women_survived=\
    np.sum(women_onboard) / np.size(women_onboard)
proportion_men_survived=\
    np.sum(men_onboard) / np.size(men_onboard)

print 'Proportion of women who survived is %s' % proportion_women_survived
print 'Proportion of men who survived is %s' % proportion_men_survived

test_file =open('test.csv','rb')
test_file_object = csv.reader(test_file)
header=test_file_object.next()

prediction_file  = open('mygenderbasedmodel.csv','wb')
prediction_file_object = csv.writer(prediction_file)
prediction_file_object.writerow(['PassengerId','Survived'])
for row in test_file_object:
    if row[3] == 'female':
        prediction_file_object.writerow([row[0],'1'])
    else:
        prediction_file_object.writerow([row[0],'0'])
test_file.close()
prediction_file.close()
