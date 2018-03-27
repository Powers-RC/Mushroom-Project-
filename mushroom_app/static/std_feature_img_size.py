from PIL import Image
import os

#contain with image file paths
filepaths = os.listdir('/Users/powers_rc/DS_practice/mushroom_project/mushroom_app/static/feature_imgs')

for p in filepaths:
    img = Image.open('/Users/powers_rc/DS_practice/mushroom_project/mushroom_app/static/feature_imgs/' + p)
    new_img = img.resize((264,264))
    new_img.save('/Users/powers_rc/DS_practice/mushroom_project/mushroom_app/static/feature_imgs/'+ p)
