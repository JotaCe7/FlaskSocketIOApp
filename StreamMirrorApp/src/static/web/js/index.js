var is_recording = false;
const video = document.querySelector("#videoElement");

document.querySelector("#start").addEventListener('click', async (e) => {
  /* Connect to socket and start video capture */
  connectSocket();
  startVideoCapture();
  is_recording = true;
})

document.querySelector("#stop").addEventListener('click', async (e) => {
  /* Disconnect from socket and stop video capture */
  disconnectSocket();
  stopVideoCapture();
  is_recording = false;
});


const FPS = 6;
setInterval(() => {
  /* Updates output frame */
  var resizedCanvas = document.createElement("canvas");
  var resizedContext = resizedCanvas.getContext("2d");

  resizedCanvas.height = video.clientHeight;
  resizedCanvas.width = video.clientWidth;
  
  width=video.clientWidth;
  height=video.clientHeight;
  resizedContext.drawImage(video, 0, 0, width , height );
  var data = resizedCanvas.toDataURL('image/jpeg', 0.92);
  resizedContext.clearRect(0, 0, width,height );
  if(is_recording === true) {
    socket.emit('image', data);
    console.log('RECORDING')
  }
  else {
    console.log('NOT RECORDING')
  }
}, 1000/FPS);


async function startVideoCapture() {
  /* Starts video capture */
  const stream = await navigator.mediaDevices.getUserMedia({
    audio: false,
    video: {
      facingMode: 'environment'
      // facingMode: 'user'
    }
  })
  .then(function (stream) {
      video.srcObject = stream;
      video.play();
  })
  .catch(function (err0r) {
    console.log(err0r)
  });

}

async function stopVideoCapture() {
  /* Stops video capture */
  const mediaStream = video.srcObject;
  const tracks = mediaStream.getTracks();
  tracks[0].stop();
}