const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const fs = require("fs");
const path = require("path");
const moment = require("moment");

// Logger untuk debugging
const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

// Konfigurasi
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const dataPath = path.join(__dirname, "..", "..", "config", "data.json");

// Membaca file konfigurasi
const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));

// Membaca data JSON
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
const sessionPath = data.folder_uji; // Jalur folder untuk file sesi

// Fungsi untuk membaca sesi dari file
async function getSessionData() {
    try {
        return await fs.promises.readFile(sessionPath, "utf-8");
    } catch (err) {
        console.error(`Gagal membaca sesi: ${err.message}`);
        process.exit(1);
    }
}

// Fungsi untuk mendapatkan pesan terbaru dari user ID 777000
async function ambilKodeVerifikasi(client) {
    const duaMenitLalu = moment().subtract(2, "minutes");

    while (true) {
        try {
            // Mengambil pesan dari user ID 777000
            const messages = await client.getMessages("777000", { limit: 1 });
            if (messages.length > 0) {
                const pesan = messages[0];
                const teksPesan = pesan.message;
                const waktuPesan = moment(pesan.date * 1000); // UNIX timestamp ke moment object

                // Periksa apakah pesan baru
                if (waktuPesan.isAfter(duaMenitLalu)) {
                    const match = teksPesan.match(/(\d{5,6})/); // Cari kode verifikasi
                    if (match) {
                        const kode = match[1];
                        console.log(`Kode verifikasi ditemukan: ${kode}`);

                        // Simpan ke file data.json
                        data.kode = kode;
                        await fs.promises.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");

                        return kode;
                    }
                } else {
                    console.log("Pesan terlalu lama, menunggu pesan baru...");
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
        baseLogger: logger2,
    });

    try {
        console.log("Memulai klien Telegram...");
        await client.start();
        console.log("Klien berhasil dimulai.");

        const kodeVerifikasi = await ambilKodeVerifikasi(client);

        if (kodeVerifikasi) {
            console.log(`Kode verifikasi berhasil diambil: ${kodeVerifikasi}`);
        } else {
            console.log("Tidak ada kode verifikasi ditemukan.");
        }
    } catch (err) {
        console.error(`Terjadi kesalahan: ${err.message}`);
    } finally {
        try {
            console.log("Menutup koneksi klien...");
            await client.disconnect();
            await client.destroy();
            console.log("Klien telah dihentikan.");
        } catch (disconnectErr) {
            console.error(`Kesalahan saat menutup klien: ${disconnectErr.message}`);
        }
    }
}

// Menjalankan program
utama().catch(logger2.error);