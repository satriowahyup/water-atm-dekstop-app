import serial, time, os, json
from PyQt5.QtWidgets import ( 
    QLabel, 
    QVBoxLayout, 
    QPushButton,
    QDialog,
    QLineEdit,
    QGridLayout
)
from PyQt5.QtGui import (
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt, 
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from lib import globals

class TumblerPopup(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Proses Pengisian Air Tumbler")
        self.setFixedSize(290, 260)
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
        self.label_input = QLabel("Pilih Pengisian Air")
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setFont(QFont("Arial", 16, QFont.Bold))
        vbox.addWidget(self.label_input)

        self.button_300mL = QPushButton("300mL", self)
        self.button_300mL.setFixedWidth(180)
        self.button_300mL.setFixedHeight(50)
        self.button_300mL.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_600mL = QPushButton("600mL", self)
        self.button_600mL.setFixedWidth(180)
        self.button_600mL.setFixedHeight(50)
        self.button_600mL.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_900mL = QPushButton("900mL", self)
        self.button_900mL.setFixedWidth(180)
        self.button_900mL.setFixedHeight(50)
        self.button_900mL.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_300mL.clicked.connect(lambda: self.air_popup(volume="300"))
        self.button_300mL.clicked.connect(self.close)

        self.button_600mL.clicked.connect(lambda: self.air_popup(volume="600"))
        self.button_600mL.clicked.connect(self.close)

        self.button_900mL.clicked.connect(lambda:self.air_popup(volume="900"))
        self.button_900mL.clicked.connect(self.close)

        #vbox.addWidget(self.button_enter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_300mL, alignment=Qt.AlignHCenter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_600mL, alignment=Qt.AlignHCenter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_900mL, alignment=Qt.AlignHCenter)

        self.setLayout(vbox)
        self.digits = ""

    def air_popup(self, volume):
        dialog = JenisAirPopup(volume)
        dialog.exec_()

class StstusPengisianTumbler(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Air Tumbler")
        self.setFixedSize(280, 130)
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
        label_info = QLabel("Proses Pengisian Air")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_title = QLabel("Mohon Ditunggu")
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Arial", 14))
        vbox.addWidget(label_title)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)

class FailedTransactionPopup(QDialog):
    def __init__(self, info_machine, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Info Status")
        self.setFixedSize(280, 110)

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
        label_transaksi = QLabel("Pengisian Air Gagal")
        label_transaksi.setAlignment(Qt.AlignCenter)
        label_transaksi.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_transaksi)

        label_info_machine = QLabel(f"{info_machine}")
        label_info_machine.setAlignment(Qt.AlignCenter)
        label_info_machine.setFont(QFont("Arial", 11, QFont.Bold))
        label_info_machine.setStyleSheet("background-color: white")
        vbox.addWidget(label_info_machine)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)

class JenisAirPopup(QDialog):
    def __init__(self, volume, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Proses Pengisian Air Tumbler")
        self.setFixedSize(290, 260)
        self.initUI(volume)
        self.serial = None  # Objek serial untuk komunikasi dengan Arduino

    def initUI(self, volume):
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
        self.label_input = QLabel("Pilih Kondisi Air")
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setFont(QFont("Arial", 16, QFont.Bold))
        vbox.addWidget(self.label_input)

        self.button_normal = QPushButton("Normal", self)
        self.button_normal.setFixedWidth(180)
        self.button_normal.setFixedHeight(50)
        self.button_normal.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_dingin = QPushButton("Dingin", self)
        self.button_dingin.setFixedWidth(180)
        self.button_dingin.setFixedHeight(50)
        self.button_dingin.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_panas = QPushButton("Panas", self)
        self.button_panas.setFixedWidth(180)
        self.button_panas.setFixedHeight(50)
        self.button_panas.setFont(QFont("Arial", 14, QFont.Bold))

        self.button_normal.clicked.connect(lambda: self.send_data_to_arduino(volume, status="normal"))
        self.button_normal.clicked.connect(self.close)

        self.button_dingin.clicked.connect(lambda: self.send_data_to_arduino(volume, status="dingin"))
        self.button_dingin.clicked.connect(self.close)

        self.button_panas.clicked.connect(lambda:self.send_data_to_arduino(volume, status="panas"))
        self.button_panas.clicked.connect(self.close)

        #vbox.addWidget(self.button_enter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_panas, alignment=Qt.AlignHCenter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_dingin, alignment=Qt.AlignHCenter)
        vbox.addSpacing(10)
        vbox.addWidget(self.button_normal, alignment=Qt.AlignHCenter)

        self.setLayout(vbox)
        self.digits = ""

    def send_data_to_arduino(self, volume, status):
        #if globals.STATUS == "ready" and globals.TUMBLER == "ready":
        if globals.TUMBLER == "ready":
            ## komunikasi serial
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
                    "galon": "",
                    "volume": str(volume),
                    "tumbler": "",
                    "status": str(status)
                },
                "run": "2"
            }
            try:
                # Mengubah data menjadi format JSON
                json_data = json.dumps(data)
                
                # Mengirim data ke Arduino melalui komunikasi serial
                ser.write(json_data.encode())
                #print("Data berhasil dikirim ke Arduino:", json_data)
            except serial.SerialException as e:
                print("Terjadi kesalahan pada port serial:", str(e))

            self.showStatusTumblerPopup
            time.sleep(1)
        else :
            info = "Air Tumbler Belum Siap"
            dialog = FailedTransactionPopup(info)
            dialog.exec_()
         
    def showStatusTumblerPopup(self):
        dialog = StstusPengisianTumbler()
        dialog.exec_()

# password menu settings
class PasswordTumblerMenu(QDialog):
    def __init__(self,parent=None):
        super().__init__(parent)
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
        self.label_input = QLabel("Masukkan Password")
        self.label_input.setAlignment(Qt.AlignCenter)
        self.label_input.setFont(QFont("Arial", 18, QFont.Bold))
        vbox.addWidget(self.label_input)

        self.line_edit = QLineEdit()
        vbox.addWidget(self.line_edit)

        self.grid_layout = QGridLayout()

        for i in range(1, 10):
            self.button = QPushButton(str(i))
            self.button.clicked.connect(self.add_digit)
            self.grid_layout.addWidget(self.button, (i-1)//3, (i-1)%3)

        self.button_comma = QPushButton("@")
        self.button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(self.button_comma, 3, 0)

        self.button_0 = QPushButton("0")
        self.button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(self.button_0, 3, 1)

        self.button_clear = QPushButton("#")
        self.button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(self.button_clear, 3, 2)

        self.button_minus = QPushButton("$")
        self.button_minus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(self.button_minus, 4, 0)

        self.button_plus = QPushButton("%")
        self.button_plus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(self.button_plus, 4, 1)

        self.button_clear = QPushButton("C")
        self.button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(self.button_clear, 4, 2)

        vbox.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        self.button_enter.clicked.connect(self.checkPassword)
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
    
    def checkPassword(self):
        # Simulasikan data jumlah liter air terisi pada galon
        data = self.line_edit.text()
        if data == "2339":
            self.digits = ""
            self.line_edit.setText(self.digits)
            dialog = TumblerPopup()
            dialog.exec_()
        else:
            dialog = incorrectPassword()
            dialog.exec_()

class incorrectPassword(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login Gagal")
        self.setFixedSize(230, 90)

        vbox = QVBoxLayout()
        label = QLabel("Password Anda Salah")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label)

        self.button_close = QPushButton("Close")
        self.button_close.clicked.connect(self.close)

        vbox.addWidget(self.button_close)
        self.setLayout(vbox)