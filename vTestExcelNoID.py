#Works with labels. halting to test on seperate file to test boxes

import io
import os
import xlsxwriter

#Copys & paste API key (need to do every shell session, get new key from Google Vision)
#how often do we need to download new one?
#export GOOGLE_APPLICATION_CREDENTIALS=#need JSON

#CHANGE name EVERYTIME
name = ##
fileName = name+'.xlsx';
directoryName = 'resources/'+name;

#create workbook
workbook = xlsxwriter.Workbook(fileName);
worksheet = workbook.add_worksheet()
worksheet.write(0,0, 'image name');
row = 1;
col = 0;
labelArr = [];

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate (one at at ime)
#file_name = os.path.join(
 #   os.path.dirname(__file__),
  #  'resources/peopleDrinking.jpg')

#for each file in directory
for file_name in os.listdir(directoryName):
    print("-------------"+file_name+'----------')
    #put name of pic in col
    worksheet.write(row,col, file_name+"_"+name)

    #create fullpath name for Google
    fullpath = directoryName+'/'+file_name

    # Loads the image into memory
    with io.open(fullpath, 'rb') as image_file:
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
        #print(label.description+ ": " + str(label.score))
        #have we seen it before?
        if label.description in labelArr:
            print(label.description + " from array");
            print(labelArr.index(label.description))
            #gets column in Sheet of the label
            colOfdescription = labelArr.index(label.description)+1
            #writes score in given row and column
            worksheet.write(row,colOfdescription, label.score);
        #it's not in the array, add it!
        else: 
            labelArr.append(label.description);
            print(label.description+" added to array")
            colOfdescription = labelArr.index(label.description)+1
            worksheet.write(0,colOfdescription, label.description);
            worksheet.write(row,colOfdescription, label.score);
       # print(label.score)
    print(labelArr)
    print('Faces:')
    for face in faces:
        #print(face.bounding_poly.vertices)
        #print('anger: {}'.format(likelihood_name[face.anger_likelihood]))
        #print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
        #print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
        #vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])
        #print('face bounds: {}'.format(','.join(vertices)))
        print("faces")
    #reset col
    col=0; 
    #row add 1
    row= row+1;

workbook.close();