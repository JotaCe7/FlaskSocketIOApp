# Python imports
import cv2
import numpy as np

# Self-made
from enum import Enum

import settings

#from settings import CLASSES, COLORMAP


class CLASSES(Enum):
  PRODUCT = 3
  MISSING = 2

# COLORMAP PER CLASS
class COLORMAPS(Enum):
  PRODUCT = 'COLORMAP_TURBO'
  MISSING = 'COLORMAP_RAINBOW'



#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Functions
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def plot_bboxes(img, box_coordinates, style: str = 'bbox'):
    """ 
    It plots the bounding boxes in green when products are present.
    If there are missing products, then red bboxes are drawn.

    Parameters
    ----------
    img_path: str
        Path to image.
        
    box_coordinates: pd.DataFrame
        Contains the image coordinates to plot. 
        Default = None: searches for the coordinates in the static dataset (.csv)
        stored under `data/SKU110K/annotations/annotations.csv`.
        
    axes: matplotlib.axes.Axes (Optional)
        Axes in which to plot the image.
        
    skip_plot: bool
        Wether to skip or not the plot of the image.
        
    style: str
        The style of the bounding boxes. Use:
        - bbox: for standard bboxes
        - heatmap: heatmap version for (missing products only)
        
    Returns
    ----------
    img: np.array (Optional)
        Image plotted.
    """
    #Read the image
    #img = cv2.imread(img_path)
    
    if style == 'bbox':
      
        # Plot all boxes
        for row in box_coordinates:
            print(row)
            x1, y1, x2, y2, conf, cls = row.astype(int)
            print('x1',x1,type(x1))
            if cls == CLASSES.PRODUCT.value:
                img = cv2.rectangle(img, (x1, y1), (x2, y2), settings.COLOR_BLUE, thickness=5)
            else:
                img = cv2.rectangle(img, (x1, y1), (x2, y2), settings.COLOR_RED, thickness=7)
                  
    
    elif style == 'heatmap':
        for cls in CLASSES:
          img = apply_heatmap(img,box_coordinates[box_coordinates[:,5]==cls.value], getattr(cv2, COLORMAPS[cls.name].value))

    return img

def apply_heatmap(img, bboxes, colormap):
  h, w , _ = img.shape
  img_bw = np.zeros((h,w,1), np.uint8)
  for row in bboxes:
    img_bw[row[1]:row[3], row[0]:row[2]] = 255
  img_bw = cv2.distanceTransform(img_bw, cv2.DIST_L1, maskSize=5).astype(np.uint8)
  img_bw = cv2.applyColorMap(img_bw, colormap)
  
  for row in bboxes:
    merged_bbox  = cv2.addWeighted( img_bw[row[1]:row[3], row[0]:row[2]], 0.8, img[row[1]:row[3], row[0]:row[2]], 0.2, 0)
    img[row[1]:row[3], row[0]:row[2]] = merged_bbox

  return img

def NMS(boxes, overlapThresh = 0.4):
    
    """
    Receives `boxes` as a `numpy.ndarray` and gets the best bounding 
    box when there is overlapping bounding boxes.

    Parameters
    ----------
    boxes : numpy.ndarray
        Array with all the bounding boxes in the image.

    Returns
    -------
    best_bboxes: pd.DataFrame
        Dataframe with only the best bounding boxes, 
        in the format: ["xmin","ymin","xmax","ymax","class"]
    """
    
    #return an empty list, if no boxes given
    if len(boxes) == 0:
        return []
    x1 = boxes[:, 0]  # x coordinate of the top-left corner
    y1 = boxes[:, 1]  # y coordinate of the top-left corner
    x2 = boxes[:, 2]  # x coordinate of the bottom-right corner
    y2 = boxes[:, 3]  # y coordinate of the bottom-right corner

    # compute the area of the bounding boxes and sort the bounding
    # boxes by the bottom-right y-coordinate of the bounding box
    areas = (x2 - x1 + 1) * (y2 - y1 + 1) # We have a least a box of one pixel, therefore the +1
    indices = np.arange(len(x1))
    for i,box in enumerate(boxes):

        
        temp_indices = indices[indices!=i]
        xx1 = np.maximum(box[0], boxes[temp_indices,0])
        yy1 = np.maximum(box[1], boxes[temp_indices,1])
        xx2 = np.minimum(box[2], boxes[temp_indices,2])
        yy2 = np.minimum(box[3], boxes[temp_indices,3])
        w = np.maximum(0, xx2 - xx1 + 1)
        h = np.maximum(0, yy2 - yy1 + 1)
        # compute the ratio of overlap
        overlap = (w * h) / areas[temp_indices]
        
        if np.any(overlap) > overlapThresh:
            
            if box[4] == 0.0:
                continue

            indices = indices[indices != i]
            
    best_bboxes =   boxes[indices].astype(int)
    
    
    #best_bboxes_df = pd.DataFrame(data = best_bboxes, columns=["x1","y1","x2","y2","class"])
    
    
    return best_bboxes