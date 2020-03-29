from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse
from pprint import pprint
import os

app = Flask(__name__)


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    pprint(request.values)
    responded = False
    print("Incoming message: " + incoming_msg)
    data = getFactSearchData(str(incoming_msg))
    msg.body(data)

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

def getFactSearchData(query):

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
    print(r)
    # print(data['claims']) 
    if len(data['claims']) > 0:
        claim = data['claims'][0]['text']
        result = data['claims'][0]['claimReview'][0]['textualRating']
        reference = data['claims'][0]['claimReview'][0]['url']
        if result == 'False':
            returndata = '*FAKE NEWS ALERT* - This claim seems to be False. It is claimed that '+ claim +' But this is false. You can view more details at: ' + reference
        else:
            returndata = '*Not a Fake News* - The claim is: ' + claim + 'This claim seems to be genuine. You can view more details at: ' + reference    
        return returndata
    else:
        returndata = "Could not verify the claim"
        return returndata


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

