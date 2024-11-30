# Fungsi untuk mengatur API ID dan API Hash
def api():
    import os
    from helpers import data

    api_id_input = input("\nMasukkan API ID: ")
    if api_id_input == "":
        return
    api_id = int(api_id_input)
    api_hash = input("Masukkan API Hash: ")
    
    config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.json")
    
    config = data.baca(config_path)
    
    config["api_id"] = api_id
    config["api_hash"] = api_hash
    
    data.simpan(config_path, config)
    
    input("\nTekan ENTER untuk kembali")

# Fungsi untuk menghapus data dan membersihkan folder lab
def ruang_kerja():
    import os
    from helpers import data

    # Menghapus konten data.json
    data_path = os.path.join(os.path.dirname(__file__), "..", "config", "data.json")
    datafile = data.baca(data_path)
    for key in datafile:
        datafile[key] = ""
    data.simpan(data_path, datafile)
    
    # Daftar folder lab yang perlu dibuat dan dibersihkan
    folder_paths = [
        os.path.join(os.path.dirname(__file__), "..", "core", "lab", "1"),
        os.path.join(os.path.dirname(__file__), "..", "core", "lab", "2"),
        os.path.join(os.path.dirname(__file__), "..", "core", "lab", "3"),
        os.path.join(os.path.dirname(__file__), "..", "core", "lab", "4"),
    ]
    
    for folder_path in folder_paths:
        os.makedirs(folder_path, exist_ok=True)  # Membuat folder jika belum ada
        bersihkan_folder(folder_path)           # Bersihkan folder

# Fungsi untuk membersihkan folder (menghapus file dan subfolder)
def bersihkan_folder(folder_lab):
    import shutil
    import os

    if os.path.exists(folder_lab):  # Pastikan folder ada
        for item in os.listdir(folder_lab):
            item_path = os.path.join(folder_lab, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)  # Hapus file atau link
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)  # Hapus folder
            except Exception:
                pass
                
def salin_file(jalur_sumber):
    import shutil
    import os

    file = os.path.basename(jalur_sumber)
    
    folder_lab = os.path.join(os.path.dirname(__file__), '..', 'core', 'lab')
    folder_1 = os.path.join(folder_lab, '1')
    folder_2 = os.path.join(folder_lab, '2')
    folder_3 = os.path.join(folder_lab, '3')
    folder_4 = os.path.join(folder_lab, '4')
    
    jalur_1 = os.path.join(folder_1, file)
    jalur_2 = os.path.join(folder_2, file)
    jalur_3 = os.path.join(folder_3, file)
    jalur_4 = os.path.join(folder_4, file)
    
    try:
        os.remove(jalur_1)
    except Exception:
        pass
    
    try:
        os.remove(jalur_2)
    except Exception:
        pass
    
    try:
        os.remove(jalur_3)
    except Exception:
        pass
    
    try:
        os.remove(jalur_4)
    except Exception:
        pass
    
    if not os.path.exists(jalur_1):
        shutil.copy2(jalur_sumber, jalur_1)
        return jalur_1
    elif not os.path.exists(jalur_2):
        shutil.copy2(jalur_sumber, jalur_2)
        return jalur_2
    elif not os.path.exists(jalur_3):
        shutil.copy2(jalur_sumber, jalur_3)
        return jalur_3
    elif not os.path.exists(jalur_4):
        shutil.copy2(jalur_sumber, jalur_4)
        return jalur_4
    
def folder_uji(nama_ile):
    import os

    folder_lab = os.path.join(os.path.dirname(__file__), '..', 'core', 'lab')
    folder_1 = os.path.join(folder_lab, '1')
    folder_2 = os.path.join(folder_lab, '2')
    folder_3 = os.path.join(folder_lab, '3')
    folder_4 = os.path.join(folder_lab, '4')
    
    jalur_1 = os.path.join(folder_1, nama_ile)
    jalur_2 = os.path.join(folder_2, nama_ile)
    jalur_3 = os.path.join(folder_3, nama_ile)
    jalur_4 = os.path.join(folder_4, nama_ile)
    
    try:
        os.remove(jalur_1)
    except Exception:
        pass
    
    try:
        os.remove(jalur_2)
    except Exception:
        pass
    
    try:
        os.remove(jalur_3)
    except Exception:
        pass
    
    try:
        os.remove(jalur_4)
    except Exception:
        pass
    
    if not os.path.exists(jalur_1):
        return folder_1
    elif not os.path.exists(jalur_2):
        return folder_2
    elif not os.path.exists(jalur_3):
        return folder_3
    elif not os.path.exists(jalur_4):
        return folder_4
    
    