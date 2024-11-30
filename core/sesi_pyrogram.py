import os
import sys
# Tambahkan path untuk mengakses modul dari direktori lain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Fungsi untuk masuk menggunakan sesi Pyrogram
async def masuk_pyrogram(nama, workdir):
    import gc
    from pyrogram import Client
    from helpers import data

    # Definisi path ke folder dan file yang digunakan
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')
    file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

    # Baca konfigurasi API dari file
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]

    
    app = None  # Inisialisasi klien Pyrogram
    try:
        app = Client(
            name=nama.replace(".session", ""),
            api_id=api_id,
            api_hash=api_hash,
            workdir=workdir,
            device_model='Ulul Azmi',
            app_version='pyrogram'
        )
        await app.connect()
        me = await app.get_me()
    except Exception as e:
        print(f"Kesalahan saat menghubungkan ke Pyrogram: {e}")
        session_file = os.path.join(folder_pyrogram, nama)
        if os.path.exists(session_file):
            os.remove(session_file)
            print("File sesi telah dihapus. Silakan login kembali.")
        return None

    # Pastikan data kode tersedia dan disimpan
    kode = {}
    try:
        kode = data.baca(file_kode)
    except Exception as e:
        print(f"Kesalahan saat membaca file kode: {e}")

    if str(me.phone_number) not in kode:
        kode[str(me.phone_number)] = ""
        try:
            data.simpan(file_kode, kode)
        except Exception as e:
            print(f"Kesalahan saat menyimpan file kode: {e}")

    nama_pengguna = f"{me.first_name} {me.last_name}"
    nomor_telepon = str(me.phone_number)

    # Hentikan klien dengan aman
    if app:
        try:
            if app.is_connected:
                await app.stop()
        except Exception as e:
            print(f"Kesalahan saat menghentikan klien: {e}")

    print("Terhubung ke Pyrogram")
    print(f"{nomor_telepon} {nama_pengguna}")
    # Bebaskan semua sumber daya yang terkait dengan Pyrogram
    del app
    gc.collect()  # Memastikan tidak ada referensi residual
    return nomor_telepon, nama_pengguna

# Fungsi untuk mendaftar sesi Pyrogram menggunakan nomor telepon
async def daftar_pyrogram(name, phone_number, workdir):
    import asyncio
    import gc
    from pyrogram import Client
    from pyrogram.errors import SessionPasswordNeeded, Unauthorized
    from helpers import data
    from core import sesi_telethon

    # Definisi path ke folder dan file yang digunakan
    file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

    # Baca konfigurasi API dari file
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]

    
    app = Client(
        name=name.replace(".session", ""),
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    )
    try:
        await app.start()
        await app.send_code(phone_number)
        await asyncio.sleep(2)
        kode = await sesi_telethon.kode_telethon()
        await app.sign_in(phone_number, kode)
    except SessionPasswordNeeded:
        # Penanganan sesi yang membutuhkan kata sandi
        kode = data.baca(file_kode)
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                password = kode.get(phone_number, "") or input("Masukkan password Anda: ")
                await app.check_password(password)
                kode[phone_number] = password
                data.simpan(file_kode, kode)
                print("Login berhasil dengan password.")
                break
            except Unauthorized:
                print(f"Password salah. Sisa percobaan: {max_attempts - attempt - 1}")
                if attempt == max_attempts - 1:
                    print("Gagal login setelah beberapa percobaan.")
                    raise
    
    finally:
        # Pastikan sesi dihentikan
        if app.is_connected:
            await app.stop()
            
    # Bebaskan semua sumber daya yang terkait dengan Pyrogram
    del app
    gc.collect()  # Memastikan tidak ada referensi residual
        
    print("Sesi berhasil dibuat!")
    
# Fungsi untuk menangkap kode Pyrogram dari chat Telegram
async def kode_pyrogram(nama, workdir):
    import re
    import gc
    import asyncio

    from helpers import data
    from pyrogram import Client

    # Definisi path ke folder dan file yang digunakan
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

    # Baca konfigurasi API dari file
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]

    app = Client(
        name=nama.replace(".session", ""),
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    )
    await app.start()
    while True:
        try:
            async for message in app.get_chat_history(777000, limit=1):
                match = re.search(r'(\d{5,6})', message.text)
                if match:
                    kode = match.group(1)
                    print(f"Kode yang diterima: {kode}")
                    await app.stop()
                    # Bebaskan semua sumber daya yang terkait dengan Pyrogram
                    del app
                    gc.collect()  # Memastikan tidak ada referensi residual

                    return kode
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Kesalahan saat mengambil kode: {e}")
            await asyncio.sleep(1)
            

async def daftar_pyrogram_dari_gramjs_string(name, phone_number, workdir):
    import gc
    import shutil
    import asyncio
    import subprocess
    from helpers import data, pengaturan
    from pyrogram import Client
    from pyrogram.errors import (
        SessionPasswordNeeded, FloodWait, PhoneCodeInvalid, 
        PhoneNumberInvalid, BadRequest, Unauthorized, RPCError
    )

    # Definisi path ke folder dan file yang digunakan
    file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
    file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')
    file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')
    
    folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')
    jalur_simpan = os.path.join(folder_pyrogram, name)
    jalur_hasil = os.path.join(workdir, name)

    # Baca konfigurasi API dari file
    config = data.baca(file_config)
    api_id = config["api_id"]
    api_hash = config["api_hash"]
    
    app = Client(
        name=name.replace(".session", ""),
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    )
    try:
        print(f"Daftar ke pyrogram dengan {name} | {phone_number}")
        await app.connect()

        # Mengirim kode ke nomor telepon
        try:
            sent_code = await app.send_code(phone_number)
            phone_code_hash = sent_code.phone_code_hash
            # print(f"Kode terkirim ke nomor {phone_number}")
        except PhoneNumberInvalid:
            print("Nomor telepon tidak valid.")
            return
        except FloodWait as e:
            print(f"Tunggu {e.value} detik sebelum mencoba lagi.")
            await asyncio.sleep(e.value)
            return
        except BadRequest as e:
            print(f"Kesalahan permintaan: {e.MESSAGE}")
            return

        await asyncio.sleep(2)  # Waktu tunggu untuk pengiriman kode

        # Menjalankan skrip Node.js untuk mendapatkan kode
        try:
            folder_gramjs_string = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'gramjs_string')
            jalur_file = os.path.join(folder_gramjs_string, name)
            jalur_lab = pengaturan.salin_file(jalur_file)
            datasesi = data.baca(file_data)
            datasesi.update({"folder_uji": jalur_lab})
            data.simpan(file_data, datasesi)
            kode_gramjs_string = os.path.join("core", "js", "kode_gramjs_string.js")
            subprocess.run(["node", kode_gramjs_string], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Kesalahan saat menjalankan skrip Node.js: {e}")
            return
        except FileNotFoundError:
            print("Skrip Node.js tidak ditemukan. Pastikan file 'kode_gramjs_string.js' ada di lokasi yang benar.")
            return

        # Membaca kode yang telah disimpan
        try:
            data_file = data.baca(file_data)
            kode = data_file.get("kode", None)
            # print(f"Kode: {kode}")
            if not kode:
                raise ValueError("Kode tidak ditemukan dalam file data.")
        except Exception as e:
            print(f"Kesalahan saat membaca kode dari file: {e}")
            return

        # Melakukan login dengan kode dan phone_code_hash
        try:
            await app.sign_in(phone_number=phone_number, phone_code=kode, phone_code_hash=phone_code_hash)
            
            shutil.copy2(jalur_hasil, jalur_simpan)

        except SessionPasswordNeeded:
            # Baca data password yang disimpan
            kode = data.baca(file_kode)
            max_attempts = 3  # Maksimal percobaan untuk memasukkan password
            attempt = 0

            while attempt < max_attempts:
                try:
                    # Jika password sudah ada di file, gunakan
                    if phone_number in kode and kode[phone_number] != "":
                        password = kode[phone_number]
                    else:
                        # Jika tidak ada password, minta dari pengguna
                        password = input("Masukkan password Anda: ")

                    # Coba login dengan password
                    await app.check_password(password)
                    print("Login berhasil dengan password.")

                    # Simpan password hanya jika login berhasil
                    kode[phone_number] = password
                    data.simpan(file_kode, kode)
                    
                    shutil.copy2(jalur_hasil, jalur_simpan)

                    break  # Keluar dari loop jika login berhasil

                except Unauthorized:
                    # Jika password salah, beri peringatan dan ulangi
                    attempt += 1
                    print(f"Password salah. Anda memiliki {max_attempts - attempt} percobaan lagi.")
                    
                    if attempt >= max_attempts:
                        print("Gagal login setelah beberapa percobaan. Silakan cek kembali password Anda.")
                        raise

        except PhoneCodeInvalid:
            print("Kode yang dimasukkan salah.")
            return
        except Unauthorized as e:
            print(f"Tidak berizin: {e.MESSAGE}")
            return
        except RPCError as e:
            print(f"Kesalahan RPC: {e.MESSAGE}")
            return

        print("Login berhasil. Sesi disimpan.")

    except Exception as e:
        print(f"Kesalahan tidak terduga: {e}")

    finally:
        try:
                await app.stop()
        except ConnectionError:
            pass
        except Exception as e:
            print(f"Kesalahan saat menghentikan klien: {e}")
            
    
    # Bebaskan semua sumber daya yang terkait dengan Pyrogram
    del app
    gc.collect()  # Memastikan tidak ada referensi residual

    print("Sesi berhasil dibuat!")
    