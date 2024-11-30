import os

# Membersihkan terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Daftar jalur folder yang ingin dibuat
folders = [
    os.path.join(os.path.dirname(__file__), 'sessions', 'gramjs_string'),
    os.path.join(os.path.dirname(__file__), 'sessions', 'lupa'),
    os.path.join(os.path.dirname(__file__), 'sessions', 'pyrogram'),
    os.path.join(os.path.dirname(__file__), 'sessions', 'telethon'),
    os.path.join(os.path.dirname(__file__), 'selesai', 'gramjs_string'),
    os.path.join(os.path.dirname(__file__), 'selesai', 'pyrogram'),
    os.path.join(os.path.dirname(__file__), 'selesai', 'telethon'),
    os.path.join(os.path.dirname(__file__), 'core', 'lab', '1'),
    os.path.join(os.path.dirname(__file__), 'core', 'lab', '2'),
    os.path.join(os.path.dirname(__file__), 'core', 'lab', '3'),
    os.path.join(os.path.dirname(__file__), 'core', 'lab', '4'),
]

# Membuat folder jika belum ada
for folder in folders:
    os.makedirs(folder, exist_ok=True)

def main():
    from helpers import menu
    # Memanggil fungsi menu utama
    menu.main_menu()

if __name__ == "__main__":
    # Mengeksekusi program jika skrip ini dijalankan langsung
    main()
