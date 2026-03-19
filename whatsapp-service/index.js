const { default: makeWASocket, useMultiFileAuthState, fetchLatestBaileysVersion } = require("@whiskeysockets/baileys");
const qrcode = require("qrcode-terminal");
const axios = require("axios");

const API_URL = "http://api:8000/whatsapp";

//  retry api
async function callApi(payload, retries = 3) {
  try {
    return await axios.post(API_URL, payload);
  } catch (err) {
    if (retries > 0) {
      console.log("🔁 retry...");
      return callApi(payload, retries - 1);
    }
    throw err;
  }
}

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState("auth_info");
  const { version } = await fetchLatestBaileysVersion();

  const sock = makeWASocket({
    version,
    auth: state
  });

  sock.ev.on("creds.update", saveCreds);

  sock.ev.on("connection.update", (update) => {
    const { connection, qr } = update;

    if (qr) {
      console.log("📱 ESCANEIE O QR:");
      qrcode.generate(qr, { small: true });
    }

    if (connection === "open") {
      console.log("🚀 WhatsApp conectado!");
    }

    if (connection === "close") {
      console.log("❌ conexão fechada, reiniciando...");
      start();
    }
  });

  sock.ev.on("messages.upsert", async ({ messages }) => {
    const msg = messages[0];

    if (!msg.message || msg.key.fromMe) return;

    const sender = msg.key.remoteJid;
    const text =
      msg.message.conversation ||
      msg.message.extendedTextMessage?.text;

    if (!text) return;

    console.log(`📩 ${sender}: ${text}`);

    try {
      const response = await callApi({
        sender: sender,
        message: text
      });

      const data = response.data;

      console.log("📤 API:", data);

      if (data.messages && data.messages.length > 0) {
        for (const m of data.messages) {
          console.log(`📨 Enviando: ${m}`);
          await sock.sendMessage(sender, { text: m });
        }
      } else {
        console.log("⚠️ API sem resposta");
      }

    } catch (err) {
      console.error("❌ erro API:", err.message);
    }
  });
}

start();