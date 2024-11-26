import os
import sys
import re
import asyncio
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError, UnauthorizedError
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import data, pengaturan
from core import sesi_pyrogram

# File paths
file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

# Load configuration
config = data.baca(file_config)
api_id = config["api_id"]
api_hash = config["api_hash"]

client = None

# Fungsi untuk memulai client Telethon dan mendapatkan nomor telepon
async def masuk_telethon(jalur_file):
    global client
    client = TelegramClient(
        jalur_file.replace(".session", ""),
        api_id=api_id,
        api_hash=api_hash,
        device_model='Ulul Azmi',
        app_version='telethon'
    )
    await client.start()
    me = await client.get_me()

    # Membaca dan memperbarui file kode jika diperlukan
    kode = data.baca(file_kode)
    if str(me.phone) not in kode:
        kode[str(me.phone)] = ""
        data.simpan(file_kode, kode)

    return str(me.phone)

# Fungsi untuk mendaftar akun ke Telethon
async def daftar_telethon(jalur_file, nomor, nama, nama_file):
    try:
        print(f"Daftar ke Telethon dengan {nama} | {nomor}")
        client = TelegramClient(
            jalur_file.replace(".session", ""),
            api_id=api_id,
            api_hash=api_hash,
            device_model='Ulul Azmi',
            app_version='telethon'
        )
        
        await client.connect()

        if not await client.is_user_authorized():
            try:
                # Kirim permintaan kode otentikasi
                await client.send_code_request(nomor)
                print(f"Kode dikirim ke {nomor}")

                # Tunggu kode otentikasi (misalnya dari sesi Pyrogram)
                folder_pyrogram = os.path.join(os.path.dirname(__file__), '..', 'sessions', 'pyrogram')
                jalur_file = os.path.join(folder_pyrogram, nama_file)
                jalur_lab = pengaturan.salin_file(jalur_file)
                jalur_folder = os.path.dirname(jalur_lab)
                kode = await sesi_pyrogram.kode_pyrogram(nama_file, jalur_folder)

                if kode:
                    # Login menggunakan kode otentikasi
                    await client.sign_in(phone=nomor, code=kode)
                else:
                    print("Kode otentikasi tidak ditemukan!")
                    return

            except SessionPasswordNeededError:
                kode = data.baca(file_kode)
                attempt = 0
                max_attempts = 3  # Maksimal percobaan untuk memasukkan password

                while attempt < max_attempts:
                    try:
                        # Gunakan password dari file jika ada
                        password = kode.get(nomor, "") or input("Masukkan password Anda: ")

                        # Coba login dengan password
                        await client.sign_in(password=password)
                        print("Login berhasil dengan password.")

                        # Simpan password jika login berhasil
                        kode[nomor] = password
                        data.simpan(file_kode, kode)
                        break  # Keluar dari loop jika login berhasil

                    except UnauthorizedError:
                        attempt += 1
                        print(f"Password salah. Anda memiliki {max_attempts - attempt} percobaan lagi.")

                        if attempt >= max_attempts:
                            print("Gagal login setelah beberapa percobaan.")
                            return

                    except Exception as e:
                        print(f"Kesalahan saat login dengan password: {e}")
                        return

        print(f"Login berhasil untuk nomor: {nomor}")

    except Exception as e:
        print(f"Kesalahan tidak terdugadi daftar_telethon: {e}")
    finally:
        # Pastikan klien dihentikan dengan aman
        try:
            if client.is_connected():
                await client.disconnect()
        except Exception as e:
            print(f"Kesalahan saat menghentikan klien: {e}")

# Fungsi untuk mengambil kode otentikasi dari pesan terakhir di Telethon
async def kode_telethon():
    global client
    while True:
        messages = await client.get_messages(777000, limit=1)
        if messages:
            last_message = messages[0]
            message_text = last_message.text
            message_time = last_message.date

            # Cek apakah pesan masih dalam rentang waktu 2 menit
            waktu_sekarang = datetime.now()
            batas_waktu = waktu_sekarang - timedelta(minutes=2)

            if message_time > batas_waktu:
                match = re.search(r'(\d{5,6})', message_text)
                if match:
                    kode = match.group(1)
                    print(f'Kode yang diterima: {kode}')
                    return kode

        await asyncio.sleep(1)  # Retry setiap detik jika kode tidak ditemukan

# Fungsi untuk keluar dari klien Telethon
async def keluar_telethon():
    global client
    await client.disconnect()
