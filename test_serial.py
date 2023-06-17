import json
import serial
import time
import schedule

# Fungsi untuk mengirim data JSON ke Arduino melalui komunikasi serial
def send_data_to_arduino(data):
    try:
        # Inisialisasi port serial
        ser = serial.Serial('/dev/ttyUSB0', 9600)  # Ganti dengan port serial yang sesuai
        
        # Mengubah data menjadi format JSON
        json_data = json.dumps(data)
        
        # Mengirim data ke Arduino melalui komunikasi serial
        ser.write(json_data.encode())
        ser.close()
        
        print("Data berhasil dikirim ke Arduino:", json_data)
        
    except:
        print("Terjadi kesalahan pada port serial:")

# Fungsi untuk mengatur jadwal pengiriman data setiap 5 menit
def schedule_job():
    # Data JSON yang akan dikirim
    data = {
        "id": "00001",
        "ph": 0.4,
        "turbidity": 3.4
    }
    
    # Mengirim data ke Arduino
    send_data_to_arduino(data)

# Mengatur jadwal pengiriman data setiap 2.5 menit
schedule.every(2.5).minutes.do(schedule_job)

while True:
    # Menjalankan tugas pada jadwal yang telah ditentukan
    schedule.run_pending()
    time.sleep(1)
