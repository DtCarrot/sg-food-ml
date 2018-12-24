# sg-food-ml

This script is used to scrap images from the Internet to classify 5 common noodle "mee" dishes in Singapore. Wanton Mee, Bak Chor Mee, Lor Mee, Prawn Mee and Mee Siam. 

After scraping, the script will automatically upload the images to the indicated Google Cloud Storage bucket and import them into the AutoML dataset. It will then automatically create a new model (train the dataset) which will take a while.

I have written an [article](https://blog.darrenong.me/classifying-the-different-type-of-singapore-noodle-mee-dishes-using-googles-openml/) to explain in detail how this script works.

## Prediction

In order to make prediction programatically, I have included the predict.py script. To execute the script, run the following command

```
python predict.py <path of image we will like to receive>
```

## Limitations

1. At this point of time, the scraper can only scrap 100 images per keyword. In order to scrap more than 100 images, you will need to install Selenium driver along with chromedriver. We are using [google-images-download] (https://help.github.com/articles/basic-writing-and-formatting-syntax/#links) under the hoods, so you can refer to their Github page on how to do so.

2. Currently, I haven't automated the logic to automatically create a new bucket on Google Cloud Storage, you will need to manually create your own bucket.

