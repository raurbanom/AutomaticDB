/**
 * Name: Engineering Utils
 * Author: Richar Urbano <richar.urbano@gmail.com>
 * Comments:
 * -   This class will provide misc helpers to all modules
 * @type {{}}
 */
engineering = (typeof (engineering) !== "undefined") ? engineering : {};
engineering.util = (typeof (engineering.util) !== "undefined") ? engineering.util : {};

/**
 * Checks if a given string is empty
 * @param value
 * @returns {*}
 */
engineering.util.isEmpty = function (value) {
    if (value === 0)
        return false;
    if (value === undefined ||
            value === null ||
            value === "") {
        return true;
    }

    if (typeof (value) === "Array") {
        return value.length === 0;
    }

    if (Object.prototype.toString.apply(value) === "[object Array]") {
        return value.length === 0;
    }

    if (Object.prototype.toString.apply(value) === "[object Object]") {
        return $.isEmptyObject(value);
    }

    return false;
};

/**
 * Validates if the text is a valid opening and closing tags, including classes
 * @param text
 * @returns {*}
 */
engineering.util.validText = function(text) {
    if (text === undefined || text === null) {
        return "";
    }

    if (typeof (text) === "string") {
        return text.replace(/(<([^>]+)>)/ig, "");
    }

    return text;
};

engineering.util.isValidAttribute = function (text) {
    if (!engineering.util.isEmpty(text)) {
        return text.split(",").indexOf("") === -1;
        // return /^\w(\s*,?\s*\w)*$/.test(text);
    }

    return false;
};