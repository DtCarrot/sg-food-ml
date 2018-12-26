import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()
import os
from google.cloud import storage
from google.cloud import automl_v1beta1 as automl
from upload_food_image import upload_food_image_excel
from scrap_food_images import scrap_food_images

storage_client = storage.Client()
bucket_name = 'locationviz-1536759384444-vcm'
project_id = os.getenv('PROJECT_ID')
bucket_name = project_id + '-vcm'
region_name = os.getenv('REGION_NAME')
dataset_name = 'TEST_DATASET'
model_name = 'IMAGE_MODEL'
csv_file_name = 'images.csv'
train_budget = 1

# Engine to scrap images
food_list = ['bak chor mee', 'wanton mee', 'prawn mee', 'lor mee', 'mee siam']

# Loop through the list of images
scrap_food_images(food_list)

# After looping through all the classifier,
# We can upload them to google cloud bucket
idx = 0
bucket = storage_client.bucket(bucket_name)
# First, we read each individual directory
upload_food_image_excel(bucket, bucket_name, food_list, csv_file_name)
automl_client = automl.AutoMlClient()
project_location = automl_client.location_path(project_id, region_name)
# Define the classification_type
classification_type = 'MULTICLASS'
dataset_metadata = { 'classification_type': classification_type }
dataset_config = {
    'display_name': dataset_name,
    'image_classification_dataset_metadata': dataset_metadata
}
# Create a new automl dataset programatically
dataset = automl_client.create_dataset(project_location, dataset_config)
dataset_id = dataset.name.split('/')[-1]

dataset_full_id = automl_client.dataset_path(
    project_id, region_name, dataset_id
)

remote_csv_path = 'gs://{0}/{1}'.format(bucket_name, csv_file_name)
input_uris = remote_csv_path.split(',')
input_config = { 'gcs_source': { 'input_uris': input_uris }}
response = automl_client.import_data(dataset_full_id, input_config)

print("Processing import...")
# synchronous check of operation status.
print("Data imported. {}".format(response.result()))

image_recognition_model = {
    'display_name': model_name,
    'dataset_id': dataset_id,
    'image_classification_model_metadata': { "train_budget": train_budget }
}

response = automl_client.create_model(project_location, image_recognition_model)
print("Training operation name: {}".format(response.operation.name))
print("Training started...")
