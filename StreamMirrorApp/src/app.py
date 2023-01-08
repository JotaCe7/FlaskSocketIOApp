from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

import io, base64
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route("/")
def message():
  return render_template("index.html")

@socketio.on('image')
def image(data_image):
  """
  Receives base64 string, converts it to a image file and stores it on disk.
  """
  img = Image.open(io.BytesIO(base64.decodebytes(bytes(data_image.replace('data:image/jpeg;base64,', ''), "utf-8"))))
  img.save('src/static/predictions/output_img.jpeg')
  emit('response_back')

if __name__ == "__main__":
  app.run(debug=True)