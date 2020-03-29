import requests
from pprint import pprint
import os

URL = "https://content-factchecktools.googleapis.com/v1alpha1/claims:search"
# location given here 
query = "arsenicum medicine"
# defining a params dict for the parameters to be sent to the API 
key = os.getenv('API_KEY')
PARAMS = {'query':query, 'key': key} 
# sending get request and saving the response as response object 
r = requests.get(url = URL, params = PARAMS) 
# extracting data in json format 
data = r.json()
print(data)
# print(data['claims']) 
if len(data['claims']) > 0:
	claim = data['claims'][0]['text']
	result = data['claims'][0]['claimReview'][0]['textualRating']
	reference = data['claims'][0]['claimReview'][0]['url']
	if result == 'False':
		returndata = '*FAKE NEWS ALERT* - This claim seems to be False. It is claimed that '+ claim +' But this is false. You can view more details at: ' + reference
	else:
		returndata = '*Not a Fake News* - The claim is: ' + claim + 'This claim seems to be genuine. You can view more details at: ' + reference	
	print(returndata)
else:
	returndata = "Could not verify the claim"
	print(returndata)
