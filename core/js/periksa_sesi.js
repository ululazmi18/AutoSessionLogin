// Import modul yang diperlukan
const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const path = require("path");
const fs = require("fs/promises");
const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

// Jalur file konfigurasi dan folder sesi
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const folderGramjsString = path.join(__dirname, "..", "..", "sessions", "gramjs_string");
const cachePath = path.join(__dirname, "..", "..", "sessions", "session_cache.json");

// Fungsi untuk membaca konfigurasi API dari file config.json
async function loadConfig() {
    try {
        const configContent = await fs.readFile(configPath, "utf-8");
        return JSON.parse(configContent);
    } catch (error) {
        throw new Error(`Gagal membaca konfigurasi: ${error.message}`);
    }
}

// Fungsi untuk menghapus file dengan pengecekan keberadaan file
async function deleteFile(filePath) {
    try {
        const absolutePath = path.resolve(filePath); // Resolusi ke absolute path

        // Periksa apakah file ada sebelum mencoba menghapus
        try {
            await fs.access(absolutePath); // Mengecek apakah file dapat diakses
            await fs.unlink(absolutePath); // Menghapus file
            console.log(`File berhasil dihapus: ${absolutePath}\n`);
        } catch (err) {
            if (err.code === 'ENOENT') {
                console.log(`File tidak ditemukan: ${absolutePath}\n`); // File tidak ada
            } else {
                throw err; // Menangani error lainnya
            }
        }
    } catch (err) {
        console.error(`Error menghapus file: ${err.message}\n`);
    }
}

// Fungsi utama untuk memeriksa dan memproses sesi
async function checkSession() {
    const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
    let client; // Deklarasi variabel client di luar try-catch
    let jalurSesi; // Definisikan jalurSesi di luar blok try-catch
    let jalurlab;

    try {
        // Membaca data konfigurasi
        const { api_id, api_hash } = await loadConfig();

        // Membaca data dari file data.json
        const dataContent = await fs.readFile(dataPath, "utf-8");
        const data = JSON.parse(dataContent);
        jalurSesi = data.folder_sumber; // Mengambil jalur sesi dari data
        jalurlab = data.folder_uji;
        const namaFile = data.nama_file;     // Mengambil nama file dari data

        // Membaca data sesi dari file
        const sessionData = await fs.readFile(jalurlab, "utf-8");

        // Membuat instance TelegramClient
        client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
            connectionRetries: 5,
            timeout: 1800000,
            baseLogger: logger2,
        });

        // Menghubungkan ke Telegram
        await client.connect();

        // Mendapatkan informasi akun
        const me = await client.getMe();

        // Menampilkan informasi sesi
        const phoneNumber = me.phone;
        const name = me.lastName ? `${me.firstName} ${me.lastName}` : me.firstName;
        console.log(`${phoneNumber} | ${name} adalah sesi gramjs_string.\n`);

        // Menyimpan informasi sesi yang diperbarui ke data.json
        data.nama_file = namaFile;
        await fs.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");

    } catch (error) {
        console.error("Belum melakukan login atau terjadi kesalahan:", error.message);

        // Tangani kesalahan AUTH_KEY_UNREGISTERED
        if (error.message.includes("AUTH_KEY_UNREGISTERED")) {
            console.log("Kunci otentikasi tidak valid atau kedaluwarsa. Menghapus sesi lama...\n");
            if (jalurSesi) await deleteFile(jalurSesi); // Pastikan jalurSesi ada sebelum menghapus
        }

        // Hapus file sesi jika terjadi kesalahan lainnya
        if (error.code !== "ENOENT" && jalurSesi) {
            const dataContent = await fs.readFile(dataPath, "utf-8");
            const data = JSON.parse(dataContent);

            data.nama_file = "";
            await fs.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");

            // Menghapus file sesi jika terjadi kesalahan
            await deleteFile(jalurSesi);
        }
    } finally {
        // Menutup koneksi client jika ada
        if (client) {
            await client.disconnect();
            await client.destroy();
        }
    }
}

// Menjalankan fungsi utama
checkSession().catch(err => logger2.error(`Kesalahan saat menjalankan checkSession: ${err.message}`));
