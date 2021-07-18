import sys, random, argparse
import numpy as np
import math
from PIL import Image

# grayscale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 70 levels of gray
gscale1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "

# 10 levels of gray
gscale2 = '@%#*+=-:. '

def getAverageL(image):
    """
    Given PIL Image, retuen average value of grayscale value
    """
    
    # Get image as numpy array
    im = np.array(image)

    # Get the dimensions.
    w, h = im.shape

    # Get the average.
    return np.average(im.reshape(w*h))

def covertImageToAscii(file_name, cols, scale, moreLevels):
    """
    Given Image and dimensions (rows, cols), returns an m*n list of image.
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grey scale
    image = Image.open(file_name).convert('L')

    # Store the image dimensions.
    W, H = image.size[0], image.size[1]
    print("Input image dimensions : %d x %d" % (W, H))

    # Compute tile width
    w = W/cols

    # Compute the tile height based on the aspect ratio and scale of the font 
    h = w/scale

    # Compute the number of rows to use in the final grid.
    rows = int(H/h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))
    
    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)
    
    # an ASCII image is a list of character strings
    aimg = []
    
    # generate the list of tile dimensions
    for j in range(rows):
        y1 = int(j*h)
        y2 = int((j+1)*h)

        # correct the last tile
        if j == rows-1:
            y2 = H
        
        # append an empty string
        aimg.append("")
        for i in range(cols):
            # crop the image to fit the tile
            x1 = int(i*w)
            x2 = int((i+1)*w)
    
            # correct the last tile
            if i == cols-1:
                x2 = W
            
            # crop the image to extract the tile into another Image object
            img = image.crop((x1, y1, x2, y2))

            # get the average luminance
            avg = int(getAverageL(img))
            
            # look up the ASCII character for grayscale value (avg)
            if moreLevels:
                gsval = gscale1[int((avg*69)/255)]
            else:
                gsval = gscale2[int((avg*9)/255)]

            # append the ASCII character to the string
            aimg[j] += gsval
        # return text image
    return aimg

# main() function
def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    # parse arguments
    args = parser.parse_args()
    imgFile = args.imgFile
    
    # set output file
    outFile = 'out.txt'
    if args.outFile:
        outFile = args.outFile
    
    # set scale default as 0.43, which suits a Courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    
    # set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)
    
    print('generating ASCII art...')
    # convert image to ASCII text
    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels)

    # open a new text file
    f = open(outFile, 'w')

    # write each string in the list to the new file
    for row in aimg:
        f.write(row + '\n')
        # clean up
    f.close()
    print("ASCII art written to %s" % outFile)
    
# call main
if __name__ == '__main__':
    main()
