import sys, serial, time, os, json
from PyQt5.QtWidgets import (
    QLabel, 
    QVBoxLayout, 
    QPushButton,
    QDialog,
)
from PyQt5.QtGui import (
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt,
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

class BackwashFlashingMenu(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Backwash Flashing Menu")
        self.setFixedSize(280, 150)
        self.initUI()

    def initUI(self):
        # Warna latar belakang RGB
        self.red = 135
        self.green = 206
        self.blue = 235
        self.background_color = QColor(self.red, self.green, self.blue)

        # Atur warna latar belakang GUI
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(palette)

        vbox = QVBoxLayout()
        label_info = QLabel("Proses Sirkulasi Air")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        button_backwash = QPushButton("Backwash")
        button_flashing = QPushButton("Flashing")
        #button_backwash.clicked.connect(self.close)

        vbox.addWidget(button_backwash)
        vbox.addWidget(button_flashing)

        # when click button
        button_backwash.clicked.connect(self.sendDataBackwash)
        button_flashing.clicked.connect(self.senDataFlashing)

        self.setLayout(vbox)
    
    def sendDataBackwash(self):
        data = 'Backwash'
        print(data)
        dialog = popupInfo(data)
        dialog.exec_()
        
    def senDataFlashing(self):
        data= 'Flashing'
        print(data)
        dialog = popupInfo(data)
        dialog.exec_()

class popupInfo(QDialog):
    def __init__(self, info):
        super().__init__()
        self.setWindowTitle("Informasi")
        self.setFixedSize(280, 150)
        self.initUI(info)

    def initUI(self, info):
        # Warna latar belakang RGB
        self.red = 135
        self.green = 206
        self.blue = 235
        self.background_color = QColor(self.red, self.green, self.blue)

        # Atur warna latar belakang GUI
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), self.background_color)
        self.setPalette(palette)

        vbox = QVBoxLayout()
        label_tumbler_data = QLabel(f"Proses {info}")
        label_tumbler_data.setAlignment(Qt.AlignCenter)
        label_tumbler_data.setFont(QFont("Arial", 22, QFont.Bold))
        vbox.addWidget(label_tumbler_data)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)
