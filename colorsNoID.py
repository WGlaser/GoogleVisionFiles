import os
import io
import colorsys

#hue coloring red-blue (low red high blue)
#saturation vividness low is gray and faded
#value hsv 
from PIL import Image

#directory info
name = 
directoryName = 'resources/'+name;

#special directory functionto avoid hidden files
def myListDir(dir):
    filelist = os.listdir(dir)
    return [x for x in filelist if not (x.startswith('.'))]

def convertToHSV(r,g,b):
	red = r/255;
	green = g/255;
	blue = b/255;
	h,s,v = colorsys.rgb_to_hsv(red,green,blue);
	v= v*100;
	h = h*360;
	s =s*100;
	return [h,s,v];
	#print("RGB: "+str(r)+","+str(g)+","+str(b))
	#print("HSV: "+str(h)+","+str(s)+","+str(v))


#for each file in directory
for file_name in myListDir(directoryName):
	#create fullpath name for Google
    fullpath = directoryName+'/'+file_name
    print(fullpath)
    img = Image.open(fullpath);
    colors =img.convert('RGB').getcolors(1000000)
    width, height = img.size
    numPixels= width*height
    sumH=0
    sumS=0
    sumV=0
    for c in colors:
    	#getColors returns tuple of [[num pixels][r,g,b]]
    	hsv = convertToHSV(c[1][0],c[1][1],c[1][2]) #rgb values from colors tuple
    	sumH = sumH+ c[0]*hsv[0] #multiply hsv value for a given color by number of times it appears in image, add to running sum
    	sumS = sumS+ c[0]*hsv[1]
    	sumV = sumV+ c[0]*hsv[2]
    print("sumH="+str(sumH/numPixels)); #divide by numPixels to get mean
    print("sumS="+str(sumS/numPixels));
    print("sumV="+str(sumV/numPixels));