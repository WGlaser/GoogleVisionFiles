import io
import os


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("Keyboard.ttf", 32)

# Instantiates a client
client = vision.ImageAnnotatorClient()

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


main(#input, output, max results)