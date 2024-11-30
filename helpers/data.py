# Fungsi untuk membaca data dari file JSON
def baca(nama_file):
    import json
    with open(nama_file, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data

# Fungsi untuk menyimpan data ke file JSON
def simpan(nama_file, data):
    import json
    with open(nama_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
