# Third-party modules used
from collections import namedtuple

# Importing made functions to call
from rename import load_loop_num, rename_and_iterate
from range_test import load_obj, calc_corners, calc_gridlines, \
  calc_grid_height, locate_point, write_diffs_to_file
from crop_img_test import crop_image
from delete import move_main_image, delete_terrain

# Constants - Paths
ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 \
- Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset \
Generation\\Final_Rendering\\"
LOOP_TXT_PATH = (ROOT_FOLDER + "loop_num.txt")
DIFFS_TXT_PATH = ROOT_FOLDER + "labels\\"

# Constants - Dataset generation settings
MACHINE_VERSION = "c"

# Constants - Patch settings
NUM_PATCHES = 64
NUM_GRIDLINES = 18 # 16=10, 64=18, 256=34

# Loads in loop number
loopNumber = load_loop_num(LOOP_TXT_PATH)

# Constants - Generated file paths
INPUT_TERRAIN = ROOT_FOLDER + "terrain\\mars_terrain_c-" + str(loopNumber)
INPUT_OBJ = INPUT_TERRAIN + ".obj"
INPUT_IMAGE = ROOT_FOLDER + "images\\mars_image_c-" + str(loopNumber)
INPUT_JPG = INPUT_IMAGE + ".jpg"

# Renames files and iterates loopNumber
rename_and_iterate(ROOT_FOLDER, LOOP_TXT_PATH, loopNumber, MACHINE_VERSION)

# Named tuple storing x, y and z values for all points
Point = namedtuple('Point', 'x y z')

# Loads all vertices into an array
vertices = load_obj(INPUT_OBJ)

# Calculates corners of bounding box
box = calc_corners(vertices)

# Calculates gridlines separating patches
gridlines = calc_gridlines(box, NUM_GRIDLINES)

# Calculates height differences in each patch
height_diffs = calc_grid_height(vertices, gridlines, NUM_PATCHES)

# Writes height differences for every patch out to a txt file
write_diffs_to_file(height_diffs, DIFFS_TXT_PATH, loopNumber)

# Deletes the terrain .obj file to save space as it is no longer needed
delete_terrain(ROOT_FOLDER, loopNumber)

# Crops the image into patches and outputs each patch to a separate .jpg file
# img is the original image with the gridlines drawn over it
img = crop_image(INPUT_IMAGE, NUM_PATCHES)

# Moving main image to a different directory so its not in the dataset with all
# of the patches
move_main_image(ROOT_FOLDER, loopNumber)

print("IMAGE", loopNumber, "COMPLETE")