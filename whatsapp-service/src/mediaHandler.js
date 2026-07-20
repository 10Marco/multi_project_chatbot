const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { downloadMediaMessage } = require("@whiskeysockets/baileys");

async function downloadAttachment(sock, msg) {

    const document = msg.message.documentMessage;

    const stream = await downloadMediaMessage(
        msg,
        "stream",
        {},
        {
            logger: sock.logger,
            reuploadRequest: sock.updateMediaMessage
        }
    );

    const dir = "/tmp/attachments";

    fs.mkdirSync(dir, { recursive: true });

    const filename = document.fileName;

    const filepath = path.join(
        dir,
        `${crypto.randomUUID()}-${filename}`
    );

    const writeStream = fs.createWriteStream(filepath);

    for await (const chunk of stream) {
        writeStream.write(chunk);
    }

    writeStream.end();

    await new Promise(resolve => writeStream.on("finish", resolve));

    return {
        filename,
        mimetype: document.mimetype,
        size: Number(document.fileLength),
        path: filepath
    };
}

module.exports = {
    downloadAttachment
};