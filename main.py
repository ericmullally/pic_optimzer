from PIL import Image, ImageEnhance, ImageFilter
import os
import sys
import math
from PyQt5 import QtCore

class Main(QtCore.QObject):
    progress_signal = QtCore.pyqtSignal(int)
    finish_signal = QtCore.pyqtSignal(bool)
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    
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

    def change_size(self, img, size_tuple):
        height, width = size_tuple
        try:
            size = self.calc_size(img, width, height)
            new_img = img.resize(size, Image.LANCZOS)  
            return new_img
        except OSError as err:
            print(err)
            raise OSError

    @QtCore.pyqtSlot(str, dict, str, tuple, int)
    def convertion_loop(self, folder_path, state, ext, size_tuple, alpha): 
        file_extensions = [".bmp",".gif", ".ico",".jpeg", ".jpg", ".png"]
        alpha_extensions = [".GIF", ".ICO", ".PNG"]
        
        
        pic_strings = os.listdir(folder_path)
        pic_files = (Image.open(f"{folder_path}/{img}")  for img in pic_strings if os.path.splitext(img)[1] in file_extensions)

        for i, img in enumerate(pic_files):
            progress_val = (i + 1)*100/len(pic_strings)
            filename = img.filename.split("/")[-1:][0].split(".")[0]
            original_extension = img.format
            
            if (ext in alpha_extensions) and img.mode != "RGBA":
                    img = img.convert("RGBA")
                    img.putalpha(alpha)
            elif (ext not in alpha_extensions) and img.mode == "RGBA":
                    img.load() 
                    background = Image.new("RGB", img.size, (0, 0, 0))
                    img.paste(background, mask=img.split()[2]) 
                    img.mode = "RGB"
                    img.show()

            if ext == ".ICO":
                try:
                    self.convert_icon(img, original_extension, size_tuple, alpha, filename)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # change size only
            elif state["change_size"] and not state["sharpen"] and not state["change_type"] :
                try:
                    new_pic = self.change_size(img, size_tuple)
                    self.save_pic(new_pic, filename, original_extension)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # sharpen only
            elif state["sharpen"] and not state["change_size"] and not state["change_type"]: 
                try:
                    new_pic = self.sharpen(img, filename)
                    self.save_pic(new_pic, filename, original_extension)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # change type only
            elif state["change_type"] and not state["change_size"] and not state["sharpen"]: 
                try:
                    new_pic = self.change_type(img, filename, ext)
                    self.save_pic(new_pic, filename, ext)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # sharpen and change size only
            elif state["sharpen"] and state["change_size"] and not state["change_type"]:
                try:
                    new_pic = self.change_size(self.sharpen(img, filename), size_tuple)
                    self.save_pic(new_pic, filename, original_extension )
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # change type and change size only
            elif state["change_type"] and state["change_size"] and not state["sharpen"]:
                try:
                    new_pic = self.change_type(self.change_size(img, size_tuple), filename, ext)
                    self.save_pic(new_pic, filename, ext)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # change type and sharpen
            elif state["change_type"] and state["sharpen"] and not state["change_size"]:
                try:
                    new_pic = self.change_type(self.sharpen(img, filename), filename, ext)
                    self.save_pic(new_pic, filename, ext)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            # all actions
            elif state["change_type"] and state["sharpen"] and state["change_size"]:
                try:
                    new_pic = self.change_size(self.change_type(self.sharpen(img, filename), filename, ext),  size_tuple)
                    self.save_pic(new_pic, filename, ext)
                    self.progress_signal.emit(progress_val)
                    continue
                except:
                    continue
            else:
                print("you forgot something")
                break
        self.progress_signal.emit(0)    
        self.report_finished()

    def report_finished(self):
        if len(os.listdir("error_pics")) > 0:
            self.finish_signal.emit(False)
        else:
            self.finish_signal.emit(True)

    def convert_icon(self, img, ext, size_tuple, alpha, filename):
        
        try:
            if size_tuple[0] != None or size_tuple[1] != None:
                height, width = size_tuple
                sizes = [ (height,height) if height != 0 else (width,width) ]
            else:
                sizes = [(256, 256)]
            img.save(f"{self.desktop}/coverted pics/new {filename}.ico", sizes =sizes )
            return
        except Exception as ex:
            if "." in ext:
                ext = ext[1:]
            with open("error_logs/error.txt", "w") as error_log:
                error_log.write(f"{filename} failed to resize:  {ex}")
            img.save(f"error_pics/{filename}.{ext.lower()}")
            return

    def change_type(self, img, filename, ext):
        original_extension = img.format
        try:
            img.format = ext
            return img
        except Exception as ex:
            with open("error_logs/error.txt", "w") as error_log:
                error_log.write(f"{filename} failed to format:  {ex}")
            img.save(f"error_pics/{filename}.{original_extension}")
            return
        
    def sharpen(self, img , filename):
        original_extension = img.format
        factor = 2.0
        try:
            enhancer = ImageEnhance.Sharpness(img)
            new_img = enhancer.enhance(factor)
            enhancer2 = ImageEnhance.Sharpness(new_img)
            new_img_final = enhancer2.enhance(factor)
            return new_img_final
        except Exception as ex:
            with open("error_logs/error.txt", "w") as error_log:
                error_log.write(f"{filename} failed to sharpen:  {ex}")
            img.save(f"error_pics/{filename}.{original_extension}")
            return

    def save_pic(self, img, filename, extension):

        if "." in extension:
            extension = extension[1:]
        
        if not os.path.exists(f"{self.desktop}/coverted pics"):
                os.mkdir(f"{self.desktop}/coverted pics")

        try:
            img.save(f"{self.desktop}/coverted pics/new {filename}.{extension.lower()}", extension.upper() )
        except Exception as ex:
            with open("error_logs/error.txt", "w") as error_log:
                error_log.write(f"{filename} failed to save:  {ex}")
            img.save(f"error_pics/{filename}.{extension.lower()}")
            return
                