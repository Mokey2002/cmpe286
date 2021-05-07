
##Code references in report
import face_recognition
import boto3
import botocore
from botocore.exceptions import ClientError
import cv2
from picamera import PiCamera
from time import sleep
import numpy as np
import os
from twilio.rest import Client
import RPi.GPIO as GPIO
import time

account_sid = 
auth_token =
client = Client(account_sid, auth_token)



def get_client():
    return boto3.client(
        's3',
    aws_access_key_id=,
    aws_secret_access_key=
    aws_session_token='',
    #region_name=
    )


def get_client2():
    return boto3.client(
        's3',
    aws_access_key_id='',
    aws_secret_access_key=''
    
    #region_name=REGION_NAME
    )

def get_object(s3,key):
    result = s3.list_objects(Bucket='cmpe286')
    for item in result['Contents']:
        print (item['Key'])
        foto = item['Key']
        s3.download_file('cmpe286',foto,foto)
    #s3.download_file('cpme286',key,"cam.jpg")
 

def detect():
  
    foto = "cam.jpg"
    s3 = get_client2()
    get_object(s3,foto)
    video = cv2.VideoCapture(0)
    userimg = face_recognition.load_image_file("cam.jpg")
    userface = face_recognition.face_encodings(userimg)[0]
    allowed_users=[
     
         userface
    ]
    
    #user_names = [
    user_names=[
        "Eduardo"
        
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    while True:
        ret, frame = video.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]
        if process_this_frame:
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(allowed_users, face_encoding)
                name = "Unknown"
                face_distances = face_recognition.face_distance(allowed_users, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = user_names[best_match_index]
                else:
                    
                    
                    message = client.messages \
    .create(
         body='Warning unknown person near front door',
         from_='+',
         to='+'
     )
            
  
                    print(message.sid)

                face_names.append(name)

        process_this_frame = not process_this_frame


        for (top, right, bottom, left), name in zip(face_locations, face_names):
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    video.release()
    cv2.destroyAllWindows()

while 1==1:

    GPIO.setmode(GPIO.BCM)

    TRIG = 23 
    ECHO = 24

    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, 0)
    time.sleep(0.2)
    print ("Starting Measurement")

    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        start = time.time()

    while GPIO.input(ECHO) == 1:
        stop = time.time()

    cal_time =  (stop - start) * 17000
    
    GPIO.cleanup()
    print("Person " + str(cal_time) + "cm  away")

    if cal_time < 50:
       detect()
       break
