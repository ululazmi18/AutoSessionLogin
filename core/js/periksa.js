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

// Fungsi utama untuk memeriksa dan memproses sesi
async function checkSession() {
    const kodePath = path.join(__dirname, "..", "..", "config", "kode.json");
    const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
    const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));

    const jalurSumber = data.folder_sumber;
    const jalurUji = data.folder_uji;
    const namaFile = data.nama_file;

    try {
        // Membaca data sesi dari file
        const sessionData = await fs.promises.readFile(jalurUji, "utf-8");

        // Membuat instance TelegramClient
        const client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
            connectionRetries: 5,
            timeout: 1800000,
            baseLogger: logger2,
        });

        // Memulai client dengan argumen yang valid
        await client.start({
            phoneNumber: async () => {
                throw new Error("Nomor telepon diperlukan untuk otentikasi ulang.");
            },
            phoneCode: async () => {
                throw new Error("Kode otentikasi diperlukan untuk otentikasi ulang.");
            },
            password: async () => {
                throw new Error("Kata sandi diperlukan untuk otentikasi ulang.");
            },
            onError: (err) => console.error(`Kesalahan saat memulai klien: ${err.message}`),
        });

        // Mendapatkan informasi akun
        const me = await client.getMe();
        let kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));

        if (!kode[me.phone]) {
            kode[me.phone] = "";
            fs.writeFileSync(kodePath, JSON.stringify(kode, null, 4), "utf-8");
        }

        const phoneNumber = me.phone;
        const name = me.lastName ? `${me.firstName} ${me.lastName}` : me.firstName;
        console.log(`${namaFile} dengan ${phoneNumber} | ${name} adalah session gramjs_string.`);

        // Menutup koneksi client
        await client.disconnect();
        await client.destroy();

        // Memindahkan file ke folder tujuan
        const folderTujuan = path.join(folderGramjsString, namaFile);
        fs.renameSync(jalurSumber, folderTujuan);
    } catch (error) {
        console.error(`Error gramjs_string: ${error.message}`);
        try {
            // Menghapus file jika bukan sesi Telegram
            await fs.promises.unlink(jalurSumber);
            console.log(`${namaFile} dihapus karena bukan session Telegram`);
        } catch (err) {
            console.error(`Gagal menghapus file: ${err.message}`);
        }
    }
}

// Menjalankan fungsi utama
checkSession().catch(logger2.error);
