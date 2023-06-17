import json
import serial
import time
import threading

# Inisialisasi port serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout =1)  # Ganti dengan port serial yang sesuai

# Fungsi untuk mengirim data JSON ke Arduino melalui komunikasi serial
def send_data_to_arduino(data):
    try:
        # Mengubah data menjadi format JSON
        json_data = json.dumps(data)
        
        # Mengirim data ke Arduino melalui komunikasi serial
        ser.write(json_data.encode())
        
        print("Data berhasil dikirim ke Arduino:", json_data)
        
    except serial.SerialException as e:
        print("Terjadi kesalahan pada port serial:", str(e))
    time.sleep(1)

# Fungsi untuk membaca data serial dari Arduino
def read_serial_data():
    while True:
        val = ser.readline()
        print(len(val))
        if(len(val) > 1):
            data = (val.decode('utf-8').strip())
            json_data = json.loads(data)
            #print("Data JSON diterima:", json_data)

            # Mengakses nilai-nilai dalam data JSON
            command = json_data['command']
            id = json_data['id']
            #print(command, " | ", id)
            data = json_data['data']
            #print("Data")
            #print("ph: ", data['data0'], " | ", "turbidity: ", data['data1'])
            mode = json_data['mode']

# Fungsi untuk mengirim data JSON setiap 1 menit
def send_data_periodically():
    # Data JSON yang akan dikirim
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
                "volume": "19",
                "satuan": "liter",
                "status": ""
            }
        }

    while True:
        time.sleep(1)
        send_data_to_arduino(data)
        time.sleep(6)

send_data_thread = threading.Thread(target=send_data_periodically)
receive_data_thread = threading.Thread(target=read_serial_data)

# Menjalankan thread-thread tersebut
send_data_thread.start()
receive_data_thread.start()