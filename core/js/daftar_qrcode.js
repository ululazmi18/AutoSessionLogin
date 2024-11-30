const { Api, TelegramClient } = require('telegram');
const { StringSession } = require('telegram/sessions');
const fs = require('fs');
const path = require('path');
const input = require("input");
const readline = require('readline');
const qrcode = require('qrcode-terminal');

const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
const kodePath = path.join(__dirname, "..", "..", "config", "kode.json");
const configPath = path.join(__dirname, "..", "..", "config", "config.json");

const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
const kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));

const folderGramjsString = path.join(__dirname, "..", "..", "sessions", "gramjs_string");

// Fungsi untuk menanyakan pertanyaan menggunakan readline
function askQuestion(question) {
    return new Promise(resolve => rl.question(question, resolve));
}

// Fungsi untuk login menggunakan QR Code
async function loginDenganQRCode() {
    const stringSession = new StringSession('');
    const client = new TelegramClient(stringSession, api_id, api_hash, { 
        connectionRetries: 5, 
        timeout: 1800000, 
        baseLogger: logger2
    });

    // Pastikan data dibaca di awal fungsi, sehingga bisa digunakan di seluruh fungsi
    const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
    const kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));

    while (true) {
        try {
            await client.connect();

            let isShown = false;
            await client.signInUserWithQrCode({
                apiId: api_id,
                apiHash: api_hash,
            }, {
                qrCode: async (code) => {
                    if (!isShown) {
                        console.log("\nScan QR code below with your Telegram app to login:\n");
                        qrcode.generate(`tg://login?token=${code.token.toString("base64url")}`, { small: true }, (qrcodeString) => {
                            console.log(qrcodeString);
                        });
                        isShown = true;
                    } else {
                        readline.moveCursor(process.stdout, 0, -6);
                        readline.clearScreenDown(process.stdout);
                        console.log("\nNew QR code received\n");
                        qrcode.generate(`tg://login?token=${code.token.toString("base64url")}`, { small: true }, (qrcodeString) => {
                            console.log(qrcodeString);
                        });
                    }
                },
                password: async () => {
                    // Gunakan data yang sudah diinisialisasi di awal fungsi
                    const userPassword = await input.text("Masukkan password Anda: ");
                    data.Password = userPassword; // Perbarui data dengan password
                    await fs.promises.writeFile(dataPath, JSON.stringify(data, null, 4), "utf-8");
                    return userPassword;
                },
                onError: (error) => {
                    console.error("Error saat login dengan QR code:", error);
                    if (error.code === 400 && error.errorMessage === 'AUTH_TOKEN_EXPIRED') {
                        console.log("Token kedaluwarsa. Coba lagi untuk mendapatkan QR code baru.");
                    }
                },
            });

            console.log('Login berhasil');
            const sessionString = client.session.save();
            const me = await client.getMe();
            const sanitizedPhone = me.phone || me.username;
            const sessionFile = path.join(folderGramjsString, `${sanitizedPhone}.session`);

            const Nomor = me.phone;
            // Data dan kode sudah diinisialisasi sebelumnya, jadi tidak perlu dibaca ulang
            kode[Nomor] = data.Password;
            await fs.promises.writeFile(kodePath, JSON.stringify(kode, null, 4), "utf-8");

            // Periksa apakah file session sudah ada
            if (fs.existsSync(sessionFile)) {
                console.log(`Sesi untuk ${sanitizedPhone} sudah ada di ${sessionFile}`);
                break; // Keluar jika session sudah ada
            }

            // Jika file session belum ada, simpan sesi
            if (!fs.existsSync(folderGramjsString)) {
                fs.mkdirSync(folderGramjsString, { recursive: true });
            }

            fs.writeFileSync(sessionFile, sessionString, 'utf8');
            break;
        } catch (error) {
            console.error("Error saat login dengan QR code:", error);
            console.log("Mencoba lagi untuk mendapatkan QR code baru...");
        }
    }

    await client.disconnect();
    await client.destroy();
}

if (require.main === module) {
    loginDenganQRCode().catch(logger2.error);
}
