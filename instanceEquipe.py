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

LinuxIP="/sbin/ifconfig"

#check in visio cloud google
def testGoogleVissio(imagefile):
    print(imagefile)
    # Appel de la fonction de scan par Google
    credentials = service_account.Credentials.from_service_account_file('../visio.json')

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
    print("test google fini")
    return label

#check picture objet
#test in visio cloud google
#insert couchdb objetfind
@app.route('/Classifier', methods=["POST"])
def Classifier():
    jsonData = request.get_json(force=True)
    print(jsonData)
    #print(jsonData["image"])
    labelObjet = testGoogleVissio(jsonData["image"])

    #check reponse
    print(labelObjet)
    print(jsonData["name"])

    if jsonData["name"] == labelObjet:
        print("check reussi")
        saveImage(jsonData)
        #check number objet find
        teamrequest = requests.get("https://couchdb.mignolet.fr/objetfinddb/_design/_all_obsearch/_view/all")
        print(teamrequest.json())
        numObjetFind = json.loads(teamrequest.content)
        print(numObjetFind["rows"][0]["value"])
        #start json for couchdb
        idDevice = jsonData["id_Equipe"]
        jsonDataObjet = '{"idDevice": "'+str(idDevice)+'", "label": "'+str(labelObjet)+'"}'
        print(jsonDataObjet)
        #insert in couchdb
        r = requests.put("https://couchdb.mignolet.fr/objetfinddb/'objetFind"+str(numObjetFind["rows"][0]["value"]+1)+"'", data=jsonDataObjet)
        print(r.json())
        return json_response("true")
    else:
        print("check false")
        return json_response("False")

def readImageJson():
    data = json.load(open("image.json"))
    print("json fichier :"+str(data))
    return data


#@app.route('/saveImage', methods=["POST"])
def saveImage(jsonImage):
    #get json
    #jsonImage = request.get_json(force=True)
    print(jsonImage)
    print(json.dumps(jsonImage))
    dataFiles = readImageJson()
    print("file:"+str(dataFiles))

    #send json
    data = json.loads(dataFiles)
    print(data["objetFinb"])
    data["objetFinb"].append(jsonImage)
    print(data)
    jsonfile = json.dumps(data)
    #print(jsonfile)
    #write
    with open("image.json", "w") as f_write:
        json.dump(jsonfile, f_write)
    return "save photo"

@app.route('/getImage')
def getImage():
    json = readImageJson()
    return json

#init json file
def init():
    jsonfile = '{"objetFinb" : []}'
    with open("image.json", "w") as f_write:
        json.dump(jsonfile, f_write)
    print("init fichier json")


#link team and instance
def helloInscript():
    ip = socket.gethostbyname_ex(socket.gethostname())
    print(ip)
    jsonIP = '{"ip": "'+ip[2][0]+'"}'
    ipSend = requests.post("http://51.254.121.94:4000/linkInstance", data=jsonIP)
    print(ipSend)

if __name__ == '__main__':
    helloInscript()
    init()
    app.run(host='0.0.0.0', port=5000)

