import time
from google_images_download import google_images_download   #importing the library
response = google_images_download.googleimagesdownload()   #class instantiation
def scrap_food_images(food_list):
    for food in food_list:
        arguments = {"keywords": food, "limit": 100, "print_urls": True}
        paths = response.download(arguments)
        print(paths)
        # Set a delay
        time.sleep(5)
