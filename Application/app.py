import re
from flask import Flask, render_template, request, jsonify
from flask.helpers import flash
from tensorflow import keras

model = keras.models.load_model("model")

app = Flask(__name__)
app.secret_key ="keep it secret"
Latitude=0
Longitude=0
VIC_AGE_GROUP=0
CMPLNT_FR_YEAR=0
CMPLNT_FR_MONTH=0
CMPLNT_FR_DAY=0
CMPLNT_FR_HOUR=0
VIC_SEX_F=0
VIC_SEX_M=0
data = {}
@app.route('/' , methods=[ "GET" ,"POST" ])
def hello():
    
    if (request.method =="POST"):
        name = request.form.get("name")
        Latitude= request.form.get('x')
        Longitude=request.form.get('y')
        age = request.form.get('age')
        time =request.form.get('time')
        date=request.form.get('date')
        gender = request.form.get('gender') # 0 : for man and 1: from woman PS: you can change the value mil html
        cmplnt = date.split("-")
        CMPLNT_FR_YEAR=int(cmplnt[0])
        CMPLNT_FR_MONTH=int(cmplnt[1])
        CMPLNT_FR_DAY=int(cmplnt[2])
        CMPLNT_FR_HOUR = int(time.split(":")[0])
        if(int(age) <= 24):
            VIC_AGE_GROUP=0
        if((int(age) <= 64)and (int(age) >= 25)):
            VIC_AGE_GROUP=1
        if(int(age) > 64):
            VIC_AGE_GROUP=2
        if (int(gender)==1):
            VIC_SEX_F=1
            VIC_SEX_M=0
        if (int(gender)==0):
            VIC_SEX_M=1
            VIC_SEX_F=0
        Latitude=float(Latitude)
        Longitude=float(Longitude)
        ky_cd = model.predict(
            [
                [
                    Latitude,
                    Longitude,
                    VIC_AGE_GROUP,
                    CMPLNT_FR_YEAR,
                    CMPLNT_FR_MONTH,
                    CMPLNT_FR_DAY,
                    CMPLNT_FR_HOUR,
                    VIC_SEX_F,
                    VIC_SEX_M
                    
                    
                ]
            ]
        )
        
        # probability of crimes 
        data["Drugs crimes"] = format(ky_cd[0][0]*100, '.2f')
        data["Killing crimes"] = format(ky_cd[0][1]*100 , '.2f')
        data["Violent crimes"] = format(ky_cd[0][3]*100, '.2f')
        data["Sexual crimes"] = format(ky_cd[0][4]*100 , '.2f')
        data["Theft crimes"] = format(ky_cd[0][5]*100 , '.2f')
        data["Other type of crimes"] = format(ky_cd[0][2]*100 , '.2f')
        flash(data)
    return render_template("osm_gs.html" )  
