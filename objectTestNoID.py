import io
import os


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont

font = ImageFont.truetype("Keyboard.ttf", 32)

# Instantiates a client
client = vision.ImageAnnotatorClient()

def detect_objects(image_file, max_results):
    content = image_file.read()
    image = vision.types.Image(content=content)
    objects = client.object_localization(
        image=image).localized_object_annotations
    return objects

### gets image width/height
#im = Image.open(image_file)
 #   width, height = im.size
  #  print(width)
   # print(height)
###

def highlight_objects(image, objects, output_filename):
    """Draws a polygon around the objects, then saves to output_filename.

    Args:
      image: a file containing the image with the objects.
      objects: a list of objects found in the file. This should be in the format
          returned by the Vision API.
      output_filename: the name of the image file to be created, where the
          faces have polygons drawn around them.
    """
    im = Image.open(image)
    draw = ImageDraw.Draw(im)
    width, height = im.size
    for obj in objects:
        print(obj.name)
        box = [(vertex.x*width, vertex.y*height)
               for vertex in obj.bounding_poly.normalized_vertices]
        
        draw.line(box + [box[0]], width=5, fill='#00ff00')
        draw.text((box[0][0], box[0][1]),obj.name,(255,255,255),font=font) 

       
    im.save(output_filename)

def main(input_filename, output_filename, max_results):
    with open(input_filename, 'rb') as image:
        objects = detect_objects(image, max_results)
        print('Found {} object{}'.format(
            len(objects), '' if len(objects) == 1 else 's'))

        print('Writing to file {}'.format(output_filename))
        # Reset the file pointer, so we can read the file again
        image.seek(0)

        highlight_objects(image, objects, output_filename)


main(#input, output, results)