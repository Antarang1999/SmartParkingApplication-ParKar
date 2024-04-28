#The Program stores the intime of car from parking slot into Firebase

#Imports
import cv2  # OpenCV-Python is a library of Python bindings designed to solve computer vision problems.
import requests
import base64
import json
from firebase import firebase
from firebase_admin import db
import time
import pytz
from datetime import datetime
firebase = firebase.FirebaseApplication('https://parkin-5e7ee.firebaseio.com/', None)
import dateutil.tz

intime=[]
numberplate= {}
SECRET_KEY = 'sk_cd9c6a7e2d71bb1e1aa57590'
url = 'https://api.openalpr.com/v2/recognize_bytes?recognize_vehicle=1&country=ind&secret_key=%s' % (SECRET_KEY)
vidcap = cv2.VideoCapture('C://Users//DEVAN//Desktop//sample2.mp4')  #Open file for videocapturing
sec = 0
frameRate = 0.75
count=1
plate=[]
ref = db.reference('')


#Get Frame function i.e to convert video into frames
def getFrame(sec):
    vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
    hasFrames,image = vidcap.read()
    if hasFrames:
        cv2.imwrite("image"+str(count)+".jpg", image)   # saves the image to the specified file
        IMAGE_PATH = 'C:/Users/DEVAN/CarParking/image'+str(count)+'.jpg'
        with open(IMAGE_PATH, 'rb') as image_file:
            img_base64 = base64.b64encode(image_file.read())
    if hasFrames:
        r = requests.post(url, data=img_base64)
        jdata = json.dumps(r.json(), indent=1)
        jdata1 = str(json.loads(jdata))
        s = []
        s = jdata1.split('[')
        s4 = s[1].split(']')
        if (s4[0] != ''):
            s1 = []
            s1 = s[1].split(':')
            s2 = s1[1].split(',')
            s3 = s2[0].split("'")
            s5 = s1[2].split(",")
            con = s5[0]
            confidence = float(con)
            if (confidence >= 85.0):
                if(s3[1] not in plate):
                    local = dateutil.tz.tzlocal()
                    now = datetime.now()
                    now = now.replace(tzinfo = local)
                    tz = pytz.timezone('Asia/Kolkata')
                    your_now = now.astimezone(tz)
                    tq=str(your_now.hour)+":"+str(your_now.minute)+":"+str(your_now.second)
                    #print(tq)
                    intime.append(tq)
                    plate.append(s3[1])
                try:
                    conf = numberplate[s3[1]]
                    if conf > confidence:
                        numberplate[s3[1]] = conf
                except KeyError:
                    numberplate[s3[1]] = confidence
    return hasFrames

#Main Function
if __name__ == '__main__':
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)
    i=0
    for key in list(numberplate.keys()):
       print(key,numberplate[key])
       plate=key
       t=intime[i]
       data = {'Numberplate': plate,
               'In Time': t,
               'Out Time': 0
               }
       result = firebase.put('/users/', data)
       i+=1
        userRef = ref.child("users");
        userRef.child(plate).set({
            intime: t,
            outtime: 0
        }, onComplete);

        # booksRef.child('Niall OHiggins').set({
        #     title: "MongoDB and Python"
        # }, onComplete);
