"use strict";

const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const fs = require("fs");
const path = require("path");

// Logger untuk debugging
const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

// Konfigurasi
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const dataPath = path.join(__dirname, "..", "..", "config", "data.json");

// Membaca file konfigurasi
let api_id, api_hash, sessionPath;
try {
    const config = JSON.parse(fs.readFileSync(configPath, "utf-8"));
    api_id = config.api_id;
    api_hash = config.api_hash;
} catch (err) {
    console.error(`Gagal membaca file konfigurasi: ${err.message}`);
    process.exit(1);
}

// Membaca data JSON
let data;
try {
    data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
    sessionPath = data.folder_uji;
} catch (err) {
    console.error(`Gagal membaca file data: ${err.message}`);
    process.exit(1);
}

// Fungsi untuk membaca sesi dari file
async function getSessionData() {
    try {
        return await fs.promises.readFile(sessionPath, "utf-8");
    } catch (err) {
        console.error(`Gagal membaca file sesi: ${err.message}`);
        process.exit(1);
    }
}

// Fungsi untuk mendapatkan pesan terbaru dari user ID 777000
async function ambilKodeVerifikasi(client) {
    while (true) {
        try {
            // Mengambil pesan dari user ID 777000
            const messages = await client.getMessages("777000", { limit: 1 });

            if (messages.length > 0) {
                const pesan = messages[0];
                const teksPesan = pesan.message;

                // Cari kode verifikasi (angka 5-6 digit) dalam teks pesan
                const match = teksPesan.match(/(\d{5,6})/);
                if (match) {
                    const kode = match[1];

                    // Simpan ke file data.json
                    data.kode = kode;
                    await fs.promises.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");

                    return kode;
                }
            } else {
                console.log("Tidak ada pesan ditemukan, menunggu...");
            }
        } catch (err) {
            console.error(`Kesalahan saat mengambil pesan: ${err.message}`);
        }

        // Tunggu 1 detik sebelum mencoba lagi
        await new Promise((resolve) => setTimeout(resolve, 1000));
    }
}

// Fungsi utama
async function utama() {
    const sessionData = await getSessionData();
    const client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
        connectionRetries: 5,
        timeout: 1800000,
        baseLogger: logger2
    });

    try {
        await client.start();

        const kodeVerifikasi = await ambilKodeVerifikasi(client);

        if (kodeVerifikasi) {
            console.log(`Kode verifikasi berhasil diambil: ${kodeVerifikasi}`);
        } else {
            console.log("Tidak ada kode verifikasi ditemukan.");
        }
    } catch (err) {
        console.error(`Terjadi kesalahan di fungsi utama: ${err.message}`);
    } finally {
        try {
            await client.disconnect();
            await client.destroy();
        } catch (disconnectErr) {
            console.error(`Kesalahan saat menutup klien: ${disconnectErr.message}`);
        }
    }
}

// Menjalankan program
utama();
