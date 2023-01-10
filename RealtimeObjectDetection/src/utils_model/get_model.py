import torch
import os
import settings

def get_model(mode:str = "local", model_folder_s3: str = settings.MODELS_FOLDER_S3):
    """
    Connects to S3 bucket services and download the best custo Yolov5 model 
    trained by the user

    Parameters
    ----------
    model_folder_s3 : str
        Path to the folder where the best model is contained.

    Returns
    -------
    model: yolov5 model
        Custom Yolov5 trained model.
    """ 
    # Load the yolov5 model
    model = torch.hub.load('ultralytics/yolov5', 'custom', path=os.path.join(settings.MODELS_FOLDER,settings.BEST_MODEL))
    
    return model