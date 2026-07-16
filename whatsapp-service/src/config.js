const path = require("path");

module.exports = {

    AUTH_PATH: path.join(__dirname, "../runtime/auth"),

    CACHE_PATH: path.join(__dirname, "../runtime/cache"),

    LOG_PATH: path.join(__dirname, "../runtime/logs"),

    CONVERSATION_PATH: path.join(__dirname, "../runtime/conversations"),

    API_URL: process.env.API_URL || "http://api:8000/whatsapp" 

}