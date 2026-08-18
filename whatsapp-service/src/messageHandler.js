const { callApi } = require("./apiClient");
const { parseMessage } = require("./messageParser");
const { sendMessage } = require("./sender");
const { downloadAttachment } = require("./mediaHandler");
const { resolveSender } = require("./senderResolver");
const logger = require("./logger");
const SifopClient = require("./SifopClient");

async function handleMessages(sock, messages) {

    const msg = messages[0];

    if (!msg) return;
    if (!msg.message) return;
    if (msg.messageStubType) return;
    if (msg.key.remoteJid?.endsWith("@g.us")) return;
    if (msg.key.fromMe) return;
    if (msg.key.remoteJid === "status@broadcast") return;

    const parsed = parseMessage(msg);

    try {

        const sender = await resolveSender(sock, msg);

        logger.debug(
            "LID/JID original: %s",
            parsed.sender
        );

        logger.debug(
            "Sender resolvido: %s",
            sender
        );

        if (!sender) {

            logger.warn(
                "Não foi possível resolver o sender: %s",
                parsed.sender
            );

            return;
        }

        logger.debug(
            "Mensagem recebida de %s: %s",
            sender,
            parsed.text
        );

        let attachment = null;

        if (parsed.hasMedia) {
            attachment = await downloadAttachment(
                sock,
                msg
            );
        }

        const response = await callApi({
            sender: sender,
            message: parsed.text,
            attachment
        });

        const { data } = response;

        if (data.messages?.length) {

            for (const message of data.messages) {

                if (message.type === "sifop_folha") {

                    logger.info(
                        "Gerando folha SIFOP: tipo=%s id=%s mes=%s",
                        message.tipo,
                        message.id,
                        message.mes
                    );

                    const pdf = await SifopClient.gerarFolha(
                        message.tipo,
                        message.id,
                        message.mes
                    );

                    await sendMessage(
                        sock,
                        parsed.sender,
                        {
                            type: "document",
                            document: pdf,
                            filename: message.filename
                        }
                    );

                    logger.info(
                        "Folha SIFOP enviada: %s",
                        message.filename
                    );

                    continue;
                }

                await sendMessage(
                    sock,
                    parsed.sender,
                    message
                );
            }
        }
    }
    catch (error) {

        logger.error(
            "Erro ao processar a mensagem de %s: %s",
            parsed.sender,
            error.message
        );
    }
}

module.exports = {
    handleMessages
};