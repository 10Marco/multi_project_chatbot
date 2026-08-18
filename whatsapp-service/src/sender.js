const fs = require("fs");
const logger = require("./logger");

async function sendText(sock, to, text) {
    return sock.sendMessage(to, {
        text
    });
}

async function sendImage(sock, to, imagePath, caption = "") {
    return sock.sendMessage(to, {
        image: fs.readFileSync(imagePath),
        caption
    });
}

async function sendDocument(sock, to, document, filename) {

    const data = Buffer.isBuffer(document)
        ? document
        : fs.readFileSync(document);

    return sock.sendMessage(to, {
        document: data,
        fileName: filename,
        mimetype: "application/pdf"
    });
}

async function sendMessage(sock, to, payload) {
    logger.debug("SEND");
    logger.debug(payload);

    switch (payload.type) {
        case "text":
            return sendText(
                sock,
                to,
                payload.text
            );

        case "image":
            return sendImage(
                sock,
                to,
                payload.image,
                payload.caption
            );

        case "document":
            return sendDocument(
                sock,
                to,
                payload.document,
                payload.filename
            );

        default:
            throw new Error(
                `Tipo de mensagem não suportado: ${payload.type}`
            );
    }
}

module.exports = {
    sendMessage,
    sendText,
    sendImage,
    sendDocument
};
