#Import scikit-learn dataset library
from sklearn import datasets
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn import metrics

fname=[2,3,5]
res=[]
for i in range(3):
    #print i
    x = pd.read_csv("class"+str(fname[i])+".txt")
    a = np.array(x)
    y=a[:,7]
    data=a[:,0:7]
    ### Import train_test_split function
    ## Split dataset into training set and test set
    X_train, X_test, y_train, y_test = train_test_split(data, y,test_size=0.3,random_state=0) # 70% training and 30% test
    ###Create a svm Classifier
    clf = svm.SVC(kernel='linear') # Linear Kernel

    #Train the model using the training sets
    clf.fit(X_train, y_train)
    ##
    #Predict the response for test dataset
    y_pred = clf.predict(X_test)

    #Import scikit-learn metrics module for accuracy calculation
    ### Model Accuracy: how often is the classifier correct?
    res.append(float("{0:.2f}".format(metrics.accuracy_score(y_test, y_pred))))
    print("Accuracy of Class "+str(fname[i])+":",res[i])


###### Driver Fatigue Classification Result #######

fmax=np.max(res)
idx=res.index(fmax)
#print idx
print("Driver Fatigue Level from the Analysis is Classification Mode Class %s"%fname[idx])
