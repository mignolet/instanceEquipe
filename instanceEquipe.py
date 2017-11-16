#-*- encoding:utf-8 -*-
from json_responses import json_response, json_data, json_error
from flask import Flask, request
import json
import requests
import os
from google.oauth2 import service_account
import googleapiclient.discovery
import base64
import smtplib,socket,os,sys
import time

app = Flask(__name__)
app.debug = True

admin = os.environ.get("LOGINCOUCHDB")
pwd = os.environ.get("PWDCOUCHDB")
LinuxIP="/sbin/ifconfig"

#check in visio cloud google
def testGoogleVissio(imagefile):
    # Appel de la fonction de scan par Google
    credentials = service_account.Credentials.from_service_account_file('config/visio.json')

    # Authentification par Google
    service = googleapiclient.discovery.build('vision', 'v1', credentials=credentials)

    # Traitement de la photo
    #image_content = base64.b64encode(imagefile.read())

    # Formattage de la requête en JSON pour Google Vision

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': imagefile
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': 1
            }]
        }]
    })

    # Envoie de la requête et réception du résultat

    response = service_request.execute()
    print(response)

    # Récupération de la déduction de l'image par Google
    label = response['responses'][0]['labelAnnotations'][0]['description']

    return label

#check picture objet
#test in visio cloud google
#insert couchdb objetfind
@app.route('/Classifier', methods=["POST"])
def Classifier():
    jsonData = request.get_json(force=True)
    #print(jsonData)

    #print(jsonData["image"])
    labelObjet = testGoogleVissio(jsonData["image"])

 
    #check reponse
    print(labelObjet)
    if jsonData["name"] == labelObjet:
        print("check reussi")
        #check number objet find
        teamrequest = requests.get("https://couchdb.mignolet.fr/objetfinddb/_design/_all_obsearch/_view/all")
        print(teamrequest.json())
        numObjetFind = json.loads(teamrequest.content)
        print(numObjetFind["rows"][0]["value"])
        #start json for couchdb
        idDevice = jsonData["Device_id"]
        jsonDataObjet = '{"idDevice": "'+str(idDevice)+'", "label": "'+labelObjet+'"}'
        #insert in couchdb
        r = requests.put("https://couchdb.mignolet.fr/objetfinddb/'objetFind"+str(numObjetFind+1)+"'", data=jsonDataObjet)
        print(r.json())
        return True
    else:
        print("check false")
        return False


@app.route('/saveImage')
def saveImage():
    return "save photo"



@app.route('/getImage')
def getImage():
    return "retour photo"




#link team and instance
def helloInscript():
    ip = socket.gethostbyname_ex(socket.gethostname())
    print(ip)
    jsonIP = '{"ip": "'+ip[2][0]+'"}'
    ipSend = requests.post("https://routerint.mignolet.fr/linkInstance", data=jsonIP)
    print(ipSend)

if __name__ == '__main__':
    helloInscript()
    app.run(host='0.0.0.0', port=5000)

