import os
import cv2
import numpy as np
from img_handler import draw_rect, crop_image

# Constants - crop_image
PATCH_FOLDER = "patches"
PROCESSED_IMAGE_PATH = "uploaded_image_proc\\full_uploaded_processed_image.jpg"

# Constants - Test
TEST_IMAGES_SOURCE = "tests\\pytest_images"
STANDARD_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "standard_generated.jpg")
STANDARD_PREDICTED = os.path.join(TEST_IMAGES_SOURCE, "predicted_standard.jpg")
GENERAL_IMAGE_PATH = os.path.join(TEST_IMAGES_SOURCE, "lander_vision_photo.jpg")
GENERAL_PREDICTED = os.path.join(TEST_IMAGES_SOURCE, "predicted_general.jpg")

def test_standard_draw() -> None:
  """
  Tests the drawing of the rectangle on the uploaded standard image with a
  given patch
  """
  # Processes image and draws a rectangle where it is highlighted
  crop_image(STANDARD_IMAGE_PATH, PATCH_FOLDER)
  drawnImg = draw_rect(42)
  resizedImg = cv2.resize(drawnImg, (1080, 1080))

  # Compared to the result of it using the system
  expectedImg = cv2.imread(STANDARD_PREDICTED)

  assert np.bitwise_xor(resizedImg,expectedImg).any()

def test_general_draw() -> None:
  """
  Tests the drawing of the rectangle on the uploaded standard image with a
  given patch
  """
  # Processes image and draws a rectangle where it is highlighted
  crop_image(GENERAL_IMAGE_PATH, PATCH_FOLDER)
  drawnImg = draw_rect(6)
  resizedImg = cv2.resize(drawnImg, (1080, 1080))

  # Compared to the result of it using the system
  expectedImg = cv2.imread(GENERAL_PREDICTED)

  assert np.bitwise_xor(resizedImg,expectedImg).any()