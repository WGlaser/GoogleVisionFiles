import io
import os
import xlsxwriter

#Copys & paste API key (need to do every shell session, get new key from Google Vision)
#how often do we need to download new one?
#export GOOGLE_APPLICATION_CREDENTIALS=need JSON file

#unset PYTHONPATH

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
topRowArr = [];

# Imports the Google Cloud client library and text stuff

from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont
font = ImageFont.truetype("Keyboard.ttf", 32)


# Instantiates a client
client = vision.ImageAnnotatorClient()

######methods TO DRAW BOXES#######


def detect_face(face_file, max_results=5):
  content = face_file.read()
  image = types.Image(content=content)
  return client.face_detection(image=image).face_annotations



def highlight_faces(image, faces, output_filename):
    """Draws a polygon around the faces, then saves to output_filename.

    Args:
      image: a file containing the image with the faces.
      faces: a list of faces found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    i=1;
    for face in faces:
        box = [(vertex.x, vertex.y)
               for vertex in face.bounding_poly.vertices]
        
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        draw.text((box[0][0], box[0][1]),"face"+str(i),(255,255,255),font=font)
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])

        #draw.text((box[0][0], box[0][1]),': {}'.format(','.join(vertices)),(255,0,0),font=font)
        i=i+1;

    im.save(output_filename)

def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        faces = detect_face(image, max_results)
        print('Found {} face{}'.format(
            len(faces), '' if len(faces) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)
        highlight_faces(image, faces, output_filename)
######END methods FOR BOXES#######


#helper to avoid hidden files
def myListDir(dir):
    filelist = os.listdir(dir)
    return [x for x in filelist if not (x.startswith('.'))]

#for each file in directory
for file_name in myListDir(directoryName):
    print("-------------"+file_name+'----------')
    #put name of pic in col
    worksheet.write(row,col, file_name+"_"+name)

    #create fullpath name for Google
    fullpath = directoryName+'/'+file_name
    print(fullpath)
    #label the thing
    main(fullpath, fullpath[:-4]+"withboxes.jpg",5)

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
        if label.description in topRowArr:
            print(label.description + " from array");
           # print(topRowArr.index(label.description))
            #gets column in Sheet of the label
            colOfdescription = topRowArr.index(label.description)+1
            #writes score in given row and column
            worksheet.write(row,colOfdescription, label.score);
        #it's not in the array, add it!
        else: 
            topRowArr.append(label.description);
            print(label.description+" added to array")
            colOfdescription = topRowArr.index(label.description)+1
           # print('COLOFDESCRIPTION: '+str(colOfdescription))
            worksheet.write(0,colOfdescription, label.description);
            worksheet.write(row,colOfdescription, label.score);
       # print(label.score)
    #print(topRowArr)
    #print('Faces:')
    i =1
    for face in faces:
        vertices = (['({},{})'.format(vertex.x, vertex.y) for vertex in face.bounding_poly.vertices])
        print('face bounds: {}'.format(','.join(vertices)))
        emotionArr = ['anger','joy','surprise']
        d = {'face.anger_likelihood':face.anger_likelihood, 'face.joy_likelihood': face.joy_likelihood, 'face.surprise_likelihood': face.surprise_likelihood}
        #FORMAT: emotion_faceN
        for emotion in emotionArr:
            emotionNameNum = emotion+'_face'+str(i)
            emotionLikelihood = 'face.'+emotion + '_likelihood'


        #is this face name in row 1?
            if emotionNameNum in topRowArr:
               colOfFace = topRowArr.index(emotionNameNum)+1
               worksheet.write(row,colOfFace,'{}'.format(likelihood_name[d[emotionLikelihood]]))
            else:
                topRowArr.append(emotionNameNum)
                #print('appended'+emotionNameNum)

                colOfFace = topRowArr.index(emotionNameNum)+1
                #print('COLOFFACE: '+str(colOfFace))

                worksheet.write(0,colOfFace, emotionNameNum);
                worksheet.write(row,colOfFace, '{}'.format(likelihood_name[d[emotionLikelihood]]));

            print('{}'.format(likelihood_name[face.anger_likelihood]))
           #print(face.bounding_poly.vertices)
            print('joy_face'+str(i))
            print('joy: {}'.format(likelihood_name[face.joy_likelihood]))
            print('surprise_face'+str(i))
            print('surprise: {}'.format(likelihood_name[face.surprise_likelihood]))
            
        i=i+1
    #reset col
    col=0; 
    #row add 1
    row= row+1;
workbook.close();
