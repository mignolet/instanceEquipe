#-*- encoding:utf-8 -*-
from json_responses import json_response, json_data, json_error
from flask import Flask, request
import json
import requests
import os
from google.oauth2 import service_account
import googleapiclient.discovery
import base64

app = Flask(__name__)
app.debug = True

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
@app.route('/Classifier')
def Classifier():
    #get picture
    imagefile = request.files['file']
    labelObjet = testGoogleVissio(imagefile)
    #get data json
    jsonData = requests.get_json(force=True)

    #check reponse
    if jsonData["nameImageFr"] == labelObjet:
        #check number objet find
        teamrequest = requests.get("https://couchdb.mignolet.fr/objetfinddb/_design/_all_obsearch/_view/all")
        print(teamrequest.json())
        numObjetFind = json.loads(teamrequest.content)
        print(numObjetFind["rows"][0]["value"])
        #start json for couchdb
        idDevice = jsonData["Device_id"]
        jsonDataObjet = '{"idDevice": "'+str(idDevice)+'", "label": "'+labelObjet+'"}'
        #insert in couchdb
        r = requests.put("https://couchdb.mignolet.fr/objetfinddb/'objetFind34'", data=jsonDataObjet)
        print(r.json())
    return json_response(r.json(),r.status_code)


def helloInscript():
    dataName = requests.get("https://routerint.mignolet.fr/linkInstance")
    print(dataName.json())


if __name__ == '__main__':
    helloInscript()
    app.run(host='0.0.0.0', port=5000)

