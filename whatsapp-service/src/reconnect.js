let reconnectAttempts = 0;
let reconnectTimer = null;

const BASE_DELAY = 10000;
const MAX_DELAY = 120000;

function resetReconnect() {

    reconnectAttempts = 0;

}

function scheduleReconnect(start) {

    if (reconnectTimer)
        return;

    reconnectAttempts++;

    const delay = Math.min(

        BASE_DELAY * reconnectAttempts,

        MAX_DELAY

    );

    console.log(

        `❌ conexão fechada. Nova tentativa em ${delay / 1000}s`

    );

    reconnectTimer = setTimeout(async () => {

        reconnectTimer = null;

        try {

            await start();

        }

        catch (err) {

            console.error("❌ erro ao reiniciar WhatsApp:", err.message);

            scheduleReconnect(start);

        }

    }, delay);

}

module.exports = {

    scheduleReconnect,

    resetReconnect

}