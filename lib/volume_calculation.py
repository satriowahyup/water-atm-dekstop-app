import json

def volume_calculation(total_volume):
        # Baca file JSON
        file_path = 'volume.json'
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Update nilai total
        data['total'] = data['total'] + float(total_volume)

        # Tulis kembali ke file JSON
        with open(file_path, 'w') as file:
            json.dump(data, file)