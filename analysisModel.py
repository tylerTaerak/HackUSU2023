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

def predictWeatherDelay():
    # view target variable proportions
    pd.crosstab(df['weather_delay'], df['weather_delay'], normalize='all')*100

    # prep training
    y = df['weather_delay']
    X = df.drop('weather_delay', axis=1, inplace= False)
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=rand_state)

    # select logistic regression method
    from sklearn.linear_model import LogisticRegression

    # Fit Logistic Regression to the Training set
    logistic = LogisticRegression()
    logistic.fit(X_train, y_train)

    # testing segment
    y_hat = logistic.predict(X_test)
    y_hat_probs = logistic.predict_proba(X_test)[:,1] 


    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, matthews_corrcoef
    from sklearn.metrics import confusion_matrix, classification_report, roc_curve, roc_auc_score

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
    logistic_report(X_train, y_train, X_test,y_test, threshold=0.4)
    logistic = LogisticRegression(penalty='none')
    accuracy_CV5 = cross_val_score(estimator = logistic, X = X_train, y = y_train, cv = 5, scoring="accuracy")
