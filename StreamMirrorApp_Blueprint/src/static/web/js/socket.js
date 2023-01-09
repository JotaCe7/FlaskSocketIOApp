let socket = NaN
let socketID = NaN

function connectSocket() {
  /* Connects to socket and registers callback functioms */
  socket = io();

  socket.on("connect", () => {
    socketID = socket.id;
    console.log("You are now connected with socket id: " + socketID);
  })

  socket.on("disconnect", () => {
    console.log("Your connection with socked id" + socketID + " has been closed!");
  })

  socket.on('response_back', function(){
    var stream_container = document.getElementById("photo");
    //source = `${window.static_folder}predictions/output_img.jpeg`;
    source = route_display_stream();
    console.log(source)
    timestamp = (new Date()).getTime(),
    newUrl = source + '?_=' + timestamp;
    stream_container.src = newUrl 
  });
};

function disconnectSocket() {
  /* Disconnects from socket */
  socket.disconnect();
}