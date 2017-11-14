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

APIKEY = os.environ.get("LOGINCOUCHDB")
pwd = os.environ.get("PWDCOUCHDB")



def testGoogleVissio(imagefile):
    # Appel de la fonction de scan par Google
    credentials = service_account.Credentials.from_service_account_file('VisionTest.json')

    # Authentification par Google
    service = googleapiclient.discovery.build('vision', 'v1', credentials=credentials)

    # Traitement de la photo

    image_content = base64.b64encode(imagefile.read())

    # Formattage de la requête en JSON pour Google Vision

    service_request = service.images().annotate(body={
        'requests': [{
            'image': {
                'content': image_content.decode('UTF-8')
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

@app.route('/Classifier', methods="POST")
def Classifier():

    imagefile = request.files['file']
    labelObjet = testGoogleVissio(imagefile)

    jsonData = requests.get_json(force=True)

    if jsonData["nameImageFr"] == labelObjet:
        idDevice = jsonData["Device_if"]
        teamrequest = requests.get("https://couchdb.mignolet.fr/objetfinddb/_design/_all_obsearch/_view/all")

    return "ok"


#redirecte instance for team
@app.route('/redirecte')
def redirecte():
    return 'redirecte'


def helloInscript():
    dataName = requests.put("https://routerint.mignolet.fr/linkInstance")
    print(dataName)




if __name__ == '__main__':
    helloInscript()
    app.run(host='0.0.0.0', port=5000)

