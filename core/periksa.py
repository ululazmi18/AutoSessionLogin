import os
import sys
import shutil
import subprocess
from telethon import TelegramClient
from pyrogram import Client as PyroClient
from helpers import pengaturan, data

# Konfigurasi file
file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')

# Folder sesi
folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
folder_lupa = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'lupa')
folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')

# Membaca konfigurasi API
config = data.baca(file_config)
api_id = config["api_id"]
api_hash = config["api_hash"]

# Fungsi utama
async def periksa_folder_lupa():
    """Memindahkan sesi dari folder lupa ke folder tipe sesi yang sesuai."""
    
    os.makedirs(folder_lupa, exist_ok=True)

    session_files = [f for f in os.listdir(folder_lupa) if f.endswith('.session')]
    if not session_files:
        print("Tidak ada file sesi di folder lupa.")
        return

    print("Memproses sesi dari folder lupa...")
    kode_data = data.baca(file_kode)

    for nama_file in session_files:
        pengaturan.ruang_kerja()
        jalur_sumber = os.path.join(folder_lupa, nama_file)
        jalur_lab = pengaturan.salin_file(jalur_sumber)
        jalur_folder = os.path.dirname(jalur_lab)

        # Cek sesi dengan Telethon
        try:
            async with TelegramClient(jalur_lab.replace(".session", ""), api_id, api_hash) as client:
                me = await client.get_me()
                if str(me.phone) not in kode_data:
                    kode_data[str(me.phone)] = ""
                    data.simpan(file_kode, kode_data)
                print(f"{nama_file}: {me.phone} | {me.first_name} {me.last_name} adalah sesi Telethon.")
                nama_baru = f"{me.phone}.session"
                shutil.move(jalur_sumber, os.path.join(folder_telethon, nama_baru))
                continue  # Selesai untuk Telethon, lanjut ke file berikutnya
        except Exception as e:
            print(f"Telethon gagal untuk {nama_file}: {e}")

        # Cek sesi dengan Pyrogram
        try:
            async with PyroClient(
                name=nama_file.replace(".session", ""),
                api_id=api_id,
                api_hash=api_hash,
                workdir=jalur_folder,
            ) as app:
                me = await app.get_me()
                if str(me.phone_number) not in kode_data:
                    kode_data[str(me.phone_number)] = ""
                    data.simpan(file_kode, kode_data)
                print(f"{nama_file}: {me.phone_number} | {me.first_name} {me.last_name} adalah sesi Pyrogram.")
                nama_baru = f"{me.phone_number}.session"
                shutil.move(jalur_sumber, os.path.join(folder_pyrogram, nama_baru))
                continue  # Selesai untuk Pyrogram, lanjut ke file berikutnya
        except Exception as e:
            print(f"Pyrogram gagal untuk {nama_file}: {e}")

        # Jika gagal dengan kedua metode, gunakan GramJS (Node.js)
        periksa_data = data.baca(file_data)
        periksa_data.update({"folder_sumber": jalur_sumber, "folder_uji": jalur_lab, "nama_file": nama_file})
        data.simpan(file_data, periksa_data)
        node_script = os.path.join("core", "js", "periksa.js")
        subprocess.run(["node", node_script])

async def periksa_sesi():
    
    # Menentukan folder untuk sesi
    folder_sessions = os.path.join(os.path.dirname(__file__), '..', 'sessions')
    folder_telethon = os.path.join(folder_sessions, 'telethon')
    folder_pyrogram = os.path.join(folder_sessions, 'pyrogram')
    folder_gramjs_string = os.path.join(folder_sessions, 'gramjs_string')

    # Membuat folder jika belum ada
    os.makedirs(folder_telethon, exist_ok=True)
    os.makedirs(folder_pyrogram, exist_ok=True)
    os.makedirs(folder_gramjs_string, exist_ok=True)

    # Memeriksa file sesi di folder Telethon
    file_sesi = [f for f in os.listdir(folder_telethon) if f.endswith('.session')]
    
    if not file_sesi:
        print("Tidak ada file sesi di folder Telethon.")
        return

    else:
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari Telethon | {nama_file}")
            berhasil_diproses += 1
            jalur_sesi = os.path.join(folder_telethon, nama_file)
            client = TelegramClient(jalur_sesi.replace(".session", ""), api_id, api_hash)
            try:
                await client.connect()
                me = await client.get_me()
                print(f"{me.phone} | {me.first_name} {me.last_name} adalah sesi Telethon.\n")
                await client.disconnect()
            except Exception:
                await client.disconnect()
                print("Belum melakukan login")
                os.remove(jalur_sesi)
                print("File dihapus\n")
                continue
            
    # Memeriksa file sesi di folder Pyrogram
    file_sesi = [f for f in os.listdir(folder_pyrogram) if f.endswith('.session')]
    
    if not file_sesi:
        print("Tidak ada file sesi di folder Telethon.")
        return

    else:
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari Pyrogram | {nama_file}")
            berhasil_diproses += 1
            jalur_sesi = os.path.join(folder_pyrogram, nama_file)
            app = PyroClient(
                name=nama_file.replace(".session", ""),
                api_id=api_id,
                api_hash=api_hash,
                workdir=folder_pyrogram,
            )
            try:
                await app.connect()
                me = await app.get_me()
                print(f"[{me.phone_number} | {me.first_name} {me.last_name} adalah sesi Pyrogram.\n")
                await app.disconnect()
            except Exception as e:
                await app.disconnect()
                print(e)
                print("Belum melakukan login")
                os.remove(jalur_sesi)
                print("File dihapus\n")
                continue
                
    # Memeriksa file sesi di folder gramjs_string
    file_sesi = [f for f in os.listdir(folder_gramjs_string) if f.endswith('.session')]
    
    if not file_sesi:
        print("Tidak ada file sesi di folder Telethon.")
        return

    else:
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari gramjs_string | {nama_file}")
            berhasil_diproses += 1
            jalur_sesi = os.path.join(folder_gramjs_string, nama_file)
            periksa_data = data.baca(file_data)
            periksa_data.update({"folder_sumber": jalur_sesi, "nama_file": nama_file})
            data.simpan(file_data, periksa_data)
            node_script = os.path.join("core", "js", "periksa_sesi.js")
            subprocess.run(["node", node_script])


# Periksa perbedaan sesi antar folder
def periksa_perbedaan_sessions():
    """Periksa perbedaan file sesi antar folder."""
    pyrogram_files = {file for file in os.listdir(folder_pyrogram) if file.endswith(".session")}
    telethon_files = {file for file in os.listdir(folder_telethon) if file.endswith(".session")}
    gramjs_files = {file for file in os.listdir(folder_gramjs_string) if file.endswith(".session")}

    return {
        "hanya_di_pyrogram": sorted(pyrogram_files - telethon_files),
        "hanya_di_telethon": sorted(telethon_files - pyrogram_files),
        "hanya_di_gramjs_string": sorted(gramjs_files - pyrogram_files),
    }
