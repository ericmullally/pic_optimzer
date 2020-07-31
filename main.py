from PIL import Image, ImageEnhance, ImageFilter
import os
import sys
import math
from PyQt5 import QtCore

# have to make this a class somehow
class Main(QtCore.QObject):
    progress_signal = QtCore.pyqtSignal(int)
    def calc_size(self, img, width=0, height=0):

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

    def change_size(self, img, width,height):
        try:
            size = self.calc_size(img, width, height)
            new_img = img.resize(size, Image.LANCZOS)  
            return new_img
        except OSError as err:
            print(err)
            raise OSError


    def sharpen(self, img):
        factor = 2.0
        try:
            enhancer = ImageEnhance.Sharpness(img)
            new_img = enhancer.enhance(factor)
            enhancer2 = ImageEnhance.Sharpness(new_img)
            new_img_final = enhancer2.enhance(factor)
            return new_img_final
        except OSError:
            raise OSError

    @QtCore.pyqtSlot(str, bool, str, tuple)
    def convertion_loop(self, folder_path, sharpen, ext, size_tuple): 
       
        # need to handle not all files being photos
        pic_strings = os.listdir(folder_path)
        pic_files = (Image.open(f"{folder_path}/{img}")  for img in pic_strings if os.path.splitext(img)[1] != ".ini")

        if not os.path.exists("C:/Users/Eric/Desktop/coverted pics"):
                os.mkdir("C:/Users/Eric/Desktop/coverted pics")

        for i, img in enumerate(pic_files):
            progress_val = (i + 1)*100/len(pic_strings)
            filename = img.filename.split("/")[-1:][0].split(".")[0]
            original_extension = img.format
            
            if size_tuple[0] != None or size_tuple[1] != None:
                height, width = size_tuple
                try:
                    img = self.change_size(img, width, height)
                    img.format = original_extension
                except Exception as ex:
                    with open("error_logs/error.txt", "w") as error_log:
                        error_log.write(f"{filename} failed to resize:  {ex}")
                    img.save(f"error_pics/{filename}.{original_extension}")
                    continue
    
            if sharpen == True:
                try:
                    img = self.sharpen(img)
                    img.format = original_extension
                except Exception as ex:
                    with open("error_logs/error.txt", "w") as error_log:
                        error_log.write(f"{filename} failed to resize:  {ex}")
                    img.save(f"error_pics/{filename}.{original_extension}")
                    continue

            if ext != "":
                if ext == ".PNG" or ext== ".GIF" or ext== ".ICO":
                    img = img.convert("RGBA")
                    img.putalpha(255)
                    extension = ext
                else:
                    img = img.convert("RGB")   
                    extension = ext     
            else:
                extension = "." + img.format

            try:
                img.save(f"C:/Users/Eric/Desktop/coverted pics/new{filename}{extension.lower()}", extension[1:].capitalize() )
            except Exception as ex:
                with open("error_logs/error.txt", "w") as error_log:
                    error_log.write(f"{filename} failed to resize:  {ex}")
                    img.save(f"error_pics/{filename}.{original_extension}")
                continue
            
            self.progress_signal.emit(math.ceil(progress_val))
        self.progress_signal.emit(0)
        
            
    
  