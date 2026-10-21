<div align="center">

# 🔑 Telegram AutoSessionLogin & Multi-Format Converter
### *Universal Session Manager, Converter, & Auto-Login for Pyrogram, Telethon, & GramJS*

[![Stars](https://img.shields.io/github/stars/ululazmi18/AutoSessionLogin?style=for-the-badge&color=gold)](https://github.com/ululazmi18/AutoSessionLogin/stargazers)
[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Node.js](https://img.shields.io/badge/Node.js-18+-339933?style=for-the-badge&logo=node.js&logoColor=white)](https://nodejs.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

<p align="center">
  <a href="#-fitur-utama--key-features">Fitur</a> •
  <a href="#-arsitektur-format-sesi">Format Sesi</a> •
  <a href="#-instalasi--persyaratan">Instalasi</a> •
  <a href="#-panduan-penggunaan">Cara Pakai</a> •
  <a href="#-english-summary">English Summary</a>
</p>

</div>

---

## 🎯 Gambaran Umum (Overview)

**AutoSessionLogin** adalah platform utilitas terpadu untuk mengelola, mengonversi, memverifikasi status kesehatan, dan melakukan login otomatis pada multi-akun Telegram secara masal. 

Mendukung ekosistem tiga library Telegram terbesar di dunia:
1. **Pyrogram** (Python `.session` SQLite)
2. **Telethon** (Python `.session` SQLite)
3. **GramJS** (Node.js String Session)

---

## 🚀 Fitur Utama (Key Features)

- 🔄 **Konversi Lintas Library:** Ubah string session GramJS menjadi file `.session` Pyrogram atau Telethon, dan sebaliknya.
- 📱 **Multi-Metode Autentikasi:** Mendukung login nomor telepon, kode OTP otomatis, dan login berbasis QR Code.
- 🩺 **Session Health Checker:** Periksa apakah sesi Telegram masih aktif, terkena pembatasan (*SpamBlock / FloodWait*), atau sudah kedaluwarsa (*revoked*).
- 🗂️ **Manajemen Folder Terstruktur:** Otomatisasi pengelompokan akun yang siap digunakan (`sessions/`) dan akun yang selesai diproses (`selesai/`).
- 🖥️ **Menu Terminal Interaktif:** Dilengkapi menu TUI yang intuitif untuk kemudahan navigasi operasi multi-akun.

---

## 📑 Arsitektur Format Sesi yang Didukung

| Library | Bahasa | Format File / Tipe | Karakteristik |
|---|:---:|---|---|
| **Pyrogram** | Python | `.session` (SQLite) | Standar bot & userbot modern di Python. |
| **Telethon** | Python | `.session` (SQLite) | Format matang untuk otomasi Telegram skala besar. |
| **GramJS** | JavaScript | String Session (Base64) | Portabel, cocok untuk web app, cloud function, & Node.js. |

---

## 📥 Panduan Instalasi (Installation)

### 1. Kloning Repositori
```bash
git clone https://github.com/ululazmi18/AutoSessionLogin.git
cd AutoSessionLogin
```

### 2. Pasang Dependensi Python & Node.js
```bash
# Dependensi Python
pip install pyrogram telethon

# Dependensi Node.js (GramJS)
npm install
```

---

## 🚀 Panduan Penggunaan

1. **Jalankan Aplikasi:**
   ```bash
   python main.py
   ```
2. **Pilih Menu Operasi pada Antarmuka Terminal:**
   - Masukkan kredensial API ID & API Hash Telegram Anda di `config/config.json`.
   - Pilih opsi pembuatan sesi baru (via Nomor HP atau QR Code).
   - Jalankan verifikasi sesi untuk memeriksa status validitas seluruh akun.
   - Konversi sesi antar format sesuai kebutuhan bot tujuan Anda.

---

## 🌐 English Summary

**AutoSessionLogin** is an all-in-one Telegram session lifecycle management and conversion toolkit supporting **Pyrogram**, **Telethon**, and **GramJS** environments.

- **Cross-Framework Bridge:** Effortlessly convert between Pyrogram/Telethon SQLite databases and GramJS String Sessions.
- **Automated Verification:** Batch health audits to identify alive, muted, or terminated sessions.
- **Interactive Terminal Workflow:** Clean CLI interface designed for streamlined multi-account administration.

---

## 📄 Lisensi (License)

Didistribusikan di bawah Lisensi **MIT**. Gunakan secara bertanggung jawab sesuai Ketentuan Layanan Telegram. Dibuat oleh [**Ulul Azmi**](https://github.com/ululazmi18).
