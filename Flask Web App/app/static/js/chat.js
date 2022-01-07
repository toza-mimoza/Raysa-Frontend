// Collapsible
var coll = document.getElementsByClassName("collapsible");
// var namespace = '';
var socket;
connectToSocket();

for (let i = 0; i < coll.length; i++) {
    coll[i].addEventListener("click", function () {
        this.classList.toggle("active");

        var content = this.nextElementSibling;

        if (content.style.maxHeight) {
            content.style.maxHeight = null;
        } else {
            content.style.maxHeight = content.scrollHeight + "px";
        }
        // change title of conversation window
        $("#chat-button").html('Raysa Chatbot Cluster');
        // set focus on the text input field
        $("#textInput").focus();

    });
}
function connectToSocket(){
  socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function() {
      socket.send('User has connected!');
  });
  // console.log("Connected to the socket.")
}
function getTime() {
    let today = new Date();
    hours = today.getHours();
    minutes = today.getMinutes();

    if (hours < 10) {
        hours = "0" + hours;
    }

    if (minutes < 10) {
        minutes = "0" + minutes;
    }

    let time = hours + ":" + minutes;
    return time;
}

// Gets the first message
function firstBotMessage() {
    let firstMessage = "How's it going?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

firstBotMessage();

// Retrieves the response
// function getHardResponse(userText) {
//     let botResponse = getBotResponse(userText);
//     let botHtml = '<p class="botText"><span>' + botResponse + '</span></p>';
//     $("#chatbox").append(botHtml);
//
//     document.getElementById("chat-bar-bottom").scrollIntoView(true);
// }

//Gets the text text from the input box and processes it
function getResponse() {
    let userText = $("#textInput").val();

    if (userText == "") {
        userText = "I don't know what to ask you...";
    }

    socket.emit('UserSendsMessage', userText);

    responseText = ""
    socket.on('response_event', function(msg){
       console.log('Message received:', msg);
       responseText=msg
    });

    let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    setTimeout(() => {
      console.log("Response is: "+responseText+".")
      let botHtml = '<p class="botText"><span>' + responseText + '</span></p>';
      $("#chatbox").append(botHtml);
      document.getElementById("chat-bar-bottom").scrollIntoView(true);
      return responseText;
    }, 500)

}

// Handles sending text via button clicks
function buttonSendText(sampleText) {
    let userHtml = '<p class="userText"><span>' + sampleText + '</span></p>';

    $("#textInput").val("");
    $("#chatbox").append(userHtml);
    document.getElementById("chat-bar-bottom").scrollIntoView(true);

    //Uncomment this if you want the bot to respond to this buttonSendText event
    // setTimeout(() => {
    //     getHardResponse(sampleText);
    // }, 1000)
}

function sendButton() {
    getResponse();
}


// Press enter to send a message
$("#textInput").keypress(function (e) {
    if (e.which == 13) {
        getResponse();
    }
});
