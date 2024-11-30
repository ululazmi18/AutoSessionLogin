const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const path = require("path");
const fs = require("fs");

// Logger untuk debugging
const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

// Membaca konfigurasi API dari file config.json
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));

// Membaca jalur dan data tambahan dari data.json
const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
const jalur_uji = data.folder_uji;

// Fungsi untuk membaca data sesi dari file
async function getSessionData() {
    try {
        return await fs.promises.readFile(jalur_uji, "utf-8");
    } catch (err) {
        console.error(`Gagal membaca sesi: ${err.message}`);
        process.exit(1);
    }
}

// Fungsi utama untuk menginisialisasi TelegramClient
async function main() {
    const sessionData = await getSessionData();

    // Membuat instance TelegramClient
    const client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
        connectionRetries: 5,
        timeout: 1800000, // 30 menit
        baseLogger: logger2,
    });

    try {
        // Memulai client
        await client.start();

        // Mendapatkan informasi akun
        const me = await client.getMe();

        if (!me) {
            throw new Error("Gagal mendapatkan informasi akun. Pastikan sesi valid.");
        }

        const nama = me.lastName ? `${me.firstName} ${me.lastName}` : me.firstName;

        // Validasi jika `me.phone` tidak ada
        const nomor = me.phone || "Nomor tidak tersedia";

        // Memperbarui data kode
        const kodePath = path.join(__dirname, "..", "..", "config", "kode.json");
        const kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));

        if (!kode[nomor]) {
            kode[nomor] = "";
            fs.writeFileSync(kodePath, JSON.stringify(kode, null, 4), "utf-8");
        }

        data.nama = nama;
        data.Nomor = nomor;

        fs.writeFileSync(dataPath, JSON.stringify(data, null, 4), "utf-8");

        console.log(`Menggunakan ${nama} | ${nomor}`);
        console.log("Terhubung ke gramjs_string");

    } catch (err) {
        console.error(`Terjadi kesalahan di masuk_gramjs_string: ${err.message}`);
    } finally {
        // Menutup koneksi client
        await client.disconnect();
        await client.destroy();
    }
}

// Menjalankan fungsi utama
main();
