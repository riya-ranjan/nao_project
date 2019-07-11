function createWebSocket(webSocketConfig, startRecordButton, stopRecordButton) {
    let webSocket = new WebSocket(`ws://${webSocketConfig.host}:${webSocketConfig.port}`);

    webSocket.onopen = function (event) {
        // Web Socket is connected
        console.log("Socket successfully created");

        webSocket.send(JSON.stringify({
            type: "systemQuery",
            content: "recordStatus"
        }));
    };

    webSocket.onmessage = function (event) {
        let receivedMsg = JSON.parse(event.data);
        console.log(`Receive message:`);
        console.log(receivedMsg);

        if (receivedMsg["type"].trim() === "systemResponse") {
            if (receivedMsg["response"].trim() === "recordStatus") {
                console.log(`recordStatus response: ${receivedMsg["content"]}`);

                startRecordButton.disabled = receivedMsg["content"];
                stopRecordButton.disabled = !receivedMsg["content"];
                isRecording = receivedMsg["content"];
            }
        }
    };


    webSocket.onclose = function (event) {
        // websocket is closed.
        console.log("Connection is closed...");
        console.log(event.code);
    };

    return webSocket;
}