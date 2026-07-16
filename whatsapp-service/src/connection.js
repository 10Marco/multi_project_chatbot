function getDisconnectStatusCode(update) {

    const error = update.lastDisconnect?.error;

    return error?.output?.statusCode;

}

function logDisconnectReason(update) {

    const error = update.lastDisconnect?.error;

    const statusCode = getDisconnectStatusCode(update);

    console.log(

        `❌ conexão fechada: ${error?.message || "motivo não informado"}`

    );

    if (statusCode)

        console.log(`ℹ️ status ${statusCode}`);

}

module.exports = {

    getDisconnectStatusCode,

    logDisconnectReason

};