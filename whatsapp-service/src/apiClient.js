const axios = require("axios");

const { API_URL } = require("./config");

const sleep = (ms) =>
    new Promise(resolve => setTimeout(resolve, ms));

async function callApi(payload, retries = 3) {

    try {

        return await axios.post(API_URL, payload);

    } catch (err) {

        if (retries > 0) {

            console.log("🔁 retry...");

            await sleep(1000);

            return callApi(payload, retries - 1);

        }

        throw err;

    }

}

module.exports = {

    callApi

};