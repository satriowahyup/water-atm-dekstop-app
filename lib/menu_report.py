import sys
import csv
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QApplication, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QScrollArea, QDesktopWidget
from PyQt5.QtGui import (
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class ReportMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Report Pengisian Air")
        self.initUI()

    def initUI(self):
        self.vbox = QVBoxLayout()
        self.scroll = QScrollArea()
        self.vbox.addWidget(self.scroll)
        self.setLayout(self.vbox)

        path = '/home/satrio/Documents/Data Laptop Asus - Satrio/Satrio/Personal Project/Water ATM/desktop-app/report.csv'  # Ganti dengan path sesuai dengan direktori Anda
        with open(path, 'r') as file_csv:
            data = list(csv.reader(file_csv))
            header = data[0]
            data_terbalik = [header] + list(reversed(data[1:]))
            self.tampilkan_data(data_terbalik)

        self.setFixedSize(890, 1000)  # Atur ukuran jendela sesuai keinginan Anda
        self.center()
    
    def center(self):
        frame_info = self.frameGeometry()
        layar_tengah = QDesktopWidget().availableGeometry().center()
        frame_info.moveCenter(layar_tengah)
        self.move(frame_info.topLeft())

    def tampilkan_data(self, data):
        self.table_widget = QTableWidget()
        self.table_widget.setRowCount(len(data))
        self.table_widget.setColumnCount(len(data[0]))

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                item = QTableWidgetItem(col)
                font = QFont()
                font.setPointSize(19)  # Atur ukuran font sesuai keinginan Anda
                item.setFont(font)
                self.table_widget.setItem(i, j, item)

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        self.scroll.setWidget(self.table_widget)
        self.scroll.setWidgetResizable(True)
