import os
import cv2
from img_handler import crop_image

# Constants - crop_image
PATCH_FOLDER = "patches"
PROCESSED_IMAGE_PATH = "uploaded_image_proc\\full_uploaded_processed_image.jpg"

# Constants - Standard tests
PATCH_0_PATH = os.path.join(PATCH_FOLDER, "0.jpg")
PATCH_63_PATH = os.path.join(PATCH_FOLDER, "63.jpg")

# Constants - Test
TEST_IMAGES_SOURCE = "tests\\pytest_images"
STANDARD_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "standard_generated.jpg")
OVERSIZED_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "oversized.jpg")
UNDERSIZED_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "undersized.jpg")
RECTANGULAR_HORI_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "rectangular_hori.jpg")
RECTANGULAR_VERT_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "rectangular_vert.jpg")
PNG_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "filetype_test.png")
GREYSCALE_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "greyscale_generated.jpg")
GENERAL_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "lander_vision_photo.jpg")

### STANDARD TESTS - Used on different images later ###

def shape_test(imagePath, small=False):
  """
  Tests the processing of an image from dataset into the correct size and
  colour

  :param imagePath: path of image to test
  :param small: boolean determining whether to test based on the image
    being the standard size (2160) or small (1080) - defaults to False for
    dealing with an image over 1080
  :return: returns true or false whether the test has passed
  """
  crop_image(imagePath, PATCH_FOLDER)

  img = cv2.imread(PROCESSED_IMAGE_PATH)

  imgHeight, imgWidth, imgChannels = img.shape

  if (imgHeight == imgWidth) and ((imgHeight == 1080 and small == True) or (imgHeight == 2160 and small == False)):
    return True
  else:
    return False


def patchSize_test(imagePath, small=False):
  """
  Tests the cropping of an image from dataset into 64 patches

  :param imagePath: path of image to test
  :param small: boolean determining whether to test based on the image
    being the standard size (2160) or small (1080)
  :return: returns true or false whether the test has passed
  """
  crop_image(imagePath, PATCH_FOLDER)

  img = cv2.imread(PATCH_0_PATH)

  imgHeight, imgWidth, imgChannels = img.shape

  if (imgHeight == imgWidth) and ((imgHeight == 135 and small == True) or (imgHeight == 270 and small == False)):
    return True
  else:
    return False


def numPatches_test(imagePath):
  """
  Tests the cropping of an image from dataset into the correct sized patches

  :param imagePath: path of image to test
  :return: returns true or false whether the test has passed
  """
  if os.path.exists(PATCH_0_PATH):
    os.remove(PATCH_0_PATH)
  if os.path.exists(PATCH_63_PATH):
    os.remove(PATCH_63_PATH)

  crop_image(imagePath, PATCH_FOLDER)

  if (os.path.exists(PATCH_0_PATH)) and (os.path.exists(PATCH_63_PATH)):
    return True
  else:
    return False


### IMAGE TESTS ###

def test_standard_generated_jpg_colour() -> None:
  """
  Tests standard generated image
  """
  assert shape_test(STANDARD_IMAGE_PATH)
  assert patchSize_test(STANDARD_IMAGE_PATH)
  assert numPatches_test(STANDARD_IMAGE_PATH)


def test_oversized() -> None:
  """
  Tests oversized generated image
  """
  assert shape_test(OVERSIZED_IMAGE_PATH)
  assert patchSize_test(OVERSIZED_IMAGE_PATH)
  assert numPatches_test(OVERSIZED_IMAGE_PATH)


def test_undersized() -> None:
  """
  Tests undersized generated image
  """
  assert shape_test(UNDERSIZED_IMAGE_PATH, True)
  assert patchSize_test(UNDERSIZED_IMAGE_PATH, True)
  assert numPatches_test(UNDERSIZED_IMAGE_PATH)


def test_rectangular_horizontal() -> None:
  """
  Tests rectangular generated image
  """
  assert shape_test(RECTANGULAR_HORI_IMAGE_PATH)
  assert patchSize_test(RECTANGULAR_HORI_IMAGE_PATH)
  assert numPatches_test(RECTANGULAR_HORI_IMAGE_PATH)


def test_rectangular_vertical() -> None:
  """
  Tests rectangular generated image
  """
  assert shape_test(RECTANGULAR_VERT_IMAGE_PATH, True)
  assert patchSize_test(RECTANGULAR_VERT_IMAGE_PATH, True)
  assert numPatches_test(RECTANGULAR_VERT_IMAGE_PATH)


def test_png() -> None:
  """
  Tests png file of generated image
  """
  assert shape_test(PNG_IMAGE_PATH)
  assert patchSize_test(PNG_IMAGE_PATH)
  assert numPatches_test(PNG_IMAGE_PATH)


def test_greyscale() -> None:
  """
  Tests greyscale generated image
  """
  assert shape_test(RECTANGULAR_HORI_IMAGE_PATH)
  assert patchSize_test(RECTANGULAR_HORI_IMAGE_PATH)
  assert numPatches_test(RECTANGULAR_HORI_IMAGE_PATH)


def test_general_photo() -> None:
  """
  Tests real lander vision camera image
  """
  assert shape_test(GENERAL_IMAGE_PATH, True)
  assert patchSize_test(GENERAL_IMAGE_PATH, True)
  assert numPatches_test(GENERAL_IMAGE_PATH)

  


