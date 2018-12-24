import os
import pandas as pd

# Check whether the file is a valid image. For this app, only accept .jpg and .png extensions
def check_if_file_type_valid(image):
    # List of valid extensions
    exts = {'.jpg', '.png'}
    file_valid = any(image.endswith(ext) for ext in exts)
    return file_valid

def upload_food_image_excel(bucket, bucket_name, food_list, csv_file_name):
    idx = 0
    # Create a new dataframe
    df = pd.DataFrame(columns=['file', 'name'])
    # Loop through the different type of food labels in local disk
    for food in food_list:
        files = os.listdir(os.path.join('downloads', food))
        # Iterate the files in the food folder
        for file in files:

            if check_if_file_type_valid(file) == False:
                # Ignore this file and continue
                print("Not valid extension")
                continue

            # file_dir - The file dir in local disk
            file_dir = os.path.join('downloads', food, file)

            # remote_file_name - Where we will like to store the image in Google Cloud
            remote_file_name = os.path.join('food-dataset', food, file)

            # Upload image to Google Cloud
            blob = bucket.blob(remote_file_name)
            # Upload blob from named file in local disk
            blob.upload_from_filename(file_dir)

            # Append the location of this image in Google Cloud to the excel sheet.
            gs_name = 'gs://' + bucket_name + '/' + os.path.join('food-dataset', food, file)
            df.loc[idx] = [gs_name, food]
            idx = idx + 1

        print('Successfully uploaded: {0}', remote_file_name)

    # Save the excel file without row and column header
    csv_file_name = 'images.csv'
    df.to_csv(csv_file_name, header=False, index=False)
    # Upload csv to google cloud
    blob = bucket.blob(csv_file_name)
    blob.upload_from_filename(csv_file_name)




