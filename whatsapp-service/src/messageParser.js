const logger = require("./logger");

function parseMessage(msg) {
    logger.debug("RAW BAILEYS");
    logger.debug(msg);

    const sender =
        msg.key.participant ||
        msg.key.remoteJid;


    logger.debug("SENDER: %s", sender);

    logger.debug(
        "REMOTE JID: %s",
        msg.key.remoteJid
    );

    logger.debug(
        "PARTICIPANT: %s",
        msg.key.participant
    );
    

    const text =
        msg.message.conversation ||
        msg.message.extendedTextMessage?.text ||
        "";

    const type =
        Object.keys(msg.message)[0];

    return {
        sender,
        text,
        type,
        message: msg.message,
        key: msg.key,
        hasMedia: [
            "imageMessage",
            "videoMessage",
            "documentMessage",
            "audioMessage"
        ].includes(type)
    };
}

module.exports = {
    parseMessage
};
