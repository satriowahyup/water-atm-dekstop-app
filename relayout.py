import sys
import json
import serial
import time
import threading
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QMessageBox, 
    QPushButton,
    QDialog,
    QLineEdit,
    QGridLayout
)
from PyQt5.QtGui import (
    QPixmap, 
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt, 
    QTimer
)

class GalonPopup(QDialog):
    def __init__(self, galon_data):
        super().__init__()
        self.setWindowTitle("Air Galon")
        self.setFixedSize(280, 150)
        self.initUI(galon_data)

    def initUI(self, galon_data):
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

        label_info = QLabel("Proses Pengisian Air")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_title = QLabel("Jumlah Air Terisi")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Arial", 14))
        vbox.addWidget(label_title)

        label_galon_data = QLabel(f"{galon_data} L")
        label_galon_data.setAlignment(Qt.AlignCenter)
        label_galon_data.setFont(QFont("Arial", 22, QFont.Bold))
        vbox.addWidget(label_galon_data)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)

#Menu Tumbler
class TumnlerPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Proses Pengisian Air Tumbler")
        self.setFixedSize(370, 300)
        self.initUI()
        self.serial = None  # Objek serial untuk komunikasi dengan Arduino

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
        self.label_input = QLabel("Masukkan Jumlah mL Air")
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setFont(QFont("Arial", 18, QFont.Bold))
        vbox.addWidget(self.label_input)

        self.line_edit = QLineEdit()
        vbox.addWidget(self.line_edit)

        self.grid_layout = QGridLayout()

        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(self.add_digit)
            self.grid_layout.addWidget(button, (i-1)//3, (i-1)%3)

        button_comma = QPushButton(".")
        button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(button_comma, 3, 0)

        button_0 = QPushButton("0")
        button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_0, 3, 1)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 3, 2)

        vbox.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        #self.button_enter.clicked.connect(self.send_data_to_arduino)
        self.button_enter.clicked.connect(self.readData)
        self.button_enter.clicked.connect(self.showStatusTumblerPopup)
        vbox.addWidget(self.button_enter)

        self.setLayout(vbox)
        self.digits = ""
    
    def add_digit(self):
        sender = self.sender()
        self.digits += sender.text()
        self.line_edit.setText(self.digits)

    def add_comma(self):
        if "." not in self.digits:
            self.digits += "."
            self.line_edit.setText(self.digits)

    def clear_digits(self):
        self.digits = ""
        self.line_edit.setText(self.digits)

    def send_data_to_arduino(self, liter):
        total_liter = liter
        # Kirim data total liter ke Arduino menggunakan komunikasi serial
        print(f"Mengirim data total liter: {total_liter} ke Arduino")
    
    def showStatusTumblerPopup(self):
        # Simulasikan data jumlah liter air terisi pada galon
        tumbler_data = self.line_edit.text()
        if int(tumbler_data) > 1000:
            info = "Melebihi Batas Maksimum"
            dialog = FailedTransactionPopup(info)
            dialog.exec_()
        else:
            dialog = StstusPengisianTumbler(int(tumbler_data))
            dialog.exec_()
    
    def readData(self):
        data = self.line_edit.text()
        print("Data : ", data)

class StstusPengisianTumbler(QDialog):
    def __init__(self, galon_data):
        super().__init__()
        self.setWindowTitle("Air Tumbler")
        self.setFixedSize(280, 150)
        self.initUI(galon_data)

    def initUI(self, galon_data):
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
        label_info = QLabel("Proses Pengisian Air")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_title = QLabel("Jumlah Air Terisi")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Arial", 14))
        vbox.addWidget(label_title)

        label_tumbler_data = QLabel(f"{galon_data} mL")
        label_tumbler_data.setAlignment(Qt.AlignCenter)
        label_tumbler_data.setFont(QFont("Arial", 22, QFont.Bold))
        vbox.addWidget(label_tumbler_data)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)

class FailedTransactionPopup(QDialog):
    def __init__(self, info_machine):
        super().__init__()
        self.setWindowTitle("Transaksi Gagal")
        self.setFixedSize(230, 110)

        vbox = QVBoxLayout()
        label_transaksi = QLabel("Pengisian Air Gagal")
        label_transaksi.setAlignment(Qt.AlignCenter)
        label_transaksi.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label_transaksi)

        label_info_machine = QLabel(f"{info_machine}")
        label_info_machine.setAlignment(Qt.AlignCenter)
        label_info_machine.setFont(QFont("Arial", 11, QFont.Bold))
        vbox.addWidget(label_info_machine)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)

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

class PasswordPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Masukan Password")
        self.setFixedSize(370, 300)
        self.initUI()
        self.serial = None  # Objek serial untuk komunikasi dengan Arduino

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
        self.label_input = QLabel("Masukkan Jumlah Password")
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setFont(QFont("Arial", 18, QFont.Bold))
        vbox.addWidget(self.label_input)

        self.line_edit = QLineEdit()
        vbox.addWidget(self.line_edit)

        self.grid_layout = QGridLayout()

        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(self.add_digit)
            self.grid_layout.addWidget(button, (i-1)//3, (i-1)%3)

        button_comma = QPushButton(".")
        button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(button_comma, 3, 0)

        button_0 = QPushButton("0")
        button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_0, 3, 1)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 3, 2)

        vbox.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        self.button_enter.clicked.connect(self.showStatusTumblerPopup)
        vbox.addWidget(self.button_enter)

        self.setLayout(vbox)
        self.digits = ""
    
    def add_digit(self):
        sender = self.sender()
        self.digits += sender.text()
        self.line_edit.setText(self.digits)

    def add_comma(self):
        if "." not in self.digits:
            self.digits += "."
            self.line_edit.setText(self.digits)

    def clear_digits(self):
        self.digits = ""
        self.line_edit.setText(self.digits)
    
    def showStatusTumblerPopup(self):
        # Simulasikan data jumlah liter air terisi pada galon
        tumbler_data = 160
        if tumbler_data > 1000:
            info = "Air Kurang Berkualitas"
            dialog = FailedTransactionPopup(info)
            dialog.exec_()
        else:
            dialog = StstusPengisianTumbler(tumbler_data)
            dialog.exec_()

## menu settings
class SettingsMenu(QDialog):
    def __init__(self,):
        super().__init__()
        self.setWindowTitle("Menu Settings")
        self.setFixedSize(350, 340)
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
        label_info = QLabel("Masukan Settings Parameter")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_id = QLabel("ID Mesin: 000001")
        label_id.setAlignment(Qt.AlignCenter)
        label_id.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label_id)

        label_ph = QLabel("Setting pH Threshold")
        label_ph.setAlignment(Qt.AlignCenter)
        label_ph.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label_ph)
        self.line_edit_ph = QLineEdit()
        vbox.addWidget(self.line_edit_ph)

        self.grid_layout = QGridLayout()

        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(self.add_digit)
            self.grid_layout.addWidget(button, (i-1)//3, (i-1)%3)

        button_comma = QPushButton(".")
        button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(button_comma, 3, 0)

        button_0 = QPushButton("0")
        button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_0, 3, 1)

        button_backspace = QPushButton("<")
        button_backspace.clicked.connect(self.backspace_digits)
        self.grid_layout.addWidget(button_backspace, 3, 2)

        button_minus = QPushButton("-")
        button_minus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_minus, 4, 0)

        button_plus = QPushButton("+")
        button_plus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_plus, 4, 1)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 4, 2)

        vbox.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        self.button_enter.clicked.connect(self.nextSettingTurbidity)
        vbox.addWidget(self.button_enter)

        self.setLayout(vbox)
        self.digits = ""
    
    def add_digit(self):
        sender = self.sender()
        self.digits += sender.text()
        self.line_edit_ph.setText(self.digits)

    def add_comma(self):
        if "." not in self.digits:
            self.digits += "."
            self.line_edit_ph.setText(self.digits)

    def backspace_digits(self):
        self.digits = ""
        self.line_edit_ph.backspace()
    
    def clear_digits(self):
        self.digits = ""
        self.line_edit_ph.setText(self.digits)

    def nextSettingTurbidity(self):
        # Simulasikan data jumlah liter air terisi pada galon
        data_ph = self.line_edit_ph.text()
        dialog = TurbiditySettingsMenu(data_ph)
        dialog.exec_()

class TurbiditySettingsMenu(QDialog):
    def __init__(self, data_ph):
        super().__init__()
        self.setWindowTitle("Menu Settings")
        self.setFixedSize(350, 340)
        self.initUI(data_ph)

    def initUI(self, data_ph):
        print("data ph : ", data_ph)
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
        label_info = QLabel("Masukan Settings Parameter")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_id = QLabel("ID Mesin: 000001")
        label_id.setAlignment(Qt.AlignCenter)
        label_id.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label_id)

        label_turbidity = QLabel("Setting Turbidity Threshold")
        label_turbidity.setAlignment(Qt.AlignCenter)
        label_turbidity.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label_turbidity)
        self.line_edit_turbidity = QLineEdit()
        vbox.addWidget(self.line_edit_turbidity)

        self.grid_layout = QGridLayout()

        for i in range(1, 10):
            button = QPushButton(str(i))
            button.clicked.connect(self.add_digit)
            self.grid_layout.addWidget(button, (i-1)//3, (i-1)%3)

        button_comma = QPushButton(".")
        button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(button_comma, 3, 0)

        button_0 = QPushButton("0")
        button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_0, 3, 1)

        button_backspace = QPushButton("<")
        button_backspace.clicked.connect(self.backspace_digits)
        self.grid_layout.addWidget(button_backspace, 3, 2)

        button_minus = QPushButton("-")
        button_minus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_minus, 4, 0)

        button_plus = QPushButton("+")
        button_plus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_plus, 4, 1)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 4, 2)

        vbox.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        #self.button_enter.clicked.connect(self.closeAllPopups)
        vbox.addWidget(self.button_enter)

        self.setLayout(vbox)
        self.digits = ""
    
    def add_digit(self):
        sender = self.sender()
        self.digits += sender.text()
        self.line_edit_turbidity.setText(self.digits)

    def add_comma(self):
        if "." not in self.digits:
            self.digits += "."
            self.line_edit_turbidity.setText(self.digits)

    def backspace_digits(self):
        self.line_edit_turbidity.backspace()
    
    def clear_digits(self):
        self.digits = ""
        self.line_edit_turbidity.setText(self.digits)
    
    def closeAllPopups(self):
        self.parent().close()
        self.parent().parent().close()


# Main WIndow
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mulai Hidup Sehat dengan Air Berkualitas")
        self.setGeometry(5, 5, 1920, 1080)

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

        self.layout = QVBoxLayout()

        # Label untuk status machine
        self.label_machine = QLabel("Machine : -",self)
        self.label_machine.setGeometry(10, 5, 250, 25)
        self.label_machine.setFont(QFont("Arial", 15))
        self.label_machine.setAlignment(Qt.AlignLeft)
        self.label_machine.setStyleSheet("color: white")

        # Label untuk status water
        self.label_water = QLabel("Water : -",self)
        self.label_water.setGeometry(1070, 5, 250, 25)
        self.label_water.setFont(QFont("Arial", 15))
        self.label_water.setAlignment(Qt.AlignRight)
        self.label_water.setStyleSheet("color: white")

        # Judul
        self.title_label = QLabel("Mulai Hidup Sehat dengan Air Berkualitas", self)
        self.title_label.setGeometry(260, 30, 770, 40)
        self.title_label.setFont(QFont("Arial", 28, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: black")

        # Gambar mata air
        self.water_image = QPushButton(self)
        self.water_image.setGeometry(285, 90, 670, 300)
        self.water_image.setStyleSheet("QPushButton { border-image: url(water-icon.png) 0 0 0 0 stretch stretch; }")

        # Tombol transaksi air galon
        self.galon_button = QPushButton(self)
        self.galon_button.setGeometry(40, 350, 400, 300)  # Atur posisi dan ukuran tombol
        self.galon_button.setStyleSheet("QPushButton { border-image: url(galon.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air galon
        self.label_galon = QLabel("Air Galon",self)
        self.label_galon.setGeometry(168, 630, 150, 40)
        self.label_galon.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_galon.setAlignment(Qt.AlignCenter)

        # Tombol transaksi air tumbler
        self.tumbler_button = QPushButton(self)
        self.tumbler_button.setGeometry(860,365, 330, 280)
        self.tumbler_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler
        self.label_tumbler = QLabel("Air Tumbler",self)
        self.label_tumbler.setGeometry(940, 630, 200, 40)
        self.label_tumbler.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_tumbler.setAlignment(Qt.AlignCenter)

        # ph
        self.ph = QPushButton(self)
        self.ph.setGeometry(448, 450, 250, 140)
        self.ph.setStyleSheet("QPushButton { border-image: url(ph.png) 0 0 0 0 stretch stretch; }")
        # label nilai ph
        self.label_ph = QLabel("7.5",self)
        self.label_ph.setGeometry(488, 590, 120, 30)
        self.label_ph.setFont(QFont("Arial", 18))
        self.label_ph.setAlignment(Qt.AlignCenter)
        self.label_ph.setStyleSheet("background-color: white")
        
        # Label untuk Turbidity
        self.turbidity = QPushButton(self)
        self.turbidity.setGeometry(608, 470, 170, 120)
        self.turbidity.setStyleSheet("QPushButton { border-image: url(turbidity.png) 0 0 0 0 stretch stretch; }")
        # nilai turbidity
        self.nilai_turbidity = QLabel("24",self)
        self.nilai_turbidity.setGeometry(633, 590, 120, 30)
        self.nilai_turbidity.setFont(QFont("Arial", 18))
        self.nilai_turbidity.setAlignment(Qt.AlignCenter)
        self.nilai_turbidity.setStyleSheet("background-color: white")
        # label turbidity
        self.label_turbidity = QLabel("Turbidity",self)
        self.label_turbidity.setGeometry(636, 490, 120, 30)
        self.label_turbidity.setFont(QFont("Arial", 16, QFont.Bold))
        self.label_turbidity.setAlignment(Qt.AlignCenter)
        
        # pilih pengisian air
        self.info_transaksi = QLabel("Pilih Pengisian Air", self)
        self.info_transaksi.setGeometry(287, 385, 680, 40)
        self.info_transaksi.setFont(QFont("Arial", 24, QFont.Bold))
        self.info_transaksi.setAlignment(Qt.AlignCenter)
        self.info_transaksi.setStyleSheet("color: black")

        # settings
        self.settings = QPushButton(self)
        self.settings.setGeometry(1230, 620, 100, 100)
        self.settings.setStyleSheet("QPushButton { border-image: url(settings.png) 0 0 0 0 stretch stretch; }")

        # backwash
        self.backwash = QPushButton(self)
        self.backwash.setGeometry(5, 628, 80, 80)
        self.backwash.setStyleSheet("QPushButton { border-image: url(backwash.png) 0 0 0 0 stretch stretch; }")

        # when click button
        self.galon_button.clicked.connect(self.showGalonPopup)
        self.tumbler_button.clicked.connect(self.showTumblerPopup)
        self.backwash.clicked.connect(self.showBackwashFlashing)
        self.settings.clicked.connect(self.showSettings)

        # atur posisi layout
        self.setLayout(self.layout)


    def showGalonPopup(self):
        # Simulasikan data jumlah liter air terisi pada galon
        ## komunikasi serial
        galon_data = 19
        """
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout =1)  # Ganti dengan port serial yang sesuai
        data = {
            "command": "read",
            "id": "00001",
            "data": {
                "data0": "turbidity",
                "data1": "ph",
                "data2": "volume"
            },
            "mode": {
                "wadah": "galon",
                "volume": str(galon_data),
                "satuan": "liter",
                "status": ""
            }
        }
        """
        if galon_data < 10:
            info = "Air Kurang Berkualitas"
            dialog = FailedTransactionPopup(info)
            dialog.exec_()
        else:
            """
            try:
                # Mengubah data menjadi format JSON
                json_data = json.dumps(data)
                
                # Mengirim data ke Arduino melalui komunikasi serial
                ser.write(json_data.encode())
                
                print("Data berhasil dikirim ke Arduino:", json_data)
        
            except serial.SerialException as e:
                print("Terjadi kesalahan pada port serial:", str(e))
            time.sleep(1)
            """
            dialog = GalonPopup(galon_data)
            dialog.exec_()

    def showTumblerPopup(self):
        dialog = TumnlerPopup()
        dialog.exec_()
    def showBackwashFlashing(self):
        dialog = BackwashFlashingMenu()
        dialog.exec_()
    
    def showSettings(self):
        dialog = SettingsMenu()
        dialog.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
