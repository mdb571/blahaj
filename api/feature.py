from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image

import time



from dotenv import load_dotenv

load_dotenv()

subscription_key=os.environ.get('SUBSCRIPTION_KEY')
endpoint=os.environ.get('ENDPOINT')
computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))


def describe_image(filename): 
    local_image = open(filename,'rb')
    description_result = computervision_client.describe_image_in_stream(local_image)
    local_image.close()
    if (len(description_result.captions) == 0):
        print("No description detected.")
    else:
        caption = sorted(description_result.captions,key= lambda i: i.confidence)[-1]
        caption = str(caption.text)
        if 'water' or 'outdoor'or'beach'or'nature'or'bird'or'ocean'or'bottle'or'surfing'or'flock'or'pile' in description_result.tags:
            print("It works")
            return 5
        else:
            return 0
        
        
