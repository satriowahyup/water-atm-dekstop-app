import json

# Membaca data dari file JSON
with open('setting.json') as file:
    data = json.load(file)

# Mencetak nilai awal
print("Nilai awal:")
print("ID:", data['id'])
print("pH:", data['ph'])
print("Turbidity:", data['turbidity'])
print()

# Memperbarui nilai
data['ph'] = "0.23"
data['turbidity'] = "3.4"

# Menulis kembali data ke file JSON
with open('setting.json', 'w') as file:
    json.dump(data, file, indent=4)

# Membaca dan mencetak nilai yang diperbarui
with open('setting.json') as file:
    updated_data = json.load(file)

print("Nilai yang diperbarui:")
print("ID:", updated_data['id'])
print("pH:", updated_data['ph'])
print("Turbidity:", updated_data['turbidity'])