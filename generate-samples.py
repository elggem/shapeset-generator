#!/usr/bin/env python

import yaml
import cairo
#import rsvg
import os  

with open("config.yaml", 'r') as stream:
    try:
        CFG = yaml.load(stream)
    except yaml.YAMLError as exc:
        print(exc)

for fn in os.listdir(CFG['input_folder']):
    print "looking at shape " + (fn)
    
    img = cairo.ImageSurface(cairo.FORMAT_ARGB32, CFG['width'],CFG['height'])

    ctx = cairo.Context(img)

    handle = rsvg.Handle(fn)
    # or, for in memory SVG data:
    #handle= rsvg.Handle(None, str(<svg data>))

    handle.render_cairo(ctx)

    img.write_to_png(CFG['output_folder'] + fn + ".png")