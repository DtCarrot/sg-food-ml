from google.cloud import automl_v1beta1 as automl
import os
import sys
from dotenv import load_dotenv
load_dotenv()
image_path = sys.argv[1]
project_id = os.getenv("PROJECT_ID")
region_name = os.getenv("REGION_NAME")

model_id = "ICN5857674000464820778"
automl_client = automl.AutoMlClient()
model_full_id = automl_client.model_path(
    project_id, region_name, model_id 
)
predict_client = automl.PredictionServiceClient()

with open(image_path, "rb") as img:
    content = img.read()
predict_payload = {"image": { "image_bytes": content }}

response = predict_client.predict(model_full_id, predict_payload)
print("Prediction results:")
for result in response.payload:
    print("Predicted class name: {}".format(result.display_name))
    print("Predicted class score: {}".format(result.classification.score))
