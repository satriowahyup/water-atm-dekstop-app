import sys, serial, time, os, json
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
        # Membaca data dari file JSON
        with open('setting.json') as file:
            data = json.load(file)
        # nilai seeting ph
        data_ph = self.line_edit_ph.text()
        # Memperbarui nilai
        data['ph'] = data_ph
        # Menulis kembali data ke file JSON
        with open('setting.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.digits = ""
        self.line_edit_ph.setText(self.digits)
        dialog = TurbiditySettingsMenu(data_ph)
        dialog.exec_()

class TurbiditySettingsMenu(QDialog):
    def __init__(self, data_ph):
        super().__init__()
        self.setWindowTitle("Menu Settings")
        self.setFixedSize(350, 340)
        self.initUI(data_ph)

    def initUI(self, data_ph):
        data = data_ph
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
        self.button_enter.clicked.connect(self.sendSettingstoArduino)
        print(data)
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
    
    def sendSettingstoArduino(self):
        data_turbidity = self.line_edit_turbidity.text()
        print(data_turbidity)
        # Membaca data dari file JSON
        with open('setting.json') as file:
            data = json.load(file)
        # Memperbarui nilai
        data['turbidity'] = data_turbidity
        with open('setting.json', 'w') as file:
            json.dump(data, file, indent=4)
        self.digits = ""
        self.line_edit_turbidity.setText(self.digits)

    def closeAllPopups(self):
        self.parent().close()
        self.parent().parent().close()

# password menu settings
class PasswordSettings(QDialog):
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
        self.label_input = QLabel("Masukkan Password")
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

        button_comma = QPushButton("@")
        button_comma.clicked.connect(self.add_comma)
        self.grid_layout.addWidget(button_comma, 3, 0)

        button_0 = QPushButton("0")
        button_0.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_0, 3, 1)

        button_clear = QPushButton("#")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 3, 2)

        button_minus = QPushButton("$")
        button_minus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_minus, 4, 0)

        button_plus = QPushButton("%")
        button_plus.clicked.connect(self.add_digit)
        self.grid_layout.addWidget(button_plus, 4, 1)

        button_clear = QPushButton("C")
        button_clear.clicked.connect(self.clear_digits)
        self.grid_layout.addWidget(button_clear, 4, 2)

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
            dialog = SettingsMenu()
            dialog.exec_()
        else:
            dialog = incorrectPassword()
            dialog.exec_()

class incorrectPassword(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Gagal")
        self.setFixedSize(230, 90)

        vbox = QVBoxLayout()
        label = QLabel("Password Anda Salah")
        label.setAlignment(Qt.AlignCenter)
        label.setFont(QFont("Arial", 12, QFont.Bold))
        vbox.addWidget(label)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)
        self.setLayout(vbox)