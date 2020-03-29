# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# Instantiates a client
client = language.LanguageServiceClient()

# The text to analyze
text = u'Hello, world!'
document = types.Document(
    content=text,
    type=enums.Document.Type.PLAIN_TEXT)

# Detects the sentiment of the text
response = client.analyze_entities(document=document)


for entity in response.entities:
  print('=' * 20)
  print('         name: {0}'.format(entity.name))
  print('         type: {0}'.format(entity.type))
  print('     metadata: {0}'.format(entity.metadata))
  print('     salience: {0}'.format(entity.salience))
