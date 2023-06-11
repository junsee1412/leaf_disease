import sys, os, cv2
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QImage, QPixmap
from gui import Ui_App


class App(QWidget):
    def __init__(self, ):
        super().__init__()
        self.main_win = QMainWindow()
        self.mwg = Ui_App()
        self.mwg.setupUi(self.main_win)
        self.rootdir = None
        self.list_images = None
        self.list_index = 0

        self.mwg.btn_directory.clicked.connect(self.select_directory)
        self.mwg.tableWidget.cellClicked.connect(self.cell_current)
    
    def cell_current(self):
        current_row = self.mwg.tableWidget.currentRow()
        print(current_row)
    
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
        # self.mwg.tableWidget.currentColumn()
        for i in range(len(self.list_images)):
            item = QTableWidgetItem(self.list_images[i])
            self.mwg.tableWidget.setItem(i, 0, item)
    
    def display_images(self):
        file = self.list_images[self.list_index]
        Image = QPixmap(self.rootdir + '/' + file)
        Image = Image.scaled(
            self.mwg.lb_display.width(),
            self.mwg.lb_display.height(),
            Qt.KeepAspectRatio
        )
        self.mwg.lb_display.setPixmap(Image)

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