
from flask import Flask
from flask import Flask, redirect, url_for, request, jsonify
import pickle 
import pandas as pd 
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
import firebase_admin

app = Flask(__name__)
# cred_obj = firebase_admin.credentials.Certificate('....path to file')
# default_app = firebase_admin.initialize_app(cred_object, {
# 	'databaseURL':databaseURL
# 	})

filename = "DT.sav"

@app.route('/')
def index():
    return "Web App with Python Flask!"

@app.route('/value', methods=["POST"])
def storeValue():
    return "store"


@app.route('/predict', methods=["POST"])
def predict():
    pincode = request.form['pin']
    temperature = 35 #request.form['temp']
    humidity = 80#request.form['hum']
    pm2 = 19 #request.form['pm']

    print("got deatails ", pincode," ", temperature," ", humidity," ", pm2)
    li =  []
    li.append(humidity)
    li.append(temperature)
    li.append(pm2)

    X = pd.DataFrame([li],columns = ["Humidity","Temperature","PM2.5"])
    loaded_model = pickle.load(open(filename, 'rb'))
    predictions = loaded_model.predict(X)

    value = str(predictions[0])
    data = {
            "temp" : temperature,
            "hum" : humidity,
            "pin":pincode,
            "act":value,
            "pm2":pm2,
        }
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)

