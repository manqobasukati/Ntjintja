cordova.define('cordova/plugin_list', function(require, exports, module) {
module.exports = [
    {
        "id": "cordova-plugin-call-number.CallNumber",
        "file": "plugins/cordova-plugin-call-number/www/CallNumber.js",
        "pluginId": "cordova-plugin-call-number",
        "clobbers": [
            "call"
        ]
    },
    {
        "id": "com.teamnemitoff.phonedialer.phonedialer",
        "file": "plugins/com.teamnemitoff.phonedialer/www/dialer.js",
        "pluginId": "com.teamnemitoff.phonedialer",
        "merges": [
            "phonedialer"
        ]
    }
];
module.exports.metadata = 
// TOP OF METADATA
{
    "cordova-plugin-whitelist": "1.3.2",
    "cordova-plugin-call-number": "1.0.1",
    "com.teamnemitoff.phonedialer": "0.3.1"
};
// BOTTOM OF METADATA
});