import os
import sys
import shutil
import subprocess

# Menambahkan jalur folder utama ke sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modul dari direktori core dan helpers
from core import periksa, sesi_pyrogram, sesi_telethon
from helpers import data, pengaturan

folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')
folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')

# # Fungsi untuk migrasi dari sesi Telethon ke Pyrogram
# async def dari_telethon(data_telethon):
#     for nama_file in data_telethon:
#         print("\nMigrasi dari Telethon ke Pyrogram")
#         pengaturan.ruang_kerja()
#         print(f"\nMenggunakan file: {nama_file}")
#         jalur_file = os.path.join(folder_telethon, nama_file)
#         shutil.copy2(jalur_file, lab_telethon)
#         jalur_file = os.path.join(lab_telethon, nama_file)
        
#         phone_number = sesi_telethon.masuk_telethon(jalur_file)
#         sesi_pyrogram.daftar_pyrogram(nama_file, phone_number, lab_telethon)
#         sesi_telethon.keluar_telethon()

# Fungsi untuk migrasi dari Pyrogram ke Telethon
async def dari_pyrogram(data_pyrogram):
    for nama_file in data_pyrogram:
        print("\nMigrasi dari Pyrogram ke Telethon")
        pengaturan.ruang_kerja()
        print(f"\nMenggunakan file: {nama_file}")
        jalur_file = os.path.join(folder_pyrogram, nama_file)
        jalur_lab = pengaturan.salin_file(jalur_file)
        jalur_folder = os.path.dirname(jalur_lab)

        nomor, nama = await sesi_pyrogram.masuk_pyrogram(nama_file, jalur_folder)
        if nomor is None or nama is None:
            print("Gagal masuk ke Pyrogram. Menghentikan eksekusi.")
            continue

        jalur_file = os.path.join(folder_telethon, nama_file)
        await sesi_telethon.daftar_telethon(jalur_file, nomor, nama, nama_file)

# Fungsi untuk migrasi dari sesi GramJS String ke Pyrogram
async def dari_gramjs_string(data_gramjs_string):
    for nama_file in data_gramjs_string:
        print("\nMigrasi dari GramJS String ke Pyrogram")
        pengaturan.ruang_kerja()
        print(f"\nMenggunakan file: {nama_file}")
        jalur_file = os.path.join(folder_gramjs_string, nama_file)
        jalur_lab = pengaturan.salin_file(jalur_file)
        datasesi = data.baca(file_data)
        datasesi.update({"folder_uji": jalur_lab, "nama_file": nama_file})
        data.simpan(file_data, datasesi)

        masuk_gramjs_string = os.path.join("core", "js", "masuk_gramjs_string.js")
        subprocess.run(["node", masuk_gramjs_string])

        datasesi = data.baca(file_data)
        nomor = datasesi["Nomor"]
        await sesi_pyrogram.daftar_pyrogram_dari_gramjs_string(nama_file, nomor, folder_pyrogram)

# Fungsi utama untuk menjalankan proses Auto Login
async def autologin():
    print("Menjalankan Auto Login...")

    dataselisih = periksa.periksa_perbedaan_sessions()
    data_gramjs_string = dataselisih.get("hanya_di_gramjs_string", [])
    data_pyrogram = dataselisih.get("hanya_di_pyrogram", [])

    if data_gramjs_string:
        await dari_gramjs_string(data_gramjs_string)
        dataselisih = periksa.periksa_perbedaan_sessions()
        data_pyrogram = dataselisih.get("hanya_di_pyrogram", [])
        if data_pyrogram:
            await dari_pyrogram(data_pyrogram)

    if data_pyrogram:
        await dari_pyrogram(data_pyrogram)
