import joblib
import numpy as np
import datetime
from airports import getFlightInfo


def loadModel():
    model = joblib.load('trainingData/model.pkl')
    X_train = joblib.load('trainingData/dataX.pkl')
    # y_train = X_train['DEP_DEL15']
    y_train = joblib.load('trainingData/datay.pkl')

    model.fit(X_train, y_train)

    return model


# input has [MONTH, DAY OF WEEK, PRCP, SNOW, TMAX, AWND, CARRIER_NAME_int_label, DEPARTING_AIRPORT_int_label]

def predict(model, X):
    return bool(model.predict(X)[0])


if __name__ == "__main__":
    data = loadModel()
    flight_no = 'UN3436'
    print(predict(data, getFlightInfo(flight_no)))
