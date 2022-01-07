// Collapsible
var coll = document.getElementsByClassName("collapsible");
var socket;
connectToSocket();
setOnChatClickListener();
getFirstBotMessage();
setOnEnterPress();


function setOnChatClickListener(){
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
}

function setOnEnterPress(){
  // Press enter to send a message
  $("#textInput").keypress(function (e) {
      if (e.which == 13) {
          getResponse();
      }
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
function getFirstBotMessage() {
    let firstMessage = "How's it going?"
    document.getElementById("botStarterMessage").innerHTML = '<p class="botText"><span>' + firstMessage + '</span></p>';

    let time = getTime();

    $("#chat-timestamp").append(time);
    document.getElementById("userInput").scrollIntoView(false);
}

//Gets the text text from the input box and processes it
function getResponse() {
    // get user input
    let userText = $("#textInput").val();

    // if user did not type anything
    if (userText == "") {
        // request from server a random question from dict_questions in util.py
        socket.emit('request_question_event');
    }

    socket.on('response_question_event', function(msg){
       // console.log('User received:', msg);
       userText=msg
       console.log(userText)
    });

    // send user text to server
    socket.emit('UserSendsMessage', userText);

    // init response text
    responseText = ""

    // wait for response
    socket.on('response_event', function(msg){
       console.log('User received:', msg);
       responseText=msg
    });

    setTimeout(() => {
      // console.log("Response is: "+responseText+".")

      // generate user text HTML
      let userHtml = '<p class="userText"><span>' + userText + '</span></p>';

      // delete input field
      $("#textInput").val("");

      // represent users
      $("#chatbox").append(userHtml);
      document.getElementById("chat-bar-bottom").scrollIntoView(true);

      // console.log("Response is: "+responseText+".")
      // represent response
      let botHtml = '<p class="botText"><span>' + responseText + '</span></p>';
      $("#chatbox").append(botHtml);
      document.getElementById("chat-bar-bottom").scrollIntoView(true);

    }, 500)

    return responseText;
}

function sendButton() {
  // on click send button
  getResponse();
}
