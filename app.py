
from ipaddress import ip_address
from flask import Flask
from flask import Flask, redirect, url_for, request, jsonify
import pickle 
import pandas as pd 
import warnings

from requests import NullHandler
warnings.filterwarnings("ignore", category=UserWarning)
import firebase_admin
from firebase_admin import db

app = Flask(__name__)

# cred = credentials.Certificate("asthma-pred-firebase-adminsdk-kokv3-19683e0cac.json")
# firebase_admin.initialize_app(cred)
cred_obj = firebase_admin.credentials.Certificate('asthma-pred-firebase-adminsdk-kokv3-19683e0cac.json')
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://asthma-pred-default-rtdb.firebaseio.com',
	})


filename = "DT.sav"

@app.route('/')
def index():
    return "Web App with Python Flask!"

@app.route('/postplain/', methods= ["POST", 'GET'])
def postplain():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        print(json)
        return "Done"
    else:
        return 'Content-Type not supported!'



@app.route('/value', methods=["GET"])
def storeValue():
    ref = db.reference("/")
    ref.push({
    "data": {
        "673640": {
            "timestamp": "1",
            "temp": "34",
            "hum": "72",
            "pm2": "49",
    }
  }
})
    return "Done"

@app.route('/getvalue', methods=["GET"])
def getValue():
    pin = '673640'
    ref = db.reference("/")
    j_value = ref.get()
    for i in j_value:
        a = j_value[i]['data'].get(pin)
        print(a)
    if a == None:
        print(a)
        return('no pincode')
    return(a)

@app.route('/updatevalue', methods=["GET"])
def updatevalue():
    pin = '673640'
    ref = db.reference("/")
    j_value = ref.get()
    for i in j_value:
        a = j_value[i]['data'].get(pin)
        print(a)
    if a == None:
        print(a)
        return('no pincode')
    
    return(a)

@app.route('/predict', methods=["POST"])
def predict():
    pincode = request.form['pin']
    print("Pin ", pincode)
    ref = db.reference("/-N2fNxS3nj_2fiKPVv2A/data/"+pincode)
    value = ref.get()
    if value == None:
        print("No value in")
        return "no data"
    temperature = value["temp"]
    humidity = value["hum"]
    pm2 = value["pm2"]

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
    app.run(debug=True, port="6000", host="0.0.0.0")

