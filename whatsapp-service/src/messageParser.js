function parseMessage(msg) {

    console.log("========= RAW BAILEYS =========");
    console.dir(msg, { depth: null });
    console.log("===============================");

    const sender =
        msg.key.participant ||
        msg.key.remoteJid;

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

        hasMedia:
            [
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