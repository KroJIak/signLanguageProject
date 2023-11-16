document.addEventListener('deviceready', onDeviceReady, false);

function onDeviceReady() {
    // Cordova is now initialized. Have fun!
    url = 'https://krojiak.surge.sh/'
    showurl(url)
    console.log('Running cordova-' + cordova.platformId + '@' + cordova.version);
    document.getElementById('deviceready').classList.add('ready');
}

function showurl(url){
    var ref = cordova.InAppBrowser.open(url, '_self', 'location=no,zoom=no,hardwareback=none')
    return;
}