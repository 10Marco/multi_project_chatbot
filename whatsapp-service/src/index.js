const {
    default: makeWASocket,
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    DisconnectReason
} = require("@whiskeysockets/baileys");

const qrcode = require("qrcode-terminal");

const { AUTH_PATH } = require("./config");

const {
    scheduleReconnect,
    resetReconnect
} = require("./reconnect");

const {
    handleMessages
} = require("./messageHandler");

const {
    getDisconnectStatusCode,
    logDisconnectReason
} = require("./connection");

let starting = false;

async function start() {

    if (starting)
        return;

    starting = true;

    try {

        const { state, saveCreds } =
            await useMultiFileAuthState(AUTH_PATH);
            console.log("=================================");
            console.log("WhatsApp Service");
            console.log("AUTH:", AUTH_PATH);
            console.log("=================================");

        const { version } =
            await fetchLatestBaileysVersion();
        console.log("Versão WA:", version);    

        const sock = makeWASocket({

            version,

            auth: state,

            printQRInTerminal: false,

            syncFullHistory: false,

            markOnlineOnConnect: false

        });

        sock.ev.on("creds.update", saveCreds);

        sock.ev.on("connection.update", (update) => {

            const { connection, qr } = update;

            if (qr) {

                console.log("📱 ESCANEIE O QR:");
                qrcode.generate(qr, { small: true });

            }

            if (connection === "open") {

                resetReconnect();

                console.log("🚀 WhatsApp conectado!");

                return;

            }

            if (connection === "close") {

                logDisconnectReason(update);

                const status = getDisconnectStatusCode(update);

                console.log("Status:", status);
                console.log("DisconnectReason.loggedOut:", DisconnectReason.loggedOut);

                if (status === DisconnectReason.loggedOut) {

                    console.log("🔐 Sessão realmente expirada.");

                    return;

                }

                scheduleReconnect(start);

            }

        });

        sock.ev.on("messages.upsert", async ({ messages }) => {

            try {

                await handleMessages(sock, messages);

            } catch (err) {

                console.error(err);

            }

        });

    }

    finally {

        starting = false;

    }

}

start().catch((err) => {

    console.error(err);

    scheduleReconnect(start);

});