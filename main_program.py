import sys
import serial
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QGridLayout
from PyQt5.QtGui import QCursor, QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Inisialisasi komponen GUI
        self.setWindowTitle("Water ATM")
        self.setGeometry(100, 100, 1920, 1080)
        #self.setWindowState(Qt.WindowFullScreen)

        self.layout = QVBoxLayout()

        # Create a label to display image
        self.label_title = QLabel("Mulai Hidup Sehat dengan Air Berkualitas")
        self.label_title.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.label_title)

        self.button_air_galon = QPushButton("Pesan Air Galon")
        self.button_air_galon.clicked.connect(self.show_page_air_galon)
        self.layout.addWidget(self.button_air_galon)

        self.button_air_tumbler = QPushButton("Pesan Air Tumbler")
        self.button_air_tumbler.clicked.connect(self.show_page_air_tumbler)
        self.layout.addWidget(self.button_air_tumbler)

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout)
        self.setCentralWidget(self.central_widget)

    def show_page_air_galon(self):
        self.central_widget.setParent(None)
        self.setCentralWidget(PageAirGalon(self))

    def show_page_air_tumbler(self):
        self.central_widget.setParent(None)
        self.setCentralWidget(PageAirTumbler(self))


class PageAirGalon(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label_title = QLabel("Halaman Transaksi Air Galon")
        self.layout.addWidget(self.label_title)

        self.label_input = QLabel("Masukkan jumlah liter:")
        self.layout.addWidget(self.label_input)

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

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

        self.layout.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        self.button_enter.clicked.connect(self.send_data_to_arduino)
        self.layout.addWidget(self.button_enter)

        self.button_back = QPushButton("Back")
        self.button_back.clicked.connect(self.go_back)
        self.layout.addWidget(self.button_back)

        self.setLayout(self.layout)

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

    def send_data_to_arduino(self):
        total_liter = self.digits
        # Kirim data total liter ke Arduino menggunakan komunikasi serial
        print(f"Mengirim data total liter: {total_liter} ke Arduino")

    def go_back(self):
        self.setParent(None)
        self.main_window.setCentralWidget(MainWindow())


class PageAirTumbler(QWidget):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window

        self.layout = QVBoxLayout()

        self.label_title = QLabel("Halaman Transaksi Air Tumbler")
        self.layout.addWidget(self.label_title)

        self.label_input = QLabel("Masukkan jumlah liter:")
        self.layout.addWidget(self.label_input)

        self.line_edit = QLineEdit()
        self.layout.addWidget(self.line_edit)

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

        self.layout.addLayout(self.grid_layout)

        self.button_enter = QPushButton("Enter")
        self.button_enter.clicked.connect(self.send_data_to_arduino)
        self.layout.addWidget(self.button_enter)

        self.button_back = QPushButton("Back")
        self.button_back.clicked.connect(self.go_back)
        self.layout.addWidget(self.button_back)

        self.setLayout(self.layout)

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

    def send_data_to_arduino(self):
        total_liter = self.digits
        # Kirim data total liter ke Arduino menggunakan komunikasi serial
        print(f"Mengirim data total liter: {total_liter} ke Arduino")

    def go_back(self):
        self.setParent(None)
        self.main_window.setCentralWidget(MainWindow())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
