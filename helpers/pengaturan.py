import shutil
import os
from helpers import data

# Fungsi untuk mengatur API ID dan API Hash
def api():
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
    # Menghapus konten data.json
    data_path = os.path.join(os.path.dirname(__file__), "..", "config", "data.json")
    datafile = data.baca(data_path)
    for key in datafile:
        datafile[key] = ""
    data.simpan(data_path, datafile)
    
    # Membersihkan folder lab_gramjs_string
    bersihkan_folder(os.path.join(os.path.dirname(__file__), '..', 'core', 'lab', '1'))
    
    # Membersihkan folder lab_lupa
    bersihkan_folder(os.path.join(os.path.dirname(__file__), '..', 'core', 'lab', '2'))
    
    # Membersihkan folder lab_pyrogram
    bersihkan_folder(os.path.join(os.path.dirname(__file__), '..', 'core', 'lab', '3'))
    
    # Membersihkan folder lab_telethon
    bersihkan_folder(os.path.join(os.path.dirname(__file__), '..', 'core', 'lab', '4'))

# Fungsi untuk membersihkan folder (menghapus file dan subfolder)
def bersihkan_folder(folder_lab):
    if not os.path.exists(folder_lab):
        os.makedirs(folder_lab)
    else:
        for item in os.listdir(folder_lab):
            item_path = os.path.join(folder_lab, item)
            try:
                if os.path.isfile(item_path) or os.path.islink(item_path):
                    os.unlink(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)
            except Exception:
                pass

def salin_file(jalur_sumber):
    
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
    