from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from pprint import pprint
import os

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import vision


app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    pprint(request.values)
    responded = False

    media = request.values.get('MediaContentType0', '')
    if media.startswith('image/'):
        incoming_media = request.values.get('MediaUrl0', '')
        if not incoming_media == '':
            incoming_msg = incoming_msg + " " + extractTextsFromImage(incoming_media)

    '''
    if hasattr(request.values, 'MediaContentType0'):
        print("found media")
        if request.values.get('MediaContentType0').contains('image'):
            print('containsimage')
            incoming_msg = incoming_msg + " " + extractTextsFromImage(request.values.get('MediaUrl0'))
    ''' 
    print("Incoming message: " + incoming_msg)
    entities = getKeyWords(incoming_msg)
    output = prepareFactSearchOutput(entities)
    msg.body(output)




    '''
    if 'quote' in incoming_msg:
        # return a quote
        r = requests.get('https://api.quotable.io/random')
        if r.status_code == 200:
            data = r.json()
            quote = f'{data["content"]} ({data["author"]})'
        else:
            quote = 'I could not retrieve a quote at this time, sorry.'
        msg.body(quote)
        responded = True
    if 'cat' in incoming_msg:
        # return a cat pic
        msg.media('https://cataas.com/cat')
        responded = True
    if not responded:
        msg.body('I only know about famous quotes and cats, sorry!')
    '''
    return str(resp)

def extractTextsFromImage(imageURL):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
    # We need the final url of the image
    r = requests.get(imageURL)
    uri = r.url
    print('URL: ' + uri)
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()
    image.source.image_uri = uri
    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    # print(texts)
    if len(texts) > 0:
        text = texts[0].description
    else:
        text = ''
    print(text)
    return text

def prepareFactSearchOutput(entities):
    for i in range(10,0,-1):
        searchstring = ' '.join(entities[0:i])
        data = performFactSearch(searchstring)
        print("Searching for: " + searchstring)
        if "claims" in data and len(data['claims']) > 0:
            output = ""
            print("Searching for: " + searchstring)   
            if i < 6:
                output = "This might be a general search. Please google to look further. \n"
            return output + prepareFactSearchString(data)

    returndata = "Could not verify the claim. Didn't find any references on this."
    return returndata
        

def performFactSearch(query):
    URL = "https://content-factchecktools.googleapis.com/v1alpha1/claims:search"
    # location given here 
    # defining a params dict for the parameters to be sent to the API 
    # query = "arsenicum medicine"
    key = os.getenv('API_KEY')
    print(key)
    PARAMS = {'query':query, 'key': key}
    # sending get request and saving the response as response object 
    r = requests.get(url = URL, params = PARAMS)
    # extracting data in json format 
    data = r.json()
    return data

def prepareFactSearchString(data):
    claim = data['claims'][0]['text']
    result = data['claims'][0]['claimReview'][0]['textualRating']
    reference = data['claims'][0]['claimReview'][0]['url']
    returndata = "Claim: " + claim + '\n'
    returndata = returndata + "Refer: " + reference + '\n'
    if result == 'False':
        returndata = '*FAKE NEWS ALERT* - There are fake news around for this. \n' + returndata 
    else:
        returndata = "There are several genuine articles on this topic. \n" + returndata
    return returndata

def getKeyWords(text):
    client = language.LanguageServiceClient()
    # The text to analyze
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT,
        language='en')
    # Detects the sentiment of the text
    response = client.analyze_entities(document=document)
    output = []
    for entity in response.entities:    
        output.append(entity.name)
    return output


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

