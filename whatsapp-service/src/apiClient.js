const axios = require("axios");
const FormData = require("form-data");
const fs = require("fs");

const { API_URL } = require("./config");

const sleep = (ms) =>
    new Promise((resolve) => setTimeout(resolve, ms));

async function callApi(payload, retries = 3) {
    try {
        const form = new FormData();

        form.append("sender", payload.sender);
        form.append("message", payload.message);

        if (payload.attachment) {
            form.append(
                "file",
                fs.createReadStream(payload.attachment.path),
                payload.attachment.filename
            );
        }

        return await axios.post(API_URL, form, {
            headers: form.getHeaders(),
        });

    } catch (err) {
        if (retries > 0) {
            console.log(`🔁 Retry (${4 - retries}/3)...`);

            await sleep(1000);

            return callApi(payload, retries - 1);
        }

        throw err;
    }
}

module.exports = {
    callApi,
};