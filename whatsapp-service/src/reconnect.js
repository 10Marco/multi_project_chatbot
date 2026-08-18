const logger = require("./logger");

let reconnectAttempts = 0;
let reconnectTimer = null;

const BASE_DELAY = 10000;
const MAX_DELAY = 120000;

function resetReconnect() {
    reconnectAttempts = 0;
}

function scheduleReconnect(start) {
    if (reconnectTimer) return;

    reconnectAttempts++;

    const delay = Math.min(
        BASE_DELAY * reconnectAttempts,
        MAX_DELAY
    );

    logger.info("conexão fechada. Nova tentativa em %ss", delay / 1000);

    reconnectTimer = setTimeout(async () => {
        reconnectTimer = null;

        try {
            await start();
        } catch (err) {
            logger.error("erro ao reiniciar WhatsApp: %s", err.message);
            scheduleReconnect(start);
        }
    }, delay);
}

module.exports = {
    scheduleReconnect,
    resetReconnect
};
