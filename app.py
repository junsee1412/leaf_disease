import sys, os, cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtMultimedia import QCameraInfo
from gui import Ui_App

class Camera1(QThread):
    FrameUpdate = pyqtSignal(QImage)
    def __init__(self, source="/dev/video0"):
        super().__init__()
        self.cap = cv2.VideoCapture(source)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1366)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 768)
        self.cap.set(cv2.CAP_PROP_FPS, 30)
        self.ThreadActive = False

    def run(self):
        self.ThreadActive = True
        while self.ThreadActive:
            ret, frame = self.cap.read()
            if ret:
                Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                FlippedImage = cv2.flip(Image, 1)
                ConvertToQtFormat = QImage(FlippedImage.data, FlippedImage.shape[1], FlippedImage.shape[0], QImage.Format_RGB888)
                self.FrameUpdate.emit(ConvertToQtFormat)
        self.cap.release()
    def stop(self):
        self.ThreadActive = False
        self.quit()

class App(QWidget):
    def __init__(self, ):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_App()
        self.mwg.setupUi(self.main_win)

        self.mwg.txt_path.setVisible(False)
        self.mwg.btn_path.setVisible(False)
        self.mwg.btn_path.clicked.connect(self.OpenFile)
        
        self.mwg.btn_stop.clicked.connect(self.CancelFeed)
        self.mwg.btn_play.clicked.connect(self.PlayFeed)
        
        self.LoadCamera()
        
        self.Camera1 = None

    def LoadCamera(self):
        camera = QCameraInfo()
        for i in camera.availableCameras():
            self.mwg.cb_device.addItem(i.deviceName())

    def ImageUpdateSlot(self, Image):
        Image = Image.scaled(
            self.mwg.lb_display.width(),
            self.mwg.lb_display.height(),
            Qt.KeepAspectRatio
        )
        self.mwg.lb_display.setPixmap(QPixmap.fromImage(Image))

    def CancelFeed(self):
        self.Camera1.stop()
        self.mwg.lb_display.clear()
    
    def PlayFeed(self):
        if self.mwg.r_device.isChecked():
            self.Camera1 = Camera1(self.mwg.cb_device.currentText())
        else:
            self.Camera1 = Camera1(self.mwg.txt_path.text())
        self.Camera1.FrameUpdate.connect(self.ImageUpdateSlot)
        self.Camera1.start()

    def OpenFile(self):
        home = os.path.expanduser('~')
        fname = QFileDialog.getOpenFileName(self, 'Open file', home)
        self.mwg.txt_path.setText(fname[0])

    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication([])
    form = App()
    form.show()
    sys.exit(app.exec_())