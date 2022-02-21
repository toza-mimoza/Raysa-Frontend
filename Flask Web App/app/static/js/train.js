var socket;
var resultStartTime;
var resultEndTime;

function connectToSocket(){
  socket = io.connect('http://' + document.domain + ':' + location.port);
  socket.on('connect', function() {
      socket.send('Connected to socket for training!');
  });
  // console.log("Connected to the socket.")
  return socket;
}

function getStartTime(){
  socket.emit("req_start_time");
  socket.on("res_start_time", function(start_time){
    console.log("Getting start time..."+start_time);
    resultStartTime = start_time;
  });
}

function getEndTime(){
  // get end time

  socket.emit("req_end_time");
  socket.on("res_end_time", function(end_time){
    console.log("Getting end time..."+end_time);
    resultEndTime = end_time;
  });
}
function run_training_update(){
  console.log("Starting time updater...");
  // connect to the socket to receive time updates
  connectToSocket();

  // get start time
  getStartTime();

  getEndTime();
  // update html timer for start time
  setTimeout(() => {
    let startTimeHtml = '<p><span> Start time:' + resultStartTime + '</span></p>';
    $("#startTime").append(startTimeHtml);

    let endTimeHtml = '<p><span> End time:' + resultEndTime + '</span></p>';
    $("#endTime").append(endTimeHtml);
  }, 200)
}
