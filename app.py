import sys, os, cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from gui import Ui_App
from gui import Ui_Dialog
import numpy as np
from imutils import paths
from keras.models import load_model

class Worker(QObject):
    progress = pyqtSignal(str)
    list_pred = pyqtSignal(list)
    finished = pyqtSignal()
    def __init__(self, directory :str, model :str):
        super().__init__()
        self.rootdir = directory
        self.model = model

    @pyqtSlot()
    def run(self):
        from preprocessing import imagetoarraypreprocessor
        from preprocessing import simplepreprocessor
        from preprocessing import simpledatasetloader

        classLabels = ["Cercospora", "Healthy", "Miner", "Phoma", "Rust"]

        self.progress.emit("Nạp model mạng pre-trained ...")
        print("Nạp model mạng pre-trained ...")
        self.model = load_model(self.model)

        #Lấy danh sách các hình ảnh trong tập dữ liệu sau đó lấy mẫu ngẫu nhiên
        # ảnh theo chỉ số để đưa vào đường dẫn hình ảnh
        self.progress.emit("Đang nạp ảnh mẫu để phân lớp (dự đoán)...")
        print("Đang nạp ảnh mẫu để phân lớp (dự đoán)...")
        imagePaths = np.array(list(paths.list_images(self.rootdir))) #xác định số file trong dataset
        idxs = range(0, len(imagePaths)) # Lấy tất cả các chỉ số idxs của ảnh
        imagePaths = imagePaths[idxs]

        sp = simplepreprocessor.SimplePreprocessor(32, 32) # Thiết lập kích thước ảnh 32 x 32
        iap = imagetoarraypreprocessor.ImageToArrayPreprocessor() # Gọi hàm để chuyển ảnh sang mảng


        # Nạp dataset từ đĩa rồi co dãn mức xám của pixel trong vùng [0,1]
        sdl = simpledatasetloader.SimpleDatasetLoader(preprocessors=[sp, iap])
        (data, labels) = sdl.load(imagePaths)
        data = data.astype("float") / 255.0

        # Dự đoán
        self.progress.emit("Đang dự đoán...")
        print("Đang dự đoán...")
        preds = self.model.predict(data, batch_size=32).argmax(axis=1)

        # Lặp qua tất cả các file ảnh trong imagePaths
        # Nạp ảnh ví dụ --> Vẽ dự đoán --> Hiển thị ảnh
        text_preds = [classLabels[pred] for pred in preds]

        self.list_pred.emit(text_preds)
        self.finished.emit()
    

class App(QWidget):
    def __init__(self, ):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_App()
        self.mwg.setupUi(self.main_win)

        self.dlg = Ui_Dialog()
        self.dialog = QDialog()
        self.dlg.setupUi(self.dialog)

        self.rootdir = None
        self.list_images = None
        self.model = "modVGGNet.hdf5"

        self.mwg.btn_directory.clicked.connect(self.select_directory)
        self.mwg.btn_model.clicked.connect(self.select_model)
        self.mwg.tableWidget.cellClicked.connect(self.display_images)
        self.mwg.btn_predict.clicked.connect(self.process_start)
    
    def select_model(self):
        self.model, _ = QFileDialog.getOpenFileName(self.main_win, 'Select Model', '', '*.hdf5')
        self.mwg.lineModel.setText(self.model)

    def select_directory(self):
        self.rootdir = QFileDialog.getExistingDirectory(self.main_win, 'Select Directory')
        try:
            self.mwg.linePath.setText(self.rootdir)
            self.list_images = self.get_images()
            self.show_table_widget()
        except Exception as e:
            print(e)
            self.mwg.statusbar.showMessage(f'Error: {e}', 5000)
    
    def show_table_widget(self):
        self.mwg.tableWidget.setRowCount(len(self.list_images))
        for i in range(len(self.list_images)):
            item = self.list_images[i]
            self.mwg.tableWidget.setItem(i, 0, QTableWidgetItem(item))
            self.mwg.tableWidget.setItem(i, 1, QTableWidgetItem(os.path.join(self.rootdir ,item)))
            self.mwg.tableWidget.setItem(i, 2, QTableWidgetItem(''))

    def display_images(self):
        index = self.mwg.tableWidget.currentRow()
        file = self.list_images[index]
        Image = QPixmap(self.rootdir + '/' + file)
        Image = Image.scaled(450, 600, Qt.KeepAspectRatio)
        
        self.dlg.label_display.setPixmap(Image)
        self.dlg.label_disease.setText(self.mwg.tableWidget.item(index, 2).text())
        self.dialog.show()

    def get_images(self):
        list_files = os.listdir(self.rootdir)
        print(self.rootdir)
        new_list = []
        for file in list_files:
            fi, ext = os.path.splitext(file)
            if ext != '.jpg' or ext != '.png' or ext != '.jpeg':
                new_list.append(file)
        
        return new_list
    
    def show(self):
        self.main_win.show()

    def process_start(self):
        self.worker = Worker(self.rootdir, self.model)
        self.thread_pred = QThread()
        self.worker.moveToThread(self.thread_pred)

        self.worker.progress.connect(self.mwg.statusbar.showMessage)
        self.worker.list_pred.connect(self.set_preds)
        self.worker.finished.connect(self.process_done)

        self.thread_pred.started.connect(self.worker.run)

        self.thread_pred.start()
    
    @pyqtSlot(list)
    def set_preds(self, preds :list):
        for (i, pred) in enumerate(preds):
            self.mwg.tableWidget.setItem(i, 2, QTableWidgetItem(pred))
    
    @pyqtSlot()
    def process_done(self):
        self.mwg.statusbar.showMessage("Done!", 5000)
        self.thread_pred.quit()

if __name__ == "__main__":
    app = QApplication([])
    form = App()
    form.show()
    sys.exit(app.exec_())
