"use strict";

class Logger {
    constructor() {
        this.levels = ["none", "error", "warn", "info", "debug"];
        this._logLevel = "none"; // Default log level

        // ANSI colors for styling logs
        this.colors = {
            RESET: "\u001b[0m",
            BLUE: "\u001b[34m",
            RED: "\u001b[31m",
            GREEN: "\u001b[32m",
            YELLOW: "\u001b[33m",
            LAVENDER: "\u001b[38;5;147m",
        };

        // Bind methods to maintain the correct `this` context
        this.error = this.error.bind(this);
        this.warn = this.warn.bind(this);
        this.info = this.info.bind(this);
        this.debug = this.debug.bind(this);
        this.success = this.success.bind(this);
        this._log = this._log.bind(this);
        this.paragraph = this.paragraph.bind(this);
    }

    // Determines if a log should be sent based on the current log level
    canSend(level) {
        return this.levels.indexOf(this._logLevel) >= this.levels.indexOf(level);
    }

    // Internal method to process and log messages
    _log(level, message) {
        if (!this.canSend(level)) return;

        const color = this._getColor(level);
        console.log(`${color}${level.toUpperCase()} | ${message}${this.colors.RESET}`);
    }

    // Helper to get color based on log level
    _getColor(level) {
        switch (level) {
            case "error": return this.colors.RED;
            case "warn": return this.colors.YELLOW;
            case "info": return this.colors.BLUE;
            case "debug": return this.colors.LAVENDER;
            default: return this.colors.RESET;
        }
    }

    // Public logging methods
    error(message) {
        this._log("error", message); // Ensure this._log exists
    }

    warn(message) {
        this._log("warn", message);
    }

    info(message) {
        this._log("info", message);
    }

    debug(message) {
        this._log("debug", message);
    }

    success(message) {
        this._log("info", `SUCCESS: ${message}`);
    }

    // Set or get log level
    set logLevel(level) {
        if (this.levels.includes(level)) {
            this._logLevel = level;
        } else {
            console.warn(`Invalid log level: ${level}`);
        }
    }

    get logLevel() {
        return this._logLevel;
    }

    // Utility to format multi-line messages with rounded borders
    paragraph(message) {
        const lines = message.split("\n");
        const maxLength = Math.max(...lines.map(line => line.length));
        const border = "─".repeat(maxLength + 2);

        console.log(`${this.colors.BLUE}╭${border}╮${this.colors.RESET}`);
        lines.forEach(line => {
            console.log(`${this.colors.BLUE}│ ${line.padEnd(maxLength)} │${this.colors.RESET}`);
        });
        console.log(`${this.colors.BLUE}╰${border}╯${this.colors.RESET}`);
    }
}

// Export singleton logger instance
const logger = new Logger();
module.exports = logger;
