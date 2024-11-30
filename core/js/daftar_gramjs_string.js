const { TelegramClient } = require("telegram");
const { StringSession } = require("telegram/sessions");
const path = require("path");
const fs = require("fs");
const input = require("input");

const logger2 = require(path.join(__dirname, "..", "..", "helpers", "TldLogger"));

const folderGramjsString = path.join(__dirname, "..", "..", "sessions", "gramjs_string");
const configPath = path.join(__dirname, "..", "..", "config", "config.json");
const dataPath = path.join(__dirname, "..", "..", "config", "data.json");
const kodePath = path.join(__dirname, "..", "..", "config", "kode.json");

// Membaca konfigurasi
const { api_id, api_hash } = JSON.parse(fs.readFileSync(configPath, "utf-8"));
const kode = JSON.parse(fs.readFileSync(kodePath, "utf-8"));
const data = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
const jalurUji = data.folder_uji;
const Nomor = data.Nomor;

async function getSessionData() {
    try {
        return await fs.promises.readFile(jalurUji, "utf-8");
    } catch (err) {
        console.error(`Gagal membaca sesi: ${err.message}`);
        process.exit(1);
    }
}

async function main() {
    const sessionData = await getSessionData();

    const client = new TelegramClient(new StringSession(sessionData), api_id, api_hash, {
        connectionRetries: 5,
        timeout: 1800000,
        baseLogger: logger2,
    });

    try {
        await client.start({
            phoneNumber: async () => await input.text("Masukkan nomor Anda: "),
            phoneCode: async () => {
                console.log("Menjalankan skrip Python untuk mendapatkan kode...");
                const { spawn } = require("child_process");
                const pythonScriptPath = path.join(__dirname, "..", "core", "kode_pyrogram.py");

                await new Promise((resolve, reject) => {
                    const process = spawn("python", [pythonScriptPath]);

                    process.stdout.on("data", (data) => console.log(`Python: ${data.toString()}`));
                    process.stderr.on("data", (data) => console.error(`Error Python: ${data.toString()}`));

                    process.on("close", (code) => {
                        code === 0 ? resolve() : reject(new Error(`Skrip Python gagal: kode keluar ${code}`));
                    });
                });

                const updatedData = JSON.parse(fs.readFileSync(dataPath, "utf-8"));
                if (updatedData.kode) {
                    console.log(`Kode ditemukan: ${updatedData.kode}`);
                    return updatedData.kode;
                } else {
                    throw new Error("Kode tidak ditemukan di data.json!");
                }
            },
            password: async () => {
                while (true) {
                    const userPassword = await input.text("Masukkan password Anda: ");
                    try {
                        await client.checkPassword(userPassword);
                        console.log("Login berhasil dengan password.");

                        kode[Nomor] = userPassword;
                        await fs.promises.writeFile(kodePath, JSON.stringify(kode, null, 4), "utf-8");
                        return userPassword;
                    } catch (error) {
                        if (error.message.includes("PASSWORD_HASH_INVALID")) {
                            console.log("Password salah. Silakan coba lagi.");
                        } else {
                            console.error(`Kesalahan tidak terduga saat login dengan password: ${error.message}`);
                            throw error;
                        }
                    }
                }
            },
            onError: (err) => console.error(`Error: ${err.message}`),
        });

        const me = await client.getMe();
        const sessionFile = path.join(folderGramjsString, `${me.phone}.session`);
        const sessionString = client.session.save();

        await fs.promises.writeFile(sessionFile, sessionString, "utf8");
        console.log(`Sesi berhasil disimpan untuk pengguna: ${me.phone}`);
    } catch (err) {
        console.error(`Terjadi kesalahan di daftar_gramjs_string: ${err.message}`);
    } finally {
        try {
            await client.disconnect();
            await client.destroy();
            console.log("Koneksi TelegramClient telah ditutup.");
        } catch (err) {
            console.error(`Kesalahan saat menutup koneksi: ${err.message}`);
        }
    }
}

main().catch(logger2.error);