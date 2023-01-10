from flask import Flask #, render_template, request, redirect, url_for
from flask_socketio import SocketIO, emit
from general.general import general_bp

from utils_model.get_model import get_model
from utils_model.bboxes import plot_bboxes, NMS
import os

import io, base64
from PIL import Image
import numpy as np
import settings
import cv2

import sys
sys.path.append('../yolov5/')
from models.common import DetectMultiBackend
from utils.torch_utils import select_device

import detect

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.register_blueprint(general_bp, url_prefix='/')

# model = get_model()

print(detect.ROOT)
device = select_device('')
model = DetectMultiBackend('./yolov5s.pt', device=device, dnn=False, data='./data/coco128.yaml', fp16=False)

def predict_bboxes(img_orig, annotation_style, show_heuristic=False):
    """
    Loads the original image and logs the new image
    with the bounding boxes. It stores it a new folder
    called response. 

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    # Load original image
    # orig_img_path = os.path.join(settings.UPLOAD_FOLDER,img_name)
    # img_orig = cv2.imread(orig_img_path)
    
    # Get bounding boxes
    print('START DETECTION')
    output = model(img_orig)
    print('FINISH DETECTION')
    # Non-Max Supression: Filter only best bounding boxes
    best_bboxes =output.xyxy[0].cpu().numpy()# NMS(output.xyxy[0].numpy(), overlapThresh= settings.OVERLAP_THRESH)


    # Build image name and path
    # extension = '.' + img_name.split('.')[-1]
    # img_base_name = img_name.split('.')[:-1]
    
    # if annotation_style == 'bbox':
    #   img_name =  ''.join(img_base_name) + '_bbox' + extension
    # else:
    #   img_name =  ''.join(img_base_name) + '_heat' + extension
    img_name = 'output_img.jpeg'
    pred_img_path = os.path.join(settings.PREDICTIONS_FOLDER, img_name)  
    # Annotate image and stores it
    if best_bboxes.size == 0:
      cv2.imwrite(pred_img_path, img_orig)
      return img_orig
    else:
      img_pred = plot_bboxes(img_orig, box_coordinates= best_bboxes, style = annotation_style) 
      cv2.imwrite(pred_img_path, img_pred)     
      return img_pred       


@socketio.on('image')
def image(data_image):
  """
  Receives base64 string, converts it to a image file and stores it on disk.
  """
  print('get socket io request')
  img = Image.open(io.BytesIO(base64.decodebytes(bytes(data_image.replace('data:image/jpeg;base64,', ''), "utf-8"))))
  img.save('static/predictions/output_img.jpeg')

  # encoded_data = data_image.split(',')[1]
  # nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
  # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
  # predict_bboxes(img, 'bbox')

  print('START DETECTION')
  detect.run(model=model,source='static/predictions/output_img.jpeg',project='static',name='predictions',exist_ok=True)
  print('FINISH DETECTION')

  emit('response_back')





if __name__ == "__main__":
  app.run(debug=True)