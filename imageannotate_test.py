from google.cloud import vision


def detect_text_uri(uri):
    """Detects text in the file located in Google Cloud Storage or on the Web.
    """
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

    for text in texts:
        # print(text.description.split())
        # print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        # print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))



detect_text_uri('https://api.twilio.com/2010-04-01/Accounts/AC4f3f21e7eae8777700fb56c7b5cb8258/Messages/MMb6dbc759accc4f334dfdf6644a158833/Media/ME5ce32d7430e2870c7a456eaf5ef88d42')
