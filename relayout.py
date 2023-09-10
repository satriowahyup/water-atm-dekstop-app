import sys
import json
import serial
import threading
import time, os
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QLabel, 
    QVBoxLayout, 
    QDesktopWidget, 
    QPushButton,
)
from PyQt5.QtGui import (
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt, 
    QTimer,
    QDateTime,
    QUrl
)
from lib import globals
from lib.menu_galon import GalonPopup, PasswordGalonMenu
from lib.menu_tumbler import TumblerPopup, FailedTransactionPopup, PasswordTumblerMenu
from lib.menu_backwash_flashing import BackwashFlashingMenu
from lib.menu_settings import SettingsMenu, PasswordSettings
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent

# variabel global
panjang_data_serial = 0
command = "" # read | write
id = "00001" 
ph = "" # 0.1 | number
turbidity = "" # 0.1 | number
wadah = "" # galon | tumbler
volume = "" # 19 | 300
satuan = "" # liter | mililiter
status = "" # waiting | running | done


# Main WIndow
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Water ATM")
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry(screen)

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
        self.label_machine = QLabel(self)
        self.label_machine.setGeometry(10, 5, 300, 25)
        self.label_machine.setFont(QFont("Arial", 15))
        self.label_machine.setAlignment(Qt.AlignLeft)
        self.label_machine.setStyleSheet("color: white")
        self.label_machine.setText(f"Machine : {globals.STATUS}")
        
        self.label_galon_status= QLabel(self)
        self.label_galon_status.setGeometry(10, 35, 300, 25)
        self.label_galon_status.setFont(QFont("Arial", 15))
        self.label_galon_status.setAlignment(Qt.AlignLeft)
        self.label_galon_status.setStyleSheet("color: white")
        self.label_galon_status.setText(f"Galon : {globals.GALON}")

        self.label_tumbler_status= QLabel(self)
        self.label_tumbler_status.setGeometry(10, 65, 300, 25)
        self.label_tumbler_status.setFont(QFont("Arial", 15))
        self.label_tumbler_status.setAlignment(Qt.AlignLeft)
        self.label_tumbler_status.setStyleSheet("color: white")
        self.label_tumbler_status.setText(f"Tumbler : {globals.TUMBLER}")

        #label untuk datetime
        self.label_datetime = QLabel(self)
        self.label_datetime.setGeometry(1710, 5, 300, 25)
        self.label_datetime.setFont(QFont("Arial", 14, QFont.Bold))
        self.label_datetime.setAlignment(Qt.AlignCenter)
        self.label_datetime.setStyleSheet("color: black")

        # Judul
        self.title_label = QLabel("Mulai Hidup Sehat dengan Air Berkualitas", self)
        self.title_label.setGeometry(520, 40, 850, 50)
        self.title_label.setFont(QFont("Arial", 32, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: black")

        # Gambar mata air
        self.water_image = QPushButton(self)
        self.water_image.setGeometry(530, 110, 850, 420)
        self.water_image.setStyleSheet("QPushButton { border-image: url(water-icon.png) 0 0 0 0 stretch stretch; }")

        # Tombol transaksi air galon
        self.galon_button = QPushButton(self)
        self.galon_button.setGeometry(120, 500, 550, 430)  # Atur posisi dan ukuran tombol
        self.galon_button.setStyleSheet("QPushButton { border-image: url(galon.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air galon
        self.label_galon = QLabel("Air Galon",self)
        self.label_galon.setGeometry(235, 905, 310, 40)
        self.label_galon.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_galon.setAlignment(Qt.AlignCenter)
        self.label_galon.setStyleSheet("background-color: white")
        #tombol bilas galon
        self.bilas_galon_button = QPushButton("Bilas Galon",self)
        self.bilas_galon_button.setGeometry(235, 950, 310, 40)
        self.bilas_galon_button.setFont(QFont("Arial", 24, QFont.Bold))
        self.bilas_galon_button.setStyleSheet("background-color: skyblue")

        # Tombol transaksi air tumbler
        self.tumbler_button = QPushButton(self)
        self.tumbler_button.setGeometry(1320,515, 480, 410)
        self.tumbler_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler
        self.label_tumbler = QLabel("Air Tumbler",self)
        self.label_tumbler.setGeometry(1425, 910, 300, 40)
        self.label_tumbler.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_tumbler.setAlignment(Qt.AlignCenter)
        self.label_tumbler.setStyleSheet("background-color: white")
        #tombol bilas galon
        self.bilas_tumbler_button = QPushButton("Bilas Tumbler",self)
        self.bilas_tumbler_button.setGeometry(1425, 953, 300, 40)
        self.bilas_tumbler_button.setFont(QFont("Arial", 24, QFont.Bold))
        self.bilas_tumbler_button.setStyleSheet("background-color: skyblue")

        # ph
        self.ph = QPushButton(self)
        self.ph.setGeometry(798, 700, 250, 140)
        self.ph.setStyleSheet("QPushButton { border-image: url(ph.png) 0 0 0 0 stretch stretch; }")
        # label nilai ph
        self.label_ph = QLabel(self)
        self.label_ph.setGeometry(838, 840, 120, 30)
        self.label_ph.setFont(QFont("Arial", 18))
        self.label_ph.setAlignment(Qt.AlignCenter)
        self.label_ph.setStyleSheet("background-color: white")
        self.label_ph.setText(f"{globals.PH}")
        
        # label kualitas air
        self.label_quality = QLabel("Kualitas Air",self)
        self.label_quality.setGeometry(835, 685, 280, 35)
        self.label_quality.setFont(QFont("Arial", 22, QFont.Bold))
        self.label_quality.setAlignment(Qt.AlignCenter)
        self.label_quality.setStyleSheet("background-color: white")
        #tombol kualitas air
        self.kualitas_air_button = QPushButton("Cek Kualitas Air",self)
        self.kualitas_air_button.setGeometry(835, 880, 280, 40)
        self.kualitas_air_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.kualitas_air_button.setStyleSheet("background-color: skyblue")

        # Gambar untuk Turbidity
        self.turbidity = QPushButton(self)
        self.turbidity.setGeometry(958, 720, 170, 120)
        self.turbidity.setStyleSheet("QPushButton { border-image: url(turbidity.png) 0 0 0 0 stretch stretch; }")
        # nilai turbidity
        self.nilai_turbidity = QLabel(self)
        self.nilai_turbidity.setGeometry(983, 840, 120, 30)
        self.nilai_turbidity.setFont(QFont("Arial", 18))
        self.nilai_turbidity.setAlignment(Qt.AlignCenter)
        self.nilai_turbidity.setStyleSheet("background-color: white")
        self.nilai_turbidity.setText(f"{globals.TURBIDITY}")
        # label turbidity
        self.label_turbidity = QLabel("Turbidity",self)
        self.label_turbidity.setGeometry(985, 740, 120, 30)
        self.label_turbidity.setFont(QFont("Arial", 16, QFont.Bold))
        self.label_turbidity.setAlignment(Qt.AlignCenter)
        
        # pilih pengisian air
        self.info_transaksi = QLabel("Pilih Pengisian Air", self)
        self.info_transaksi.setGeometry(665, 545, 620, 40)
        self.info_transaksi.setFont(QFont("Arial", 26, QFont.Bold))
        self.info_transaksi.setAlignment(Qt.AlignCenter)
        self.info_transaksi.setStyleSheet("background-color: white")

        # settings
        self.settings = QPushButton(self)
        self.settings.setGeometry(1825, 960, 100, 100)
        self.settings.setStyleSheet("QPushButton { border-image: url(settings.png) 0 0 0 0 stretch stretch; }")

        # backwash
        self.backwash = QPushButton(self)
        self.backwash.setGeometry(5, 965, 80, 80)
        self.backwash.setStyleSheet("QPushButton { border-image: url(backwash.png) 0 0 0 0 stretch stretch; }")

        # when click button
        #self.galon_button.clicked.connect(self.showGalonPopup)
        self.galon_button.clicked.connect(self.checkPasswordMenuGalon)
        #self.tumbler_button.clicked.connect(self.showTumblerPopup)
        self.tumbler_button.clicked.connect(self.checkPasswordTmblerGalon)
        self.backwash.clicked.connect(self.showBackwashFlashing)
        self.settings.clicked.connect(self.showPasswordSettings)
        self.kualitas_air_button.clicked.connect(lambda: self.send_instruction_to_controller(run="3"))
        self.bilas_galon_button.clicked.connect(lambda: self.send_instruction_to_controller(run="4"))
        self.bilas_tumbler_button.clicked.connect(lambda: self.send_instruction_to_controller(run="5"))

        self.label_serial = QLabel("Panjang Data",self)
        self.label_serial.setGeometry(860, 990, 200, 100)
        self.label_serial.setFont(QFont("Arial", 12))
        self.label_serial.setAlignment(Qt.AlignCenter)

        self.receive_data_thread = threading.Thread(target=self.read_serial_data)
        # Menjalankan thread-thread tersebut
        self.receive_data_thread.start()
        
        # atur posisi layout
        self.setLayout(self.layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data) # update data dan tampilam aplikasi
        self.timer.start(100)  # Refresh setiap 100 milidetik (0.1 detik)

        # timer untuk refresh datetime
        self.timer_datetime = QTimer(self)
        self.timer_datetime.timeout.connect(self.update_datetime)
        self.timer_datetime.start(1000)  # Update setiap 1000 milidetik (1 detik)

        # audio
        self.player = QMediaPlayer()
        self.player.setVolume(50)
        self.player.setNotifyInterval(100)  # Update every 100 milliseconds
        self.player.mediaStatusChanged.connect(self.handleMediaStatusChanged)

        self.file_path = os.path.join(os.getcwd(), 'Selamat-Datang.mp3')
        self.url = QUrl.fromLocalFile(self.file_path)
        self.content = QMediaContent(self.url)
        
        self.toggleAudioPlayback()

    def refresh_data(self):
        #self.nilai_turbidity.setText(f"{globals.TURBIDITY}")
        #self.label_ph.setText(f"{globals.PH}")
        self.label_ph.setText(f"{globals.DATA_PH}")
        self.nilai_turbidity.setText(f"{globals.DATA_TURBIDITY}")
        self.label_machine.setText(f"Machine : {globals.STATUS}")
        self.label_galon_status.setText(f"Galon : {globals.GALON}")
        self.label_tumbler_status.setText(f"Tumbler : {globals.TUMBLER}")

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        current_time = current_datetime.toString("hh:mm:ss")
        self.label_datetime.setText(current_time)
        """
        try:
            client = ntplib.NTPClient()
            response = client.request('pool.ntp.org')
            current_time = QDateTime.fromMSecsSinceEpoch(response.tx_time * 1000).toString("hh:mm:ss")
            self.label_datetime.setText(current_time)
        except Exception as e:
            print("Error updating datetime:", str(e))
        """
    def request_data_sensor(self):
        print("kirim request sensor ph dan turbidity")

    def read_serial_data(self):
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout =1)  # Ganti dengan port serial yang sesuai
        while True:
            val = ser.readline()
            panjang_data_serial = len(val)
            
            self.label_serial.setText(f"{panjang_data_serial}")
            if(len(val) > 10):
                print(f"panjang data: {panjang_data_serial}")
                #print(val)
                #data = val.decode('utf-8').strip()
                data = val.decode('latin-1').strip()
                #data = val.decode('latin-1', 'ignore').strip() 
                #print(val)
                print(data)
                try:
                    json_data = json.loads(data)
                    data = json_data['data']
                    mode = json_data['mode']
                    #globals.COMMAND = json_data['command']
                    globals.ID = json_data['id']
                    globals.PH = data['data0']
                    globals.TURBIDITY = data['data1']
                    globals.GALON = mode['galon'] #if mode['galon'] != "" else None
                    globals.TUMBLER = mode['tumbler'] #if mode['tumbler'] != "" else None
                    globals.STATUS = mode['status']
                    #sprint("galon: ", mode['galon'], " | ", "tumbler: ", mode['tumbler'])

                    if data['data0'] != "" or data['data0'] != None:
                        globals.DATA_PH = data['data0']
                        #print("ph: ",globals.DATA_PH)
                    if data['data1'] != "" or data['data1'] != None:
                        globals.DATA_TURBIDITY = data['data1']
                        #print("turbidity: ",globals.DATA_TURBIDITY)

                except json.decoder.JSONDecodeError:
                    print("Data JSON tidak valid:", data)
                    globals.PH = "-"
                    globals.TURBIDITY = "-"
            else:
                globals.PH = "-"
                globals.TURBIDITY= "-"

    def checkPasswordMenuGalon(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = PasswordGalonMenu()
        dialog.exec_()
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()
        
    def showGalonPopup(self):
        """
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = GalonPopup(parent=self)
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()
        """
        if globals.GALON == "ready":
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            dialog = GalonPopup(parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        else :
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            info = "Air Galon Belum Siap"
            dialog = FailedTransactionPopup(info, parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
    
    def checkPasswordTmblerGalon(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = PasswordTumblerMenu()
        dialog.exec_()
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()

    def showTumblerPopup(self): 
        """
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = TumblerPopup(parent=self)
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()
        """ 
        if globals.TUMBLER == "ready":
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            dialog = TumblerPopup(parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            info = "Air Tumbler Belum Siap"
            dialog = FailedTransactionPopup(info, parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        
    def showBackwashFlashing(self):
        dialog = BackwashFlashingMenu()
        dialog.exec_()
    
    def showSettings(self):
        dialog = SettingsMenu()
        dialog.exec_()
        
    def showPasswordSettings(self):
        dialog = PasswordSettings()
        dialog.exec_()
    
    def toggleAudioPlayback(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        else:
            self.player.setMedia(self.content)
            self.player.play()
    
    def handleMediaStatusChanged(self, status):
        if status == QMediaPlayer.EndOfMedia:
            self.player.play()

    def send_instruction_to_controller(self, run):
        #print("run : ", run)
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
                "volume": "",
                "tumbler": "",
                "status": ""
            },
            "run": str(run)
        }
        try:
            # Mengubah data menjadi format JSON
            json_data = json.dumps(data)
            
            # Mengirim data ke Arduino melalui komunikasi serial
            ser.write(json_data.encode())
            #print("Data berhasil dikirim ke Arduino:", json_data)
        except serial.SerialException as e:
            print("Terjadi kesalahan pada port serial:", str(e))

        time.sleep(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    #window.showFullScreen()
    sys.exit(app.exec_())
