const winston = require("winston");
const path = require("path");
const { LOG_PATH } = require("./config");

const logger = winston.createLogger({
    level: "info",

    format: winston.format.combine(
        winston.format.timestamp(),
        winston.format.errors({ stack: true }),
        winston.format.json()
    ),

    transports: [
        new winston.transports.File({
            filename: path.join(LOG_PATH, "error.log"),
            level: "error"
        }),

        new winston.transports.File({
            filename: path.join(LOG_PATH, "combined.log")
        }),

        new winston.transports.Console()
    ]
});

module.exports = logger;