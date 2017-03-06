#!/usr/bin/env python

import yaml
import cairo
import cairosvg
import numpy as np
from numpy import random as rnd
import cv2
import os  

with open("config.yaml", 'r') as stream:
    try:
        CFG = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for fn in os.listdir(CFG['input_folder']):
    input_file = CFG['input_folder'] + "/" + fn
    print "looking at shape " + (fn)
    
    output_name = fn.split(".")[0]

    byte_string = cairosvg.svg2png(url=input_file)
    nparr = np.fromstring(byte_string, np.uint8)
    
    for sample in xrange(CFG['sample_size']):
        img = cv2.imdecode(nparr, flags=cv2.CV_LOAD_IMAGE_GRAYSCALE)
        img = cv2.resize(img, (CFG['width'], CFG['height'])) 
        img = cv2.copyMakeBorder(img,100,100,100,100,cv2.BORDER_CONSTANT,value=[0,0,0])
        img = cv2.resize(img, (CFG['width'], CFG['height'])) 
        rows,cols = img.shape
        
        rotate_angle = CFG['angle']/2 - int(CFG['angle'] * rnd.random())
        scale_x = int((0.25 + (0.5 * rnd.random())) * rows)
        scale_y = int((0.25 + (0.5 * rnd.random())) * cols)
        
        translate_factor = CFG['translation'] * (rows+cols/2)
        translate_x = scale_x / 2 + translate_factor/2 - int(translate_factor * rnd.random())
        translate_y = scale_y / 2 + translate_factor/2 - int(translate_factor * rnd.random())
                
        M_translate = np.float32([[1,0,translate_x],[0,1,translate_y]])
        M_rotate = cv2.getRotationMatrix2D((cols/2,rows/2),rotate_angle,1)

        img = cv2.resize(img,(scale_x, scale_y), interpolation = cv2.INTER_CUBIC)
        img = cv2.warpAffine(img, M_rotate, (cols,rows))
        img = cv2.warpAffine(img, M_translate, (cols,rows))

        noise = np.zeros(img.shape, np.uint8)
        cv2.randn(noise,(0),(CFG['noise']))
        
        img += noise
        
        cv2.imwrite(CFG['output_folder'] + "/" + output_name + "%05d.png" % sample, img)