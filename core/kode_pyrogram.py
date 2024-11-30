import os
import sys
import re
import asyncio
import subprocess
from pyrogram import Client
from pyrogram.errors import SessionPasswordNeeded
from datetime import datetime, timedelta

# Menambahkan jalur core dan helpers ke path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from helpers import data
from core import sesi_telethon

# File konfigurasi dan sesi
file_kode = os.path.join(os.path.dirname(__file__), '..', 'config', 'kode.json')
file_data = os.path.join(os.path.dirname(__file__), '..', 'config', 'data.json')
file_config = os.path.join(os.path.dirname(__file__), '..', 'config', 'config.json')

# Membaca konfigurasi API
config = data.baca(file_config)
api_id = config["api_id"]
api_hash = config["api_hash"]

# Fungsi masuk Pyrogram
async def masuk_pyrogram(name, workdir):
    """Login ke akun Pyrogram menggunakan file sesi."""
    async with Client(
        name=name.replace(".session", ""),
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    ) as app:
        me = await app.get_me()
        kode = data.baca(file_kode)
        if str(me.phone_number) not in kode:
            kode[str(me.phone_number)] = ""
            data.simpan(file_kode, kode)
        return str(me.phone_number)

# Fungsi mendaftar Pyrogram
async def daftar_pyrogram(name, phone_number, workdir):
    """Daftar sesi Pyrogram baru."""
    async with Client(
        name=name.replace(".session", ""),
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    ) as app:
        try:
            await app.send_code(phone_number)
            await asyncio.sleep(2)
            kode = await sesi_telethon.kode_telethon()
            await app.sign_in(phone_number, kode)
        except SessionPasswordNeeded:
            kode = data.baca(file_kode)
            password = kode.get(phone_number, input("Masukkan password Anda: "))
            kode[phone_number] = password
            data.simpan(file_kode, kode)
            await app.check_password(password)
        print("Sesi berhasil dibuat!")

# Fungsi mendaftar Pyrogram dari GramJS String
async def daftar_pyrogram_dari_gramjs_string(name, phone_number, workdir):
    """Daftar Pyrogram menggunakan kode dari GramJS String."""
    async with Client(
        name=name.replace(".session", ""),
        phone_number=phone_number,
        api_id=api_id,
        api_hash=api_hash,
        workdir=workdir,
        device_model='Ulul Azmi',
        app_version='pyrogram'
    ) as app:
        try:
            await app.send_code(phone_number)
            await asyncio.sleep(2)
            kode_gramjs_string = os.path.join("core", "js", "kode_gramjs_string.js")
            subprocess.run(["node", kode_gramjs_string])
            data_file = data.baca(file_data)
            kode = data_file["kode"]
            await app.sign_in(phone_number, kode)
        except SessionPasswordNeeded:
            kode = data.baca(file_kode)
            password = kode.get(phone_number, input("Masukkan password Anda: "))
            kode[phone_number] = password
            data.simpan(file_kode, kode)
            await app.check_password(password)
        print("Sesi berhasil dibuat!")

# Fungsi mendapatkan kode verifikasi
async def kode_pyrogram(timeout=120):
    """Mendapatkan kode verifikasi dari Telegram."""
    batas_waktu = datetime.now() - timedelta(seconds=timeout)
    async with app:
        while True:
            messages = await app.get_messages(777000, limit=1)
            if messages:
                last_message = messages[0]
                if last_message.date > batas_waktu:
                    match = re.search(r'(\d{5,6})', last_message.text)
                    if match:
                        return match.group(1)
            await asyncio.sleep(1)
