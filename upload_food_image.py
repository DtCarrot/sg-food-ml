import os
import pandas as pd

def check_if_file_type_valid(image):
    # List of valid extensions
    exts = {'.jpg', '.png'}
    file_valid = any(image.endswith(ext) for ext in exts)
    return file_valid

def upload_food_image_excel(bucket, bucket_name, food_list, csv_file_name):
    idx = 0
    df = pd.DataFrame(columns=['file', 'name'])
    for food in food_list:

        files = os.listdir(os.path.join('downloads', food))
        for file in files:
            if check_if_file_type_valid(file) == False:
                # Ignore this file and continue
                print("Not valid extension")
                continue
            file_dir = os.path.join('downloads', food, file)
            remote_file_name = os.path.join('food-dataset', food, file)
            print(file_dir)
            blob = bucket.blob(remote_file_name)
            blob.upload_from_filename(file_dir)
            gs_name = 'gs://' + bucket_name + '/' + os.path.join('food-dataset', food, file)
            df.loc[idx] = [gs_name, food]
            # df.append([file_name, food])
            idx = idx + 1
        print('Successfully uploaded: {0}', remote_file_name)
    csv_file_name = 'images.csv'
    df.to_csv(csv_file_name, header=False, index=False)
    # Upload csv to google cloud
    blob = bucket.blob(csv_file_name)
    blob.upload_from_filename(csv_file_name)



