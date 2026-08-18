const path = require("path");
const SIFOP_URL = process.env.SIFOP_URL;
const SIFOP_TOKEN = process.env.SIFOP_TOKEN;

module.exports = {

    AUTH_PATH: path.join(__dirname, "../runtime/auth"),

    API_URL: process.env.API_URL || "http://api:8000/whatsapp",

    // Integração com SIFOP
    SIFOP_URL: SIFOP_URL,
    SIFOP_TOKEN: SIFOP_TOKEN

}
