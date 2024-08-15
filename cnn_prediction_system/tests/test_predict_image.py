import os
from model_handler import predict_image
from img_handler import crop_image

# Constants - predict_image
PATCH_FOLDER = "patches"
CSV_PATH = "bin\\patch.csv"
MODEL_PATH = "source\\Final_greyscale_model_compat_mode.h5"
LAMBDA_TXT_PATH = "source\\final_lambda.txt"

# Constants - Test
TEST_IMAGES_SOURCE = "tests\\pytest_images"
STANDARD_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "standard_generated.jpg")
STANDARD_2_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "standard_generated_2.jpg")
PNG_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "filetype_test.png")
GREYSCALE_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "greyscale_generated.jpg")
GENERAL_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "lander_vision_photo.jpg")

def pred_patch_test(imagePath, expectedPatch, expectedValue):
  """
  Tests the system using the model's prediction

  :param imagePath: path of image to test
  :param expectedPatch: number of patch expected to be predicted as smoothest
  :param expectedValue: value expected to be predicted
  :return: true or false whether the test has passed
  """
  # Uploads image and uses model to predict it
  crop_image(imagePath, PATCH_FOLDER)
  selectedPatch, predictionValue = predict_image(CSV_PATH, PATCH_FOLDER, MODEL_PATH, LAMBDA_TXT_PATH)

  if (selectedPatch == expectedPatch) and (predictionValue == expectedValue):
    return True
  else:
    return False


def test_standard() -> None:
  """
  Tests standard generated image
  """
  pred_patch_test(STANDARD_IMAGE_PATH, 42, 48.39)


def test_standard_2() -> None:
  """
  Tests a different standard generated image
  """
  pred_patch_test(STANDARD_2_IMAGE_PATH, 3, 47.44)


def test_png() -> None:
  """
  Tests a png version of a generated image
  """
  pred_patch_test(PNG_IMAGE_PATH, 42, 48.39)


def test_greyscale() -> None:
  """
  Tests greyscale generated image
  """
  pred_patch_test(GREYSCALE_IMAGE_PATH, 42, 47.95)


def test_general() -> None:
  """
  Tests real lander vision camera image
  """
  pred_patch_test(GENERAL_IMAGE_PATH, 33, 63.62)