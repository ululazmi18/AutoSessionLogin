const { Api, TelegramClient } = require('telegram');
const { StringSession } = require('telegram/sessions');
const fs = require('fs');
const path = require('path');
const input = require("input");
const readline = require('readline');

const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
const kodePath = path.join(__dirname, "..", "..", "config", "kode.json");
const configPath = path.join(__dirname, "..", "..", "config", "config.json");

const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
const kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));

const folderGramjsString = path.join(__dirname, "..", "..", "sessions", "gramjs_string");

const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
});

// Fungsi untuk menanyakan pertanyaan menggunakan readline
function askQuestion(question) {
    return new Promise(resolve => rl.question(question, resolve));
}

// Fungsi untuk login menggunakan nomor telepon
async function loginDenganNomorTelepon() {
    const nomorTelepon = await askQuestion("Nomor telepon Anda (misalnya, +1234567890): ");
    const sanitizedPhone = nomorTelepon.replace(/\D/g, ''); // Sanitasi nomor telepon
    const sessionFile = path.join(folderGramjsString, `${sanitizedPhone}.session`);

    // Periksa apakah file session sudah ada
    if (fs.existsSync(sessionFile)) {
        console.log(`Sesi untuk nomor telepon ${nomorTelepon} sudah ada di ${sessionFile}`);
        return; // Keluarkan fungsi jika file session sudah ada
    }

    const stringSession = new StringSession('');
    const client = new TelegramClient(stringSession, api_id, api_hash, { 
        connectionRetries: 5, 
        timeout: 1800000, 
        baseLogger: logger2 
    });

    await client.start({
        phoneNumber: async () => nomorTelepon,
        phoneCode: async () => await askQuestion("Kode yang Anda terima: "),
        password: async () => {
            // Gunakan data yang sudah diinisialisasi di awal fungsi
            const userPassword = await input.text("Masukkan password Anda: ");
            data.Password = userPassword; // Perbarui data dengan password
            await fs.promises.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");
            return userPassword;
        },
        onError: (error) => console.error("Error:", error),
    });

    console.log('Login berhasil');

    const sessionString = client.session.save();
    const me = await client.getMe();
    
    const Nomor = me.phone
    const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
    const userPassword = data.Password;
    kode[Nomor] = userPassword;
    await fs.promises.writeFile(kodePath, JSON.stringify(kode, null, 4), "utf-8");

    // Buat folder untuk menyimpan session jika belum ada
    if (!fs.existsSync(folderGramjsString)) {
        fs.mkdirSync(folderGramjsString, { recursive: true });
    }

    // Simpan sesi dalam file
    fs.writeFileSync(sessionFile, sessionString, 'utf8');
    console.log(`Sesi disimpan di ${sessionFile}`);

    await client.disconnect();
    await client.destroy();
}

if (require.main === module) {
    loginDenganNomorTelepon().catch(logger2.error);
}
