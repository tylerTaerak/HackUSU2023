from flask import Flask
from flask import request, jsonify, render_template
from flask_cors import CORS
from loadModel import loadModel, predict

from airports import getFlightInfo

app = Flask(__name__)
cors = CORS(app, resources={r"/flights/query": {"origins": "*"}})

model = loadModel()


@app.route('/flights', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/flights/query', methods=['POST'])
def query():
    flight_no = request.json['flightNumber']

    # try:
    predictionData = getFlightInfo(flight_no)
    if predict(model, predictionData):
        prediction = {'prediction': "Your flight is likely to be delayed"}
    else:
        prediction = {'prediction': predict(model, predictionData)}
    # except:
    #     prediction = {'prediction': "could not find data for that flight number"}

    response = jsonify(prediction)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
