const {
    default: makeWASocket,
    useMultiFileAuthState,
    fetchLatestBaileysVersion,
    DisconnectReason
} = require("@whiskeysockets/baileys");

const qrcode = require("qrcode-terminal");

const { AUTH_PATH } = require("./config");
const logger = require("./logger");

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
    if (starting) return;

    starting = true;

    try {
        const { state, saveCreds } =
            await useMultiFileAuthState(AUTH_PATH);

        logger.info("WhatsApp Service");
        logger.info("AUTH: %s", AUTH_PATH);

        const { version } =
            await fetchLatestBaileysVersion();

        logger.info("Versão WA: %s", version);

        const sock = makeWASocket({
            version,
            auth: state,
            logger: logger.baileysLogger,
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
                logger.info("WhatsApp conectado!");
                return;
            }

            if (connection === "close") {
                logDisconnectReason(update);

                const status = getDisconnectStatusCode(update);

                logger.debug("Status: %s", status);
                logger.debug("DisconnectReason.loggedOut: %s", DisconnectReason.loggedOut);

                if (status === DisconnectReason.loggedOut) {
                    logger.info("Sessão realmente expirada.");
                    return;
                }

                scheduleReconnect(start);
            }
        });

        sock.ev.on("messages.upsert", async ({ messages }) => {
            try {
                await handleMessages(sock, messages);
            } catch (err) {
                logger.error(err);
            }
        });
    } finally {
        starting = false;
    }
}

start().catch((err) => {
    logger.error(err);
    scheduleReconnect(start);
});
