import sys
import asyncio
from helpers import pengaturan
from core import periksa, auto_login

# Menampilkan menu utama dan menangani pilihan pengguna
def main_menu():
    while True:
        print("""
        Menu Utama:
        1. Pengaturan
        2. Auto Login
        3. Periksa Sesi
        4. Keluar
        """)

        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            menu_pengaturan()
        elif pilihan == "2":
            asyncio.run(periksa.periksa_folder_lupa())
            asyncio.run(auto_login.autologin())
        elif pilihan == "3":
            asyncio.run(periksa.periksa_sesi())
        elif pilihan == "4":
            print("Keluar dari program.")
            sys.exit(1)
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

# Menampilkan menu pengaturan dan menangani pilihan pengguna
def menu_pengaturan():
    while True:
        print("""
        Pengaturan:
        1. API
        2. Kembali
        """)
        
        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            pengaturan.api()
        elif pilihan == "2":
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")
