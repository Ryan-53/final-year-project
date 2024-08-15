import cv2
import math

# Edit here to change resolution of orgininal image size and number of patches
NUM_PATCHES = 16

# Turn this to true to open a window showing grid on original image
SHOW_GRID = True

ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 - Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset Generation\\Rendering_final_test\\"
INPUT = ROOT_FOLDER + "initial_test_set\\mars_image_c-101"
INPUT_JPG = INPUT + ".jpg"

def crop_image(imgPath, numPatches):
  """
  Crops a full 2160 x 2160 image into patches as separate .jpg files

  :param imgPath: path of image to crop
  :param numPatches: number of patches to crop the image into
  :param loopNum: loop number - used if generating 2 sets of different patches
    (default = -2 [indicates to output images normally])
  :return: the original full image with gridlines drawn over it to show where
    the patches were cropped
  """

  IMG_SIZE = 2160
  imgPathJpg = imgPath + ".jpg"

  # Reads in the image
  img = cv2.imread(imgPathJpg)

  # Makes a copy of that image object
  img_copy = img.copy()

  # Calculates how big each patch will be in pixels
  croppedImgSize = int(IMG_SIZE / (math.sqrt(numPatches)))

  # Used to label each patch with its corresponding gridbox number
  i = 0

  # Adapted from learnopencv.com/cropping-an-image-using-opencv/
  for y in range(0, IMG_SIZE, croppedImgSize):
    for x in range(0, IMG_SIZE, croppedImgSize):

      # Checks whether there is enough space left in the image to crop another
      # patch
      if (IMG_SIZE - y) < croppedImgSize or (IMG_SIZE - x) < croppedImgSize:
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

      # Outputs the image with the given gridbox label
      cv2.imwrite(imgPath + "~" + str(gridbox) + ".jpg", patch)
      cv2.rectangle(img, (x, y), (x1, y1), (0, 0, 255), 2)

  print(f"Cropped image into {numPatches} patches")

  return img

def main():

  img = crop_image(INPUT, NUM_PATCHES)

  if SHOW_GRID == True:
    img = cv2.resize(img, (1080, 1080))
    cv2.imshow("Patches", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

