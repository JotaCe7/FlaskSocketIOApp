from flask import Flask #, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from general.general import general_bp

import io, base64
from PIL import Image

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.register_blueprint(general_bp, url_prefix='/')

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