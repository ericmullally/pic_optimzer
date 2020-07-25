# Check if you want the photos to be enhanced
# dropdown choice for file types to be turned into
# text box for measurment of resize on photos.
# one check box for turning photos into icons which includes enhancement and file change.
import os, sys
from PIL import Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from main import change_size, change_file_type, sharpen 

Ui_MainWindow, main_baseClass = uic.loadUiType("Main_window.ui")
class MainWindow(main_baseClass):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.ui.widthInput.setEnabled(False)
      self.ui.heightInput.setEnabled(False)
      self.ui.actionresize.triggered.connect(self.toggle_size)
      self.ui.choose_file_button.clicked.connect(self.choose_folder)
      self.ui.convert_btn.clicked.connect(self.pic_convert)
      self.ui.convert_btn.setEnabled(False)

      self.file_start_path ="C:\\Users\\Eric\\Documents"
      self.folder_path = ""
      self.show()

   def toggle_size(self):
      if self.ui.actionresize.isChecked():
         self.ui.heightInput.setEnabled(True)
         self.ui.widthInput.setEnabled(True)
      else:
         self.ui.heightInput.setEnabled(False)
         self.ui.widthInput.setEnabled(False)


   def choose_folder(self):
      file_win = QtWidgets.QFileDialog.getExistingDirectory(None,"Select folder",f'{self.file_start_path}' )
      # go through selected folder and make sure there are pictures inside
      # if there are set self.folder_path to the path 
      file_extensions = [".bmp",".gif", ".ico",".jpeg", ".jpg", ".png"]
      
      if file_win == "":
         return
      else:
         files = os.listdir(file_win)

      pic_count = 0
      for item in files:
         
         if "." in item:
            extension =  os.path.splitext(item)[1]
            if extension.lower() in file_extensions:
              pic_count += 1
            else:
               continue
         else:
            continue
      
      if pic_count > 0:
         self.folder_path = file_win
         self.ui.convert_btn.setEnabled(True)
      else:
         no_pics_error_box = QtWidgets.QMessageBox(self)
         no_pics_error_box.setText("No photos found")
         no_pics_error_box.show()

   def pic_convert(self):
      if self.folder_path != "":
         pic_strings = os.listdir(self.folder_path)
         pic_files = [Image.open(f"{self.folder_path}/{img}") for img in pic_strings]

         if self.ui.actionchangeType.isChecked():
            if self.ui.fileTypeSelector.currentText() != "None":
               for pic in pic_files:
                  change_file_type(pic,self.ui.fileTypeSelector.currentText() )
            else:
               change_extension_error = QtWidgets.QMessageBox(self)
               change_extension_error.setText("Please select an extension.")
               change_extension_error.show()
               return
         
         if self.ui.actionresize.isChecked():
            if self.ui.heightInput.value() != 0 or self.ui.widthInput.value() != 0:
               height = self.ui.heightInput.value()
               width = self.ui.widthInput.value()
               for pic in pic_files:
                  change_size(pic, width, height)
            else:
               size_error_box = QtWidgets.QMessageBox(self)
               size_error_box.setText("You must provide height, width or both.")
               size_error_box.show()
               return


         if self.ui.actionsharpen.isChecked():
            for pic in pic_files:
               sharpen(pic)

         imgs_final_list = os.listdir("old_imgs")
         if len(imgs_final_list) > 0:
            for img in imgs_final_list:
               final_img = Image.open(f"old_imgs/{img}")
               final_img.save(f"output_file/new{img}")
               os.remove(f"old_imgs/{img}")
         
           
      else:
         no_file_selected_error_box = QtWidgets.QMessageBox(self)
         no_file_selected_error_box.setText("Please select a file")
         no_file_selected_error_box.show()

            
      


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())