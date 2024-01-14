import csv, json
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QScrollArea, QDesktopWidget, QPushButton, QLabel
from PyQt5.QtGui import (
    QFont,
)
from PyQt5.QtGui import (
    QFont,
    QColor
)
from PyQt5.QtCore import (
    Qt,
)

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

        # Tambahkan tombol close
        self.button_box = QDialogButtonBox(QDialogButtonBox.Close)
        self.button_box.rejected.connect(self.close)
        self.vbox.addWidget(self.button_box)

        # Tambahkan tombol Volume
        button_volume = QPushButton("Total Volume")
        button_volume.clicked.connect(self.volumePopup)
        self.vbox.addWidget(button_volume)

        #path = '/home/satrio/Documents/Data Laptop Asus - Satrio/Satrio/Personal Project/Water ATM/desktop-app/report.csv'  # Ganti dengan path sesuai dengan direktori Anda
        path = '/home/admin/Documents/apps/desktop-app/report.csv'
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
    
    def volumePopup(self):
        dialog = TotalVolumePopup()
        dialog.exec_()

class TotalVolumePopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Total Volume")
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

        # reaad total volume
        file_path = 'volume.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Update nilai total
        volume= data['total']
        total_volume = str(volume) + " Liter"

        vbox = QVBoxLayout()
        label_info = QLabel("Total Pengisian Air")
        label_info.setAlignment(Qt.AlignCenter)
        label_info.setFont(QFont("Arial", 14, QFont.Bold))
        vbox.addWidget(label_info)

        label_title = QLabel(total_volume)
        label_title.setAlignment(Qt.AlignCenter)
        label_title.setFont(QFont("Arial", 14))
        vbox.addWidget(label_title)

        button_close = QPushButton("Close")
        button_close.clicked.connect(self.close)

        vbox.addWidget(button_close)

        self.setLayout(vbox)