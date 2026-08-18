const logger = require("./logger");

function getDisconnectStatusCode(update) {
    const error = update.lastDisconnect?.error;

    return error?.output?.statusCode;
}

function logDisconnectReason(update) {
    const error = update.lastDisconnect?.error;

    const statusCode = getDisconnectStatusCode(update);

    logger.info(
        "conexão fechada: %s",
        error?.message || "motivo não informado"
    );

    if (statusCode) {
        logger.info("status %s", statusCode);
    }
}

module.exports = {
    getDisconnectStatusCode,
    logDisconnectReason
};
