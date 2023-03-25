# importing libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from sklearn.utils.validation import column_or_1d
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler

rand_state=1000

# read in the data
df = pd.read_csv("/content/full_data_flightdelay.csv")

df_subset = df[["MONTH","DAY_OF_WEEK","DEP_DEL15","DEP_TIME_BLK","CONCURRENT_FLIGHTS","NUMBER_OF_SEATS","CARRIER_NAME","DEPARTING_AIRPORT","PRCP","SNOW","TMAX","AWND"]]
df_subset.head()

value_counts = df_subset["DEP_TIME_BLK"].value_counts().sort_index(ascending=True)
# Create a dictionary to map each unique value to a unique number
value_to_num = {value: i for i, value in enumerate(value_counts.index)}
# Create a new column in the DataFrame containing the unique number for each value
df_subset["DEP_TIME_BLK_int_label"] = df_subset["DEP_TIME_BLK"].map(value_to_num)

#looking at the "Carrier Name" for each Airline, We want to use this as a feature but we have to convert it from strings to an int
value_counts = df_subset["CARRIER_NAME"].value_counts().sort_index(ascending=True)

# taking the unique values from "Carrier Name" an assigning a value to them.
# Create a dictionary to map each unique value to a unique number
value_to_num = {value: i for i, value in enumerate(value_counts.index)}

# Create a new column in the DataFrame containing the unique number for each value
df_subset["CARRIER_NAME_int_label"] = df_subset["CARRIER_NAME"].map(value_to_num)

value_counts = df_subset["DEPARTING_AIRPORT"].value_counts().sort_index(ascending=True)

# Create a dictionary to map each unique value to a unique number
value_to_num = {value: i for i, value in enumerate(value_counts.index)}

# Create a new column in the DataFrame containing the unique number for each value
df_subset["DEPARTING_AIRPORT_int_label"] = df_subset["DEPARTING_AIRPORT"].map(value_to_num)

# see target variable proportions: clearly imbalanced
pd.crosstab(df['DEP_DEL15'], df['DEP_DEL15'], normalize='all')*100

# Pre-processing
df_subset2 = df_subset[["MONTH","DAY_OF_WEEK","DEP_DEL15","CONCURRENT_FLIGHTS","NUMBER_OF_SEATS","PRCP","SNOW","TMAX","AWND"]]
final_df = df_subset2.dropna()

# choose independant and dependant vars
y = final_df['DEP_DEL15']
X = final_df.drop('DEP_DEL15', axis=1, inplace= False)
#or
#x= data_set.iloc[:, [2,3]].values  
#y= data_set.iloc[:, 4].values  

# testing/training split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=rand_state)

# feature Scaling  
from sklearn.preprocessing import StandardScaler    
st_sc = StandardScaler()    
X_train= st_sc.fit_transform(X_train)    
X_test= st_sc.transform(X_test) 

#Fitting logistic regression model to training set
from sklearn.linear_model import LogisticRegression
logistic = LogisticRegression()
logistic.fit(X_train, y_train)

# Predicting test result
y_hat_30 = np.where(y_hat_probs>0.30,1,0)
y_hat_60 = np.where(y_hat_probs>0.60,1,0)
y_hat = logistic.predict(X_test)
y_hat_probs = logistic.predict_proba(X_test)[:,1] 
df_predictions = pd.DataFrame({'y_test': y_test, 'y_hat_probs': y_hat_probs, 
                               'y_hat': y_hat, 'y_hat_30': y_hat_30, 
                               'y_hat_60': y_hat_60})
                               
# Testing model accuracy
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, matthews_corrcoef
from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score
from sklearn.model_selection import cross_val_score
import sklearn.metrics

def logistic_report(X_train, y_train, X_test,y_test, threshold=0.5, penalty='none', class_weight=None):
    logistic= LogisticRegression(class_weight=class_weight, penalty=penalty)
    logistic.fit(X_train, y_train)
    probs = logistic.predict_proba(X_test)[:,1]
    y_hat = np.where(probs>=threshold,1,0)
    
    cm = confusion_matrix(y_test, y_hat)
    accuracy = round(accuracy_score(y_test,y_hat) ,2)
    precision = round(precision_score(y_test,y_hat),2)
    recall = round(recall_score(y_test,y_hat),2)
    f1score = round(f1_score(y_test,y_hat),2)
    MCC = round(matthews_corrcoef(y_test,y_hat),2)
    cm_labled = pd.DataFrame(cm, index=['Actual : negative ','Actual : positive'], columns=['Predict : negative','Predict :positive '])
    
    print("-----------------------------------------")
    print('Accuracy  = {}'.format(accuracy))
    print('Precision = {}'.format(precision))
    print('Recall    = {}'.format(recall))
    print('f1_score  = {}'.format(f1score))
    print('MCC       = {}'.format(MCC))
    print("-----------------------------------------")
    return cm_labled
    
# threshold can be adjusted to meet need of end user
logistic_report(X_train, y_train, X_test,y_test, threshold=0.62)
logistic = LogisticRegression(penalty='none')
accuracy_CV5 = cross_val_score(estimator = logistic, X = X_train, y = y_train, cv = 5, scoring="accuracy")


