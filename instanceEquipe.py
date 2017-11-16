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
    credentials = service_account.Credentials.from_service_account_file('/root/config/visio-cloud.json')

    # Authentification par Google
    service = googleapiclient.discovery.build('vision', 'v1', credentials=credentials)

    # Traitement de la photo
    #image_content = base64.b64encode(imagefile.read())

    # Formattage de la requête en JSON pour Google Vision

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': imagefile.decode('UTF-8')
            },
            'features': [{
                'type': 'LABEL_DETECTION',
                'maxResults': 1
            }]
        }]
    })

    # Envoie de la requête et réception du résultat

    response = service_request.execute()

    # Récupération de la déduction de l'image par Google
    label = response['responses'][0]['labelAnnotations'][0]['description']

    return label

#check picture objet
#test in visio cloud google
#insert couchdb objetfind
@app.route('/Classifier', methods=["POST"])
def Classifier():
    jsonData = requests.get_json(force=True)
    print(jsonData)
    #get picture
    #imagefile = request.files['file']
    labelObjet = testGoogleVissio(jsonData["image"])
 #   {u'latitute': u'42/1,40/1,31616/1000', u'id_Equipe': u'4185ea90f53b085cECOKBC085506',
 #    u'image': u'/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDACgcHiMeGSgjISMtKygwPGRBPDc3PHtYXUlkkYCZlo+A\njIqgtObDoKrarYqMyP/L2u71////m8H////6/+b9//j/2wBDASstLTw1PHZBQXb4pYyl+Pj4+Pj4\n+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj4+Pj/wAARCADIAMgDASIA\nAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQA\nAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3\nODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWm\np6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEA\nAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSEx\nBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElK\nU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3\nuLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwDGoooo\nAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigA\nooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACi\niigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK\nKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooo\nAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigA\nooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACi\niigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK\nKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAoooo\nAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigA\nooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACi\niigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKK\nKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooA//Z\n',
 #    u'name': u'car_20171115_194912_1858244874.jpg', u'longitude': u'2/1,50/1,58405/1000'}
    #check reponse
    print(labelObjet)
    if jsonData["name"] == labelObjet:
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

