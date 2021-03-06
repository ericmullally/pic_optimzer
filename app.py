
import os, sys
from PIL import Image, ImageFile
from PyQt5 import QtCore, QtWidgets, QtGui, uic
from main import Main

ImageFile.LOAD_TRUNCATED_IMAGES = True

Ui_MainWindow, main_baseClass = uic.loadUiType("Main_window.ui")

class MainWindow(main_baseClass):
   signal_start_background_job = QtCore.pyqtSignal(str, dict, str, tuple, int)
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.ui = Ui_MainWindow()
      self.ui.setupUi(self)
      self.ui.widthInput.setEnabled(False)
      self.ui.heightInput.setEnabled(False)
      self.ui.fileTypeSelector.setEnabled(False)
      self.ui.fileTypeSelector.currentTextChanged.connect(self.enableSlider)
      self.ui.transparencySlider.valueChanged.connect(self.sliderChange)
      self.ui.transparencySlider.setEnabled(False)

      self.ui.actionresize.triggered.connect(self.toggle_size)
      self.ui.actionchangeType.triggered.connect(self.change_type)
      self.ui.actionsharpen.triggered.connect(self.sharpen_activated)

      self.ui.choose_file_button.clicked.connect(self.choose_folder)
      self.ui.convert_btn.clicked.connect(self.pic_convert)
      self.ui.convert_btn.setEnabled(False)
      self.ui.progressBar.setValue(0)

      self.worker = Main()
      self.thread = QtCore.QThread()
      self.worker.moveToThread(self.thread)
      self.worker.progress_signal.connect(self.update_progress)
      self.worker.finish_signal.connect(self.finish_display)
     
      self.file_start_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents') 
      self.folder_path = ""
      self.extension = ""
      self.size_tuple = (None, None)
      self.signal_start_background_job.connect(self.worker.convertion_loop)
      self.alphaValue = 255
      self.state = {"change_size": False, "sharpen": False, "change_type": False}
      self.show()

   def toggle_size(self):
      if self.ui.actionresize.isChecked():
         self.ui.heightInput.setEnabled(True)
         self.ui.widthInput.setEnabled(True)
         self.state["change_size"] = True
      else:
         self.ui.heightInput.setEnabled(False)
         self.ui.widthInput.setEnabled(False)
         self.state["resize"] = False

   def change_type(self):
      if self.ui.actionchangeType.isChecked():
         self.ui.fileTypeSelector.setEnabled(True)
         self.state["change_type"] = True
      else:
         self.ui.fileTypeSelector.setEnabled(False)
         self.state["change_type"] = False
  
   def enableSlider(self):
      alphaTypes = [".GIF", ".ICO", ".PNG"]
      if self.ui.fileTypeSelector.currentText() in alphaTypes:
         self.ui.transparencySlider.setEnabled(True)
      else:
         self.ui.transparencySlider.setEnabled(False)

   def sliderChange(self):
      self.ui.imgLabel.setStyleSheet(f"color: rgba(0,0,0,{self.ui.transparencySlider.value()})")
      self.alphaValue = self.ui.transparencySlider.value()

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

   def sharpen_activated(self):
      if self.ui.actionsharpen.isChecked():
         self.state["sharpen"] = True
      else:
         self.state["sharpen"] = False

   def pic_convert(self):
      if self.folder_path != "":
         if self.ui.actionchangeType.isChecked():
            if self.ui.fileTypeSelector.currentText() != "None":
               self.extension = self.ui.fileTypeSelector.currentText()
            else:
               extension_error_box = QtWidgets.QMessageBox(self)
               extension_error_box.setText("Please select an extension.")
               extension_error_box.show()
               return
         else:
            self.extension = ""

         if self.ui.actionresize.isChecked() == True:
            if self.ui.heightInput.value() != 0 or self.ui.widthInput.value() != 0:
               height = self.ui.heightInput.value()
               width = self.ui.widthInput.value()  
               self.size_tuple = (height, width)            
            else:
               size_error_box = QtWidgets.QMessageBox(self)
               size_error_box.setText("You must provide height, width or both.")
               size_error_box.show()
               return
         else:
            self.size_tuple = (None, None)
         

         self.thread.start()
         self.signal_start_background_job.emit(self.folder_path, self.state, self.extension, self.size_tuple, self.alphaValue)
      else:
        no_file_selected_error_box = QtWidgets.QMessageBox(self)
        no_file_selected_error_box.setText("Please select a file")
        no_file_selected_error_box.show()

   @QtCore.pyqtSlot(int)
   def update_progress(self, progress):
      self.ui.progressBar.setValue(progress)

   @QtCore.pyqtSlot(bool)
   def finish_display(self, status):
      if status == True:
         success_message = QtWidgets.QMessageBox(self)
         success_message.setText("Finished with no errors!")
         success_message.show()
      else:
         photo_error_box = QtWidgets.QMessageBox(self)
         photo_error_box.setText("not all files converted, check error logs.")
         photo_error_box.show()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec_())