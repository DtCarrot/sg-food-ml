from google.cloud import automl_v1beta1 as automl
from PIL import Image
from io import BytesIO
import os
import sys
import base64
from dotenv import load_dotenv
load_dotenv()

def predict_image(image_path=None, base64_data=None):
    project_id = os.getenv("PROJECT_ID")
    region_name = os.getenv("REGION_NAME")
    model_id = "ICN5857674000464820778"
    automl_client = automl.AutoMlClient()
    model_full_id = automl_client.model_path(
        project_id, region_name, model_id 
    )
    predict_client = automl.PredictionServiceClient()

    if image_path is not None:
        with open(image_path, "rb") as img:
            content = img.read()
        predict_payload = {"image": { "image_bytes": content }}

    if base64_data is not None:
        imgdata = base64.b64decode(str(base64_data))
        image = BytesIO(imgdata).getvalue()
        predict_payload = {"image": { "image_bytes": image }}
        print(predict_payload)

    response = predict_client.predict(model_full_id, predict_payload)
    return response.payload

# Call this function directly if called
if __name__ == '__main__':
    image_path = sys.argv[1]
    payload = predict_image(image_path=image_path)
    for result in payload:
        print("Predicted class name: {}".format(result.display_name))
        print("Predicted class score: {}".format(result.classification.score))

