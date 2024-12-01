async def periksa_folder_lupa():
    import os
    import shutil
    import subprocess

    from pyrogram import Client as PyroClient
    from telethon import TelegramClient
    from helpers import pengaturan, data
            
    # Konfigurasi file
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
    file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')

    # Folder sesi
    folder_lupa = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'lupa')
    folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')

    # Membaca konfigurasi API
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]

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

def selesai_simpan(nama_file):
    import os
    import json
    import shutil
    
    # Konfigurasi file
    file_selesai = os.path.join(os.path.dirname(__file__), '..', 'config', 'selesai.json')

    # Folder sesi
    folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
    folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')
    
    # Tentukan direktori tujuan untuk masing-masing kategori
    base_dir = os.path.dirname(__file__)
    selesai_gramjs_string = os.path.join(base_dir, '..', 'selesai', 'gramjs_string')
    selesai_telethon = os.path.join(base_dir, '..', 'selesai', 'telethon')
    selesai_pyrogram = os.path.join(base_dir, '..', 'selesai', 'pyrogram')

    # Struktur awal untuk menyimpan error
    selesai_error = {"telethon": [], "pyrogram": [], "gramjs_string": []}

    # Jika file selesai.json belum ada, buat dengan struktur awal
    if not os.path.exists(file_selesai):
        with open(file_selesai, 'w') as f:
            json.dump(selesai_error, f, indent=4)

    # Tangani pemindahan file dengan error handling
    try:
        shutil.move(
            os.path.join(folder_telethon, nama_file),
            os.path.join(selesai_telethon, nama_file)
        )
    except Exception:
        selesai_error["telethon"].append(nama_file)
        print(f"Terjadi kesalahan saat memindahkan gramjstelethon_string '{nama_file}': {str(e)}")

    try:
        shutil.move(
            os.path.join(folder_pyrogram, nama_file),
            os.path.join(selesai_pyrogram, nama_file)
        )
    except Exception as e:
        selesai_error["pyrogram"].append(nama_file)
        print(f"Terjadi kesalahan saat memindahkan pyrogram '{nama_file}': {str(e)}")

    try:
        shutil.move(
            os.path.join(folder_gramjs_string, nama_file),
            os.path.join(selesai_gramjs_string, nama_file)
        )
    except Exception:
        selesai_error["gramjs_string"].append(nama_file)
        print(f"Terjadi kesalahan saat memindahkan gramjs_string '{nama_file}': {str(e)}")

    # Simpan error ke file selesai.json
    with open(file_selesai, 'w') as f:
        json.dump(selesai_error, f, indent=4)
        
async def periksa_sesi():
    import sys
    import os
    import subprocess

    from pyrogram import Client as PyroClient
    from telethon import TelegramClient
    from helpers import pengaturan, data
    
    # Konfigurasi file
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')

    # Folder sesi
    folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
    folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')

    # Membaca konfigurasi API
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]

    daftar_file_telethon = []
    daftar_file_pyrogram = []
    daftar_file_gramjs_string = []

    
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
    
    else:
        
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari Telethon | {nama_file}")
            berhasil_diproses += 1
            pengaturan.ruang_kerja()
            jalur_sesi = os.path.join(folder_telethon, nama_file)
            jalur_lab = pengaturan.salin_file(jalur_sesi)
            client = TelegramClient(jalur_lab.replace(".session", ""), api_id, api_hash)
            try:
                await client.connect()
                me = await client.get_me()
                print(f"{me.phone} | {me.first_name} {me.last_name} adalah sesi Telethon.\n")
                await client.disconnect()
                daftar_file_telethon += [nama_file]
            except Exception:
                await client.disconnect()
                print("Belum melakukan login")
                os.remove(jalur_sesi)
                print("File dihapus\n")
                continue
            
    # Memeriksa file sesi di folder Pyrogram
    file_sesi = [f for f in os.listdir(folder_pyrogram) if f.endswith('.session')]
    
    if not file_sesi:
        print("Tidak ada file sesi di folder Pyrogram.")

    else:
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari Pyrogram | {nama_file}")
            berhasil_diproses += 1
            pengaturan.ruang_kerja()
            jalur_sesi = os.path.join(folder_pyrogram, nama_file)
            jalur_lab = pengaturan.salin_file(jalur_sesi)
            jalur_folder = os.path.dirname(jalur_lab)
            app = PyroClient(
                name=nama_file.replace(".session", ""),
                api_id=api_id,
                api_hash=api_hash,
                workdir=jalur_folder,
            )
            try:
                await app.connect()
                me = await app.get_me()
                print(f"[{me.phone_number} | {me.first_name} {me.last_name} adalah sesi Pyrogram.\n")
                await app.disconnect()
                daftar_file_pyrogram += [nama_file]
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
        print("Tidak ada file sesi di folder gramjs_string.")

    else:
        # Memproses setiap file sesi
        berhasil_diproses = 0
        total_file_sesi = len(file_sesi)
        for nama_file in file_sesi:
            print(f"[{berhasil_diproses + 1}/{total_file_sesi}] dari gramjs_string | {nama_file}")
            berhasil_diproses += 1
            pengaturan.ruang_kerja()
            jalur_sesi = os.path.join(folder_gramjs_string, nama_file)
            jalur_lab = pengaturan.salin_file(jalur_sesi)
            periksa_data = data.baca(file_data)
            periksa_data.update({"folder_uji": jalur_lab, "folder_sumber": jalur_sesi, "nama_file": nama_file})
            data.simpan(file_data, periksa_data)
            node_script = os.path.join("core", "js", "periksa_sesi.js")
            subprocess.run(["node", node_script])
            periksa_data = data.baca(file_data)
            if periksa_data["nama_file"] == "":
                continue
            else:
                daftar_file_gramjs_string += [nama_file]
                
    selesai = list(
        set(daftar_file_telethon) & 
        set(daftar_file_pyrogram) & 
        set(daftar_file_gramjs_string)
    )
    
    if selesai:
        for nama_file in selesai:
            selesai_simpan(nama_file)

# Periksa perbedaan sesi antar folder
def periksa_perbedaan_sessions():
    import os

    # Folder sesi
    folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
    folder_telethon = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'telethon')
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')

    
    """Periksa perbedaan file sesi antar folder."""
    pyrogram_files = {file for file in os.listdir(folder_pyrogram) if file.endswith(".session")}
    telethon_files = {file for file in os.listdir(folder_telethon) if file.endswith(".session")}
    gramjs_files = {file for file in os.listdir(folder_gramjs_string) if file.endswith(".session")}

    return {
        "hanya_di_pyrogram": sorted(pyrogram_files - telethon_files),
        "hanya_di_telethon": sorted(telethon_files - pyrogram_files),
        "hanya_di_gramjs_string": sorted(gramjs_files - pyrogram_files),
    }
