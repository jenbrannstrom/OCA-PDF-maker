/**
@file
Minimal JS file for absulutely vital stuff that we need immediately (even for language-based redirect).
*/

/**
A complete cookies reader/writer framework with full unicode support.
@from https://developer.mozilla.org/en-US/docs/Web/API/document.cookie
@info https://developer.mozilla.org/en-US/docs/DOM/document.cookie

This framework is released under the GNU Public License, version 3 or later.
http://www.gnu.org/licenses/gpl-3.0-standalone.html
*/
var cookieController = {
    get: function (sKey) {
        return decodeURIComponent(document.cookie.replace(new RegExp("(?:(?:^|.*;)\\s*" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=\\s*([^;]*).*$)|^.*$"), "$1")) || null;
    },
    set: function (sKey, sValue, vEnd, sPath, sDomain, bSecure) {
        if (!sKey || /^(?:expires|max\-age|path|domain|secure)$/i.test(sKey)) { return false; }
        var sExpires = "";
        if (vEnd) {
            switch (vEnd.constructor) {
                case Number:
                    sExpires = vEnd === Infinity ? "; expires=Fri, 31 Dec 9999 23:59:59 GMT" : "; max-age=" + vEnd;
                    break;
                case String:
                    sExpires = "; expires=" + vEnd;
                    break;
                case Date:
                    sExpires = "; expires=" + vEnd.toUTCString();
                    break;
            }
        }
        document.cookie = encodeURIComponent(sKey) + "=" + encodeURIComponent(sValue) + sExpires + (sDomain ? "; domain=" + sDomain : "") + (sPath ? "; path=" + sPath : "") + (bSecure ? "; secure" : "");
        return true;
    },
    remove: function (sKey, sPath, sDomain) {
        if (!sKey || !this.has(sKey)) { return false; }
        document.cookie = encodeURIComponent(sKey) + "=; expires=Thu, 01 Jan 1970 00:00:00 GMT" + ( sDomain ? "; domain=" + sDomain : "") + ( sPath ? "; path=" + sPath : "");
        return true;
    },
    has: function (sKey) {
        return (new RegExp("(?:^|;\\s*)" + encodeURIComponent(sKey).replace(/[\-\.\+\*]/g, "\\$&") + "\\s*\\=")).test(document.cookie);
    }
};

var cookieMonster = cookieController;

/**
Log-level-based JS logger with polyfill (for no "console), ala log4j.
*/
var Logger = function(opts) {
    // mix in the opts
    if (opts) for (var key in opts) this[key] = opts[key];
}

Logger.prototype = (function() {

    var me = {};

    me.level = 'error';

    // polyfill
    me.console = window.console || {
        debug: function() {},
        log: function() {},
        warn: function() {},
        error: function() {},
        assert: function() {},
    };

    me.debug = function() {
        if (!window.globalIsIE && this.level == 'debug' && window.console) this.console.debug.apply(this.console, arguments);
    };

    me.log = function() {
        if (!window.globalIsIE && this.level != 'warn' && this.level != 'error' && this.level != 'fatal' && window.console) this.console.log.apply(this.console, arguments);
    };

    me.warn = function() {
        if (!window.globalIsIE && this.level != 'error' && this.level != 'fatal' && window.console) this.console.warn.apply(this.console, arguments);
    };

    me.error = function() {
        if (!window.globalIsIE && this.level != 'fatal' && window.console) this.console.error.apply(this.console, arguments);
    };

    return me;

})();

logger = new Logger({level: _gcui_loglevel});