from PIL import Image, ImageEnhance, ImageFilter
import os
import sys


def calc_size(img, width=0, height=0):

    if width == 0:
        width = img.size[0]
    if height == 0:
        height = img.size[1]

    if width < height:
        base_width = width
        width_percent = (base_width/float(img.size[0]))
        height = int((float(img.size[1])*float(width_percent)))
        return (base_width, height)
    else:
        base_height = height
        height_percent = (base_height/float(img.size[1]))
        width = int((float(img.size[0])*float(height_percent)))
        return (width, base_height)

def change_size( img, width,height):
    try:
        size = calc_size(img, width, height)
        if size[0] < 0 or size[1] < 0:
            print(img.filename)
        new_img = img.resize(size, Image.LANCZOS)
        
        return new_img
    except OSError as err:
        print(err)
        raise OSError


def sharpen(img):
    factor = 2.0
    try:
        enhancer = ImageEnhance.Sharpness(img)
        new_img = enhancer.enhance(factor)
        enhancer2 = ImageEnhance.Sharpness(new_img)
        new_img_final = enhancer2.enhance(factor)
        return new_img_final
    except OSError:
        raise OSError



