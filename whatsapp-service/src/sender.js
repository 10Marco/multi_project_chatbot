const fs = require("fs");

async function sendText(sock, to, text) {

    await sock.sendMessage(to, {

        text

    });

}

async function sendImage(sock, to, imagePath, caption = "") {

    await sock.sendMessage(to, {

        image: fs.readFileSync(imagePath),

        caption

    });

}

async function sendDocument(sock, to, documentPath, filename) {

    await sock.sendMessage(to, {

        document: fs.readFileSync(documentPath),

        fileName: filename

    });

}

async function sendMessage(sock, to, payload) {

    switch (payload.type) {

        case "text":

            return sendText(

                sock,

                to,

                payload.content

            );

        case "image":

            return sendImage(

                sock,

                to,

                payload.path,

                payload.caption

            );

        case "document":

            return sendDocument(

                sock,

                to,

                payload.path,

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