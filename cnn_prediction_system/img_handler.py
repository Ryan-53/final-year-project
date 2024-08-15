import cv2
import math
import os

PROCESSED_IMAGE_PATH = "uploaded_image_proc\\full_uploaded_processed_image.jpg"

def crop_image(imgPath, patchPath):
  """
  Crops a full 2160 x 2160 image into patches as separate .jpg files

  :param imgPath: path of image to crop
  :param patchPath: path of folder to save patches to
  """
  # Initialises image size
  imgSize = 2160

  # Reads in the image
  imgOriginal = cv2.imread(imgPath)

  ### Preprocessing and checking image
  # Finds size of image that has been loaded in
  imgHeight, imgWidth, imgChannels = imgOriginal.shape
  print(f"Original image attributes: height={imgHeight}, width={imgWidth}, channels={imgChannels}")

  ## Checking image shape is correct
  # Checks the image has a 1:1 aspect ratio, if not terminate the function
  if imgHeight != imgWidth:
    print("Cropping image into a 1:1 aspect ratio")
    
    # Calculates the size to crop the rectangular image to
    squareSize = min(imgHeight, imgWidth)

    # Calculates coordinates of new square within image for cropping
    squareTop = (imgHeight - squareSize) // 2
    squareBottom = squareTop + imgSize
    squareLeft = (imgWidth - squareSize) // 2
    squareRight = squareLeft + squareSize

    # Crops input image into a square (1:1 ratio)
    imgSquare = imgOriginal[squareTop:squareBottom, squareLeft:squareRight]

  else:
    imgSquare = imgOriginal.copy()

  # Finds size of squared image
  imgSquareHeight, imgSquareWidth, imgSquareChannels = imgSquare.shape
  print(f"Square image attributes: height={imgSquareHeight}, width={imgSquareWidth}, channels={imgSquareChannels}")


  #### CHECK THIS ERROR RANGE ####
  # Changes imgSize to 1080 if the image is smaller than that + error range,
  # if not, it remains at 2160
  if min(imgHeight, imgWidth) < 1200:
    imgSize = 1080
  
  # Resizes the image if it is not at the correct size (2160 or 1080)
  if imgHeight != imgSize:
    img = cv2.resize(imgSquare, (imgSize, imgSize))

  # If image already correct size
  else:
    img = imgSquare.copy()

  # Finds size of resized image
  imgResizedHeight, imgResizedWidth, imgResizedChannels = img.shape
  print(f"Resized image attributes: height={imgResizedHeight}, width={imgResizedWidth}, channels={imgResizedChannels}")

  # Saves processed uploaded image
  cv2.imwrite(PROCESSED_IMAGE_PATH, img)

  # Makes a copy of that image object
  img_copy = img.copy()

  # Calculates how big each patch will be in pixels
  croppedImgSize = int(imgSize / (math.sqrt(64)))

  # Used to label each patch with its corresponding gridbox number
  i = 0

  # Adapted from learnopencv.com/cropping-an-image-using-opencv/
  for y in range(0, imgSize, croppedImgSize):
    for x in range(0, imgSize, croppedImgSize):

      # Checks whether there is enough space left in the image to crop another
      # patch
      if (imgSize - y) < croppedImgSize or (imgSize - x) < croppedImgSize:
        break

      # x and y are the starting co-ordinates of the patch
      # x1 and y1 are the ending co-ordinates of the patch
      y1 = y + croppedImgSize
      x1 = x + croppedImgSize

      # Crops a patch given the size to crop to
      patch = img_copy[y:y+croppedImgSize, x:x+croppedImgSize]

      # Calculates gridbox to label the image with
      gridbox = i
      i += 1

      patchImgName = os.path.join(patchPath, f"{str(gridbox)}.jpg")
      
      """
      # Outputs the image with the given gridbox label
      if imgSize == 2160:
        resizedPatch = cv2.resize(patch, (135, 135))
        cv2.imwrite(patchImgName, resizedPatch)
      else:
      """

      cv2.imwrite(patchImgName, patch)      

  print(f"Cropped image into {64} patches")


def draw_rect(patchNum):
  """
  Draws rectangle to highlight patch of patchNum

  :param patchNum: patch to draw rectangle around
  :return: full image with a rectangle drawn around the selected patch
  """
  imgSize = 2160

  # Reads in the image
  imgOriginal = cv2.imread(PROCESSED_IMAGE_PATH, 1)

  ################# ALL THIS CHECKS CAN BE REMOVED ##########################
  ### Preprocessing and checking image
  # Finds size of image that has been loaded in
  imgHeight, imgWidth, imgChannels = imgOriginal.shape
  print(f"Predicted image attributes: height={imgHeight}, width={imgWidth}, channels={imgChannels}")

  ## Checking image shape is correct
  # Checks the image has a 1:1 aspect ratio, if not terminate the function
  if imgHeight != imgWidth:
    print("!!!---ERROR---!!! - Image is not in a 1:1 aspect ratio")
    return None
  
  # Checks the image has a colour depth of 3, if not terminate the function
  elif imgChannels != 3:
    print("!!!---ERROR---!!! - Image does not have RGB colour depth")
    return None
  
  # Changes imgSize to 1080 if the image < 1200 (so images slightly larger than
  # it do not get upsized massively), if not it remains at 2160
  elif imgHeight < 1080:
    imgSize = 1080
  
  # Resizes the image if it is not at the correct size (2160 or 1080)
  if imgHeight != imgSize:
    img = cv2.resize(imgOriginal, (imgSize, imgSize))

  # If image already correct size
  else:
    img = imgOriginal.copy()

  # Converting image to greyscale
  #imgGrey = img.copy()
  #imgGrey.convertTo(imgGrey, CV_24SC1, 1)

  # Calculates how big each patch will be in pixels
  croppedImgSize = int(imgSize / (math.sqrt(64)))

  # Used to label each patch with its corresponding gridbox number
  i = 0

  ## Adapted from learnopencv.com/cropping-an-image-using-opencv/
  for y in range(0, imgSize, croppedImgSize):
    for x in range(0, imgSize, croppedImgSize):

      # Checks whether there is enough space left in the image to crop another
      # patch
      if (imgSize - y) < croppedImgSize or (imgSize - x) < croppedImgSize:
        break

      # x and y are the starting co-ordinates of the patch
      # x1 and y1 are the ending co-ordinates of the patch
      y1 = y + croppedImgSize
      x1 = x + croppedImgSize

      # Draw a rectangle around the patch selected as the LS by the model
      if i == patchNum:
        cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 10)

      # Iterates patch gridbox number
      i += 1

  print("Highlighted chosen LS patch")

  return img
