import requests

r = requests.get('https://api.twilio.com/2010-04-01/Accounts/AC4f3f21e7eae8777700fb56c7b5cb8258/Messages/MMb6dbc759accc4f334dfdf6644a158833/Media/ME5ce32d7430e2870c7a456eaf5ef88d42')

print(r.url)
