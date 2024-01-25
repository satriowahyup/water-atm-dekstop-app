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
    QPushButton
)
from PyQt5.QtGui import (
    QFont,
    QColor,
    QIcon
)
from PyQt5.QtCore import (
    Qt, 
    QTimer,
    QDateTime,
    QUrl, QSize
)
from lib import globals
from lib.menu_tumbler1 import TumblerPopup1, FailedTransactionPopup1, PasswordTumblerMenu1
from lib.menu_tumbler2 import TumblerPopup2, FailedTransactionPopup2, PasswordTumblerMenu2
from lib.menu_tumbler3 import TumblerPopup3, FailedTransactionPopup3, PasswordTumblerMenu3
from lib.menu_report import ReportMenu
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
        
        self.label_tumbler1_status= QLabel(self)
        self.label_tumbler1_status.setGeometry(10, 35, 300, 25)
        self.label_tumbler1_status.setFont(QFont("Arial", 15))
        self.label_tumbler1_status.setAlignment(Qt.AlignLeft)
        self.label_tumbler1_status.setStyleSheet("color: white")
        self.label_tumbler1_status.setText(f"Tumbler 1 : {globals.TUMBLER1}")

        self.label_tumbler2_status= QLabel(self)
        self.label_tumbler2_status.setGeometry(10, 65, 300, 25)
        self.label_tumbler2_status.setFont(QFont("Arial", 15))
        self.label_tumbler2_status.setAlignment(Qt.AlignLeft)
        self.label_tumbler2_status.setStyleSheet("color: white")
        self.label_tumbler2_status.setText(f"Tumbler 2: {globals.TUMBLER2}")

        self.label_tumbler3_status= QLabel(self)
        self.label_tumbler3_status.setGeometry(10, 95, 300, 25)
        self.label_tumbler3_status.setFont(QFont("Arial", 15))
        self.label_tumbler3_status.setAlignment(Qt.AlignLeft)
        self.label_tumbler3_status.setStyleSheet("color: white")
        self.label_tumbler3_status.setText(f"Tumbler 3: {globals.TUMBLER3}")

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

        # Tombol transaksi tumbler 1
        self.tumbler1_button = QPushButton(self)
        self.tumbler1_button.setGeometry(150, 515, 480, 410)  # Atur posisi dan ukuran tombol
        self.tumbler1_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler 1
        self.label_tumbler1= QLabel("Air Tumbler 1",self)
        self.label_tumbler1.setGeometry(255, 915, 310, 40)
        self.label_tumbler1.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_tumbler1.setAlignment(Qt.AlignCenter)
        self.label_tumbler1.setStyleSheet("background-color: white")

        # Tombol transaksi air tumbler 2
        self.tumbler2_button = QPushButton(self)
        self.tumbler2_button.setGeometry(725,515, 480, 410)
        self.tumbler2_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler 2
        self.label_tumbler2 = QLabel("Air Tumbler 2",self)
        self.label_tumbler2.setGeometry(830, 910, 300, 40)
        self.label_tumbler2.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_tumbler2.setAlignment(Qt.AlignCenter)
        self.label_tumbler2.setStyleSheet("background-color: white")

        # Tombol transaksi air tumbler 3
        self.tumbler3_button = QPushButton(self)
        self.tumbler3_button.setGeometry(1320,515, 480, 410)
        self.tumbler3_button.setStyleSheet("QPushButton { border-image: url(tumbler.png) 0 0 0 0 stretch stretch; }")  # Atur background gambar
        # label air tumbler 3
        self.label_tumbler3 = QLabel("Air Tumbler 3",self)
        self.label_tumbler3.setGeometry(1425, 910, 300, 40)
        self.label_tumbler3.setFont(QFont("Arial", 24, QFont.Bold))
        self.label_tumbler3.setAlignment(Qt.AlignCenter)
        self.label_tumbler3.setStyleSheet("background-color: white")

        # ph
        self.ph = QPushButton(self)
        self.ph.setGeometry(798, 180, 250, 140)
        self.ph.setStyleSheet("QPushButton { border-image: url(ph.png) 0 0 0 0 stretch stretch; }")
        # label nilai ph
        self.label_ph = QLabel(self)
        self.label_ph.setGeometry(838, 320, 120, 30)
        self.label_ph.setFont(QFont("Arial", 18))
        self.label_ph.setAlignment(Qt.AlignCenter)
        self.label_ph.setStyleSheet("background-color: white")
        self.label_ph.setText(f"{globals.PH}")
        
        # label kualitas air
        self.label_quality = QLabel("Kualitas Air",self)
        self.label_quality.setGeometry(835, 165, 280, 35)
        self.label_quality.setFont(QFont("Arial", 22, QFont.Bold))
        self.label_quality.setAlignment(Qt.AlignCenter)
        self.label_quality.setStyleSheet("background-color: white")
        #tombol kualitas air
        self.kualitas_air_button = QPushButton("Cek Kualitas Air",self)
        self.kualitas_air_button.setGeometry(835, 360, 280, 40)
        self.kualitas_air_button.setFont(QFont("Arial", 20, QFont.Bold))
        self.kualitas_air_button.setStyleSheet("background-color: skyblue")

        # Gambar untuk Turbidity
        self.turbidity = QPushButton(self)
        self.turbidity.setGeometry(958, 200, 170, 120)
        self.turbidity.setStyleSheet("QPushButton { border-image: url(turbidity.png) 0 0 0 0 stretch stretch; }")
        # nilai turbidity
        self.nilai_turbidity = QLabel(self)
        self.nilai_turbidity.setGeometry(983, 320, 120, 30)
        self.nilai_turbidity.setFont(QFont("Arial", 18))
        self.nilai_turbidity.setAlignment(Qt.AlignCenter)
        self.nilai_turbidity.setStyleSheet("background-color: white")
        self.nilai_turbidity.setText(f"{globals.TURBIDITY}")
        # label turbidity
        self.label_turbidity = QLabel("TDS",self)
        self.label_turbidity.setGeometry(985, 220, 120, 30)
        self.label_turbidity.setFont(QFont("Arial", 18, QFont.Bold))
        self.label_turbidity.setAlignment(Qt.AlignCenter)
        
        # pilih pengisian air
        self.info_transaksi = QLabel("Pilih Pengisian Air", self)
        self.info_transaksi.setGeometry(665, 445, 620, 40)
        self.info_transaksi.setFont(QFont("Arial", 26, QFont.Bold))
        self.info_transaksi.setAlignment(Qt.AlignCenter)
        self.info_transaksi.setStyleSheet("background-color: white")

        # settings
        self.settings = QPushButton(self)
        self.settings.setGeometry(1825, 960, 100, 100)
        self.settings.setStyleSheet("QPushButton { border-image: url(settings.png) 0 0 0 0 stretch stretch; }")

        # report
        self.report = QPushButton(self)
        self.report.setGeometry(5, 965, 80, 80)
        self.report.setStyleSheet("QPushButton { border-image: url(report.png) 0 0 0 0 stretch stretch; }")
            
        # when click button
        self.tumbler1_button.clicked.connect(self.checkPasswordTumbler1)
        self.tumbler2_button.clicked.connect(self.checkPasswordTumbler2)
        self.tumbler3_button.clicked.connect(self.checkPasswordTumbler3)
        self.report.clicked.connect(self.showReport)
        self.settings.clicked.connect(self.showPasswordSettings)
        self.kualitas_air_button.clicked.connect(lambda: self.send_instruction_to_controller(volume="", run="4"))

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

        self.timer_sensor = QTimer(self)
        self.timer_sensor.timeout.connect(self.refresh_ph_turbidity) # update data dan tampilam aplikasi
        self.timer_sensor.start(250)  # Refresh setiap 250 milidetik

        # timer untuk refresh datetime
        self.timer_datetime = QTimer(self)
        self.timer_datetime.timeout.connect(self.update_datetime)
        self.timer_datetime.start(1000)  # Update setiap 1000 milidetik (1 detik)

        # audio
        self.player = QMediaPlayer()
        self.player.setVolume(50)
        self.player.setNotifyInterval(100)  # Update every 100 milliseconds
        self.player.mediaStatusChanged.connect(self.handleMediaStatusChanged)

        self.file_path = os.path.join(os.getcwd(), 'voice/Selamat-Datang.mp3')
        self.url = QUrl.fromLocalFile(self.file_path)
        self.content = QMediaContent(self.url)
     
        self.toggleAudioPlayback()

    def refresh_data(self):
        #self.label_ph.setText(f"{globals.DATA_PH}")
        #self.nilai_turbidity.setText(f"{globals.DATA_TURBIDITY}")
        self.label_machine.setText(f"Machine : {globals.STATUS}")
        self.label_tumbler1_status.setText(f"Tumbler 1 : {globals.TUMBLER1}")
        self.label_tumbler2_status.setText(f"Tumbler 2 : {globals.TUMBLER2}")
        self.label_tumbler3_status.setText(f"Tumbler 2 : {globals.TUMBLER3}")

    def refresh_ph_turbidity(self):
        if globals.STATUS == "ready" and globals.TUMBLER1 == "ready" and globals.TUMBLER2 == "ready" and globals.TUMBLER3 == "ready":
            self.label_ph.setText(f"{globals.DATA_PH}")
            self.nilai_turbidity.setText(f"{globals.DATA_TURBIDITY}")

    def update_datetime(self):
        current_datetime = QDateTime.currentDateTime()
        current_time = current_datetime.toString("hh:mm:ss")
        self.label_datetime.setText(current_time)

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
                    globals.TUMBLER1 = mode['tumbler1']
                    globals.TUMBLER2 = mode['tumbler2'] 
                    globals.TUMBLER3 = mode['tumbler3'] 
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

    def checkPasswordTumbler1(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = PasswordTumblerMenu1()
        dialog.exec_()
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()
        
    def showTumblerPopup1(self):
        if globals.TUMBLER1 == "ready":
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            dialog = TumblerPopup1(parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        else :
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            info = "Air Galon Belum Siap"
            dialog = FailedTransactionPopup1(info, parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
    
    def checkPasswordTumbler2(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = PasswordTumblerMenu2()
        dialog.exec_()
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()
        
    def showTumblerPopup2(self):
        if globals.TUMBLER2 == "ready":
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            dialog = TumblerPopup2(parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        else :
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            info = "Air Galon Belum Siap"
            dialog = FailedTransactionPopup2(info, parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()

    def checkPasswordTumbler3(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.stop()
        dialog = PasswordTumblerMenu3()
        dialog.exec_()
        dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
        dialog.exec_()

    def showTumblerPopup3(self): 
        if globals.TUMBLER3 == "ready":
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            dialog = TumblerPopup3(parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        else:
            if self.player.state() == QMediaPlayer.PlayingState:
                self.player.stop()
            info = "Air Tumbler Belum Siap"
            dialog = FailedTransactionPopup3(info, parent=self)
            dialog.finished.connect(self.toggleAudioPlayback)  # Mengaktifkan kembali audio setelah popup ditutup
            dialog.exec_()
        
    def showReport(self):
        dialog = ReportMenu()
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

    def send_instruction_to_controller(self, volume, run):
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
                "volume": str(volume),
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
