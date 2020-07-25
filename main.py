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
        new_img = img.resize(size, Image.LANCZOS)
        filename = img.filename.split("/")[-1:][0].split(".")[0]
        extension = img.format
        new_img.save(f"old_imgs/{filename}.{extension}")
    except OSError as err:
        print(err)
        raise OSError

def change_file_type(img, extension):
    #has to be a better way also check before completeing
    try:
        filename = img.filename.split("/")[-1:][0].split(".")[0]
        if extension == ".PNG" or extension == ".GIF":
            new_img = img.convert("RGBA")
            new_img.putalpha(255)
        else:
            new_img = img.convert("RGB")
        new_img.save(f"old_imgs/{filename}.{extension}", extension[1:].lower())
    except OSError:
        raise OSError

def sharpen(img):
    factor = 2.0
    try:
        enhancer = ImageEnhance.Sharpness(img)
        new_img = enhancer.enhance(factor)
        enhancer2 = ImageEnhance.Sharpness(new_img)
        new_img_final = enhancer2.enhance(factor)

        filename = img.filename.split("/")[-1:][0].split(".")[0]
        extension = img.format
        new_img_final.save(f"old_imgs/{filename}.{extension}")
    except OSError:
        raise OSError



