
const Alpaca = require("@alpacahq/alpaca-trade-api");
const alpaca = new Alpaca();
// server <==> data source
// communication can go both ways

const WebSocket = require('ws');
const wss = new WebSocket("wss://stream.data.alpaca.markets/v1beta1/news");
const receive_Server = new WebSocket("ws://localhost:8080");
dataToSend = ""
probability = 0
sentiment = "negative"
symbol = ""
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

receive_Server.on('message', async function(data) {
    const dataArray = JSON.parse(data);
    console.log(dataArray[0]); // Output: 0.8288981914520264
    console.log(dataArray[1]); // Output: "negative"
    probability = dataArray[0];
    sentiment = dataArray[1];
    console.log(symbol)
    if (sentiment == "positive" && probability > 0.9) {
        console.log('created order')
        let order = await alpaca.createOrder({
            symbol: symbol,
            qty: 1,
            side: "buy",
            type: "market",
            time_in_force: "day" // if the day ends then it wont trade
        });
    } else if (sentiment == "negative" && probability > 0.9) {
        console.log('selling')
        closedPosition = await alpaca.closePosition(symbol);
    }
});

wss.on('open', function() {
    console.log("Websocket connected");

    const authMsg = {
        action: 'auth',
        key: 'PK28MFMJVX0XVJMY6SS8',
        secret: 'kFAH2z0HhSPVBSw3dOGkfoSiRbhcWLM7DVKReoca'
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
        symbol = currentEvent.symbols[0]
        const headline = currentEvent.headline.toString();
        const summary = currentEvent.summary.toString();
        dataToSend = headline + summary
        console.log('data sent for' + symbol)
        sendMsg();
    }
});

