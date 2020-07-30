import io
import os

#Copys & paste API key (need to do every shell session, get new key from Google Vision)
#how often do we need to download new one?
#export GOOGLE_APPLICATION_CREDENTIALS=##Need JSON

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.join(
    os.path.dirname(__file__),
    #directory here
    )


# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

#performs face detection on image
response2 = client.face_detection(image=image)
faces = response2.face_annotations
#liklelihood names from GV
likelihood_name = ('UNKNOWN', 'VERY_UNLIKELY', 'UNLIKELY', 'POSSIBLE',
                       'LIKELY', 'VERY_LIKELY')

print('Labels:')
for label in labels:
    print(label.description)
    print(label.score)
print('Faces:')
for face in faces:
    print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
    print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
    print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
    vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])
    print('face bounds: {}'.format(','.join(vertices)))