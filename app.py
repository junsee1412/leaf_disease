import sys, os, cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QWidget, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from gui import Ui_App
from gui import Ui_Dialog


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
        self.list_index = 0

        self.mwg.btn_directory.clicked.connect(self.select_directory)
        self.mwg.tableWidget.cellClicked.connect(self.display_images)
    
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
    
    def display_images(self):
        index = self.mwg.tableWidget.currentRow()
        file = self.list_images[index]
        Image = QPixmap(self.rootdir + '/' + file)
        Image = Image.scaled(450, 600, Qt.KeepAspectRatio)
        self.dlg.label_display.setPixmap(Image)
        self.dialog.show()

    def get_images(self):
        list_files = os.listdir(self.rootdir)
        new_list = []
        for file in list_files:
            fi, ext = os.path.splitext(file)
            if ext != '.jpg' or ext != '.png' or ext != '.jpeg':
                new_list.append(file)
        
        return new_list
    
    def show(self):
        self.main_win.show()

if __name__ == "__main__":
    app = QApplication([])
    form = App()
    form.show()
    sys.exit(app.exec_())