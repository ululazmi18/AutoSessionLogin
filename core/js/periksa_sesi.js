// Import modul yang diperlukan
const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const path = require("path");
const fs = require("fs");
const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

// Jalur file konfigurasi dan folder sesi
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const folderGramjsString = path.join(__dirname, "..", "..", "sessions", "gramjs_string");

// Membaca konfigurasi API dari file config.json
const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));

// Fungsi untuk menghapus file
async function deleteFile(filePath) {
    try {
        const absolutePath = path.resolve(filePath);
        await fs.unlink(absolutePath);
        console.log(`File berhasil dihapus: ${absolutePath}`);
    } catch (err) {
        console.error(`Error menghapus file: ${err.message}`);
    }
}

// Fungsi utama untuk memeriksa dan memproses sesi
async function checkSession() {
    const dataPath = path.join(__dirname, "..", "..", "config", "data.json");

    // Membaca data dari file data.json
    const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
    const jalurSesi = data.folder_sumber;  // Mengambil jalur sesi dari data
    const namaFile = data.nama_file;        // Mengambil nama file dari data

    let client; // Deklarasi variabel client di luar try-catch

    try {
        // Membaca data sesi dari file
        const sessionData = await fs.promises.readFile(jalurSesi, "utf-8");

        // Membuat instance TelegramClient
        client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
            connectionRetries: 5,
            timeout: 1800000,
            baseLogger: logger2,
        });

        await client.connect();

        // Mendapatkan informasi akun
        const me = await client.getMe();

        // Menyiapkan informasi pengguna
        const phoneNumber = me.phone;
        const name = me.lastName ? `${me.firstName} ${me.lastName}` : me.firstName;

        // Menampilkan informasi sesi
        console.log(`${phoneNumber} | ${name} adalah sesi gramjs_string.\n`);

    } catch (error) {
        console.log("Belum melakukan login")
        // deleteFile(jalurSesi);
        console.log("File dihapus\n")
    } finally {
        // Menutup koneksi client jika ada
        if (client) {
            await client.disconnect();
            await client.destroy();
        }
    }
}

// Menjalankan fungsi utama
checkSession().catch(logger2.error);