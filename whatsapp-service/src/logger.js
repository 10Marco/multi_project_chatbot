const DEBUG = String(process.env.DEBUG || "false").toLowerCase() === "true";

function log(method, args) {
    if (!DEBUG) return;
    console[method](...args);
}

const baileysLogger = {
    level: DEBUG ? "debug" : "silent",
    child: () => baileysLogger,
    trace: (...args) => log("log", args),
    debug: (...args) => log("log", args),
    info: (...args) => log("log", args),
    warn: (...args) => log("warn", args),
    error: (...args) => log("error", args),
    fatal: (...args) => log("error", args)
};

module.exports = {
    debug: (...args) => log("log", args),
    info: (...args) => log("log", args),
    warn: (...args) => log("warn", args),
    error: (...args) => log("error", args),
    isDebug: () => DEBUG,
    baileysLogger
};
