
# Menampilkan menu utama dan menangani pilihan pengguna
def main_menu():
    import sys
    import asyncio
    from core import periksa, auto_login

    while True:
        print("""
        Menu Utama:
        1. Auto Login
        2. Membuat sesi baru
        3. Pengaturan
        4. Keluar
        """)

        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            asyncio.run(periksa.periksa_folder_lupa())
            asyncio.run(auto_login.autologin())
            asyncio.run(periksa.periksa_sesi())
        elif pilihan == "2":
            sesi_baru()
        elif pilihan == "3":
            menu_pengaturan()
        elif pilihan == "4":
            print("Keluar dari program.")
            sys.exit(1)
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

# Menampilkan menu pengaturan dan menangani pilihan pengguna
def menu_pengaturan():
    from helpers import pengaturan

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

def sesi_baru():
    import subprocess
    import os
    import asyncio
    from core import periksa, auto_login

    while True:
        print("""
        Membuat sesi baru:
        1. Dengan Nomor
        2. Dengan QRCode
        3. Kembali
        """)
        
        pilihan = input("Pilih: ")
        
        if pilihan == "1":
            jalur_file = os.path.join("core", "js", "daftar_nomor.js")
            try:
                subprocess.run(["node", jalur_file])
            except subprocess.TimeoutExpired:
                print("Proses login dengan QRCode melebihi batas waktu.")
            except KeyboardInterrupt:
                print("Proses dihentikan oleh pengguna.")
                
            asyncio.run(periksa.periksa_folder_lupa())
            asyncio.run(auto_login.autologin())
            asyncio.run(periksa.periksa_sesi())
            
        elif pilihan == "2":
            jalur_file = os.path.join("core", "js", "daftar_qrcode.js")
            try:
                subprocess.run(["node", jalur_file])
            except subprocess.TimeoutExpired:
                print("Proses login dengan QRCode melebihi batas waktu.")
            except KeyboardInterrupt:
                print("Proses dihentikan oleh pengguna.")
                
            asyncio.run(periksa.periksa_folder_lupa())
            asyncio.run(auto_login.autologin())
            asyncio.run(periksa.periksa_sesi())
            
        elif pilihan == "3":
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")
