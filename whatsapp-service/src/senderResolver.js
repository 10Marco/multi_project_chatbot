function normalizeBrazilianPhone(phone) {

    let number = phone.replace(/\D/g, "");

    if (number.startsWith("55")) {
        number = number.substring(2);
    }

    if (number.length === 10) {
        number =
            number.substring(0, 2) +
            "9" +
            number.substring(2);
    }

    return number;
}


async function resolveSender(sock, msg) {

    const jid =
        msg.key.participant ||
        msg.key.remoteJid;

    if (!jid) {
        return null;
    }

    let resolvedJid = jid;

    if (jid.endsWith("@lid")) {

        if (msg.key.remoteJidAlt) {

            resolvedJid = msg.key.remoteJidAlt;

        } else {

            const pn =
                await sock.signalRepository.lidMapping.getPNForLID(jid);

            if (!pn) {
                return null;
            }

            resolvedJid = pn;
        }
    }

    const phone = resolvedJid
        .split(":")[0]
        .split("@")[0];

    return normalizeBrazilianPhone(phone);
}


module.exports = {
    resolveSender
};