import sys
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QHBoxLayout, 
    QPushButton
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

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mulai Hidup Sehat dengan Air Berkualitas")
        self.setGeometry(5, 5, 1920, 1080)
        self.initUI()

    def initUI(self):
        # Warna latar belakang RGB
        red = 135
        green = 206
        blue = 235
        background_color = QColor(red, green, blue)

        # Atur warna latar belakang GUI
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), background_color)
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Label untuk status machine
        label_machine = QLabel("Machine : -",self)
        label_machine.setGeometry(10, 5, 250, 25)
        label_machine.setFont(QFont("Arial", 15))
        label_machine.setAlignment(Qt.AlignLeft)
        label_machine.setStyleSheet("color: white")

        # Label untuk status water
        label_water = QLabel("Water : -",self)
        label_water.setGeometry(1070, 5, 250, 25)
        label_water.setFont(QFont("Arial", 15))
        label_water.setAlignment(Qt.AlignRight)
        label_water.setStyleSheet("color: white")

        # Judul
        title_label = QLabel("Mulai Hidup Sehat dengan Air Berkualitas", self)
        title_label.setGeometry(260, 30, 770, 40)
        title_label.setFont(QFont("Arial", 28, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: black")

        # Gambar mata air
        water_image = QPushButton(self)
        water_image.setGeometry(285, 90, 670, 300)
        water_image.setStyleSheet("QPushButton { border-image: url(water-icon.png) 0 0 0 0 stretch stretch; }")

        # Tombol transaksi air galon
        galon_button = QPushButton(self)
        galon_button.setGeometry(40, 350, 400, 300)  # Atur posisi dan ukuran tombol
        galon_button.setStyleSheet("QPushButton { border-image: url(galon.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air galon
        label_galon = QLabel("Air Galon",self)
        label_galon.setGeometry(168, 630, 150, 40)
        label_galon.setFont(QFont("Arial", 24, QFont.Bold))
        label_galon.setAlignment(Qt.AlignCenter)

        # Tombol transaksi air tumbler
        tumbler_button = QPushButton(self)
        tumbler_button.setGeometry(860,365, 330, 280)
        tumbler_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler
        label_tumbler = QLabel("Air Tumbler",self)
        label_tumbler.setGeometry(940, 630, 200, 40)
        label_tumbler.setFont(QFont("Arial", 24, QFont.Bold))
        label_tumbler.setAlignment(Qt.AlignCenter)

        # ph
        ph = QPushButton(self)
        ph.setGeometry(448, 450, 250, 140)
        ph.setStyleSheet("QPushButton { border-image: url(ph.png) 0 0 0 0 stretch stretch; }")
        # label nilai ph
        label_ph = QLabel("7.5",self)
        label_ph.setGeometry(488, 590, 120, 30)
        label_ph.setFont(QFont("Arial", 18))
        label_ph.setAlignment(Qt.AlignCenter)
        label_ph.setStyleSheet("background-color: white")
        
        # Label untuk Turbidity
        turbidity = QPushButton(self)
        turbidity.setGeometry(608, 470, 170, 120)
        turbidity.setStyleSheet("QPushButton { border-image: url(turbidity.png) 0 0 0 0 stretch stretch; }")
        # nilai turbidity
        nilai_turbidity = QLabel("24",self)
        nilai_turbidity.setGeometry(633, 590, 120, 30)
        nilai_turbidity.setFont(QFont("Arial", 18))
        nilai_turbidity.setAlignment(Qt.AlignCenter)
        nilai_turbidity.setStyleSheet("background-color: white")
        # label turbidity
        label_turbidity = QLabel("Turbidity",self)
        label_turbidity.setGeometry(636, 490, 120, 30)
        label_turbidity.setFont(QFont("Arial", 16, QFont.Bold))
        label_turbidity.setAlignment(Qt.AlignCenter)
        
        # pilih pengisian air
        info_transaksi = QLabel("Pilih Pengisian Air", self)
        info_transaksi.setGeometry(287, 385, 680, 40)
        info_transaksi.setFont(QFont("Arial", 24, QFont.Bold))
        info_transaksi.setAlignment(Qt.AlignCenter)
        info_transaksi.setStyleSheet("color: black")

        # settings
        settings = QPushButton(self)
        settings.setGeometry(1230, 620, 100, 100)
        settings.setStyleSheet("QPushButton { border-image: url(settings.png) 0 0 0 0 stretch stretch; }")

        # atur posisi layout
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
