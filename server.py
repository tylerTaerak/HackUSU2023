from flask import Flask
from flask import request, jsonify, render_template
from flask_cors import CORS
import datetime

from airports import getFlightInfo

app = Flask(__name__)
cors = CORS(app, resources={r"/flights/query": {"origins": "*"}})


@app.route('/flights', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/flights/query', methods=['POST'])
def query():
    flight_no = request.json['flightNumber']
    date = datetime.datetime.strptime(request.json['flightDate'], "%Y-%m-%d")

    predictionData = 'No predictions available yet' #getFlightInfo(flight_no, date)
    prediction = {'prediction': predictionData}

    response = jsonify(prediction)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
