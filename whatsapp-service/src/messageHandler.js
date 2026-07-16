const { callApi } = require("./apiClient");
const { parseMessage } = require("./messageParser");
const { sendMessage } = require("./sender");

async function handleMessages(sock, messages) {

    const msg = messages[0];

    if (!msg) return;
    if (!msg.message) return;
    if (msg.messageStubType) return;
    if (msg.key.remoteJid?.endsWith("@g.us")) return;
    if (msg.key.fromMe) return;
    if (msg.key.remoteJid === "status@broadcast") return;

    const parsed = parseMessage(msg);

    console.log("\n==============================");
    console.log(`📩 ${parsed.sender}`);
    console.log(`💬 ${parsed.text}`);
    console.log("==============================");

    try {
        const response = await callApi({

            sender: parsed.sender,
            message: parsed.text,
            media: parsed.hasMedia,
            mediaType: parsed.type

        });

        const { data } = response;
        console.log("⬅️ API RESPONSE");

        console.dir(data, { depth: null });

        if (data.messages?.length) {

            for (const message of data.messages) {

                await sendMessage(
                    sock,
                    parsed.sender,
                    message
                );

            }

        }

    } catch (err) {

        console.error(err.response?.data || err.message);

    }

}

module.exports = {

    handleMessages

};