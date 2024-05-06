const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();
// server <==> data source
// communication can go both ways

const WebSocket = require('ws');
const wss = new WebSocket("wss://stream.data.alpaca.markets/v1beta1/news");
const receive_Server = new WebSocket("ws://localhost:8080");
dataToSend = ""
console.log(receive_Server);

function sendMsg() {
    if (dataToSend != "") {
        receive_Server.send(dataToSend);
    }
};

function loop() {
    setTimeout(() => {
      sendMsg();
      loop();
    }, 5000);
};

receive_Server.on('open', function open() {
    console.log('connect')
    console.log(receive_Server)
    // loop()
});

receive_Server.on('message', function(data) {
    console.log(data);
    console.log(data.toString('utf-8'));
    console.log('received something')
});

wss.on('open', function() {
    console.log("Websocket connected");

    const authMsg = {
        action: 'auth',
        key: 'PK1B3494WJH3KWU0Y64L',
        secret: 'mfvxDBtymMvsAL43L5xTJz75kgEqWSHA2bibwvrB'
    };

    wss.send(JSON.stringify(authMsg)); // send auth data tp ws log us in

    const subMsg = {
        action: 'subscribe',
        news: ['*']
    };

    wss.send(JSON.stringify(subMsg));


});

wss.on('message', async function(message) {
    console.log("Message is" + message);
    // message is string
    const currentEvent = JSON.parse(message)[0];
    if (currentEvent.T === "n") {
        const headline = currentEvent.headline.toString();
        const summary = currentEvent.summary.toString();
        dataToSend = headline + summary
        console.log(headline + summary)
        sendMsg()
        // python_web_socket.send(JSON.stringify({ action: 'invoke_function', headline: headline }));
    }
});

