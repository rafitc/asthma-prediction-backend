
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
        #print(json)
        pin = json["pin"]
        print(pin)
        temp = json["temp"]
        hum = json["hum"]
        pm2 = json["pm2"]

        #check for pin
        ref = db.reference("/")
        j_value = ref.get()
        for i in j_value:
            a = j_value[i]['data'].get(pin)
            if not a == None:
                print("already found a pin code, entry updated in ", pin)
                path = i + "/data/"+pin
                #update val
                ref.child(path).update({
                    "timestamp": '2',
                    "temp":temp ,
                    "hum": hum,
                    "pm2": pm2,})
                return ("already found a pin code, entry updated in "+ pin)
        if a == None:
            print("no data so adding data")
            ref = db.reference("/")
            ref.push({
            "data": {
                pin: {
                    "timestamp": "1",
                    "temp": temp,
                    "hum": hum,
                    "pm2": pm2,
            }
            }
            })
            return('Updated with new pin code :' + pin)


@app.route('/value', methods=["GET"])
def storeValue():
    ref = db.reference("/")
    ref.push({
    "data": {
        "688504": {
            "timestamp": "1",
            "temp": "30",
            "hum": "71",
            "pm2": "20",
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
    ref = db.reference("/")
    j_value = ref.get()
    value = None
    for i in j_value:
        value = j_value[i]['data'].get(pincode)
        if not value == None:
            break;
    if value == None:
        print("No value in")
        data = {
            "temp" : "error",
            "hum" : "error",
            "pin":"error",
            "act":"error",
            "pm2":"error",
        }
        return jsonify(data)
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

