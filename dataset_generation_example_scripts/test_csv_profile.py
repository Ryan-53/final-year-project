"""
Writes labels and image patch paths to a csv file for training
"""

import csv
import os


# Constants - Paths
ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 \
- Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset \
Generation\\Final_Rendering\\"
SOURCE = ROOT_FOLDER
CSV_PATH = os.path.join(SOURCE, "test.csv")
TXT_FOLDER_PATH = os.path.join(SOURCE, "labels")
IMAGE_FOLDER_PATH = os.path.join(SOURCE, "images")

# Constant - Prefix names of images
IMAGE_PATH = "mars_image_c-"

# Constant - Image loop number starting value
LOOP_START = 391
LOOP_END = 459

# Constant - Number of patches per image
NUM_PATCHES = 64

# Constant - Measure of variance - range or standard deviation
VARIANCE = 'r' # r - range | s = standard deviation

with open(CSV_PATH, 'w', newline='') as csvFile:
  
  writer = csv.writer(csvFile)
  header = ["id", "label", "filename"]

  writer.writerow(header)

  # Loops through all images
  for i in range(LOOP_START, LOOP_END + 1):

    if VARIANCE == 'r':
      txtName = str(i) + ".txt"
    elif VARIANCE == 's':
      txtName = str(i) + "_sd.txt"
    txtPath = os.path.join(TXT_FOLDER_PATH, txtName)

    # Opens label txt file
    txtFile = open(txtPath, "r")

    #labels = [None] * 16
    #filenames = [IMAGE_PATH] * 16

    # Loops through lines in txt file and writes out the corresponding values
    # to the csv file
    for j in range(NUM_PATCHES):
      
      # Reads each line 1 by 1, converts it into a float and saves it in a list
      line = txtFile.readline()
      label = float((str("".join(line))).strip())

      # Creates a list of the image filepaths for the corresponding labels
      filename = IMAGE_PATH + str(i) + "~" + str(j) + ".jpg"

      idNum = ((i - LOOP_START) * NUM_PATCHES) + j

      writer.writerow([idNum, label, filename])

    txtFile.close()
      

    # Loops through all patches within an image
    #for j in range(16):
    
      #writer.writerow([(i+j), labels[j], ])