import os

## Sets root folder path for easier path calling
ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 \
- Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset \
Generation\\Rendering_final_test\\"
LOOP_TXT_PATH = (ROOT_FOLDER + "loop_num.txt")

def load_loop_num(loopTxtPath):
  """
  Loads the current iteration number for image numbering

  :param loopTxtPath: path of txt file where loop num is located
  :return: loop number
  """

  ## Loads in loop number from txt file
  file = open(loopTxtPath, "r")
  loopNum = file.read()
  file.close()

  return loopNum


def rename_and_iterate(root, loopTxtPath, loopNum, version):
  """
  Renames all newly generated files and iterates loop by writing to txt file

  :param root: root folder where dataset generation takes place
  :param loopTxtPath: path of txt file where loop num is located
  :param loopNum: current iteration number
  :param version: char code of the machine generating the dataset (c=personal)
  """

  ## Renaming image file
  newPath = (root + "images\\mars_image_{v}-{num}.jpg")
  newPathFormatted = newPath.format(v = version, num = loopNum)
  oldPath= (root + "images\\mars_image_c.0001.tif")
  os.rename(oldPath, newPathFormatted)


  ## Renaming terrain file
  newPath = (root + "terrain\\mars_terrain_{v}-{num}.obj")
  newPathFormatted = newPath.format(v = version, num = loopNum)
  oldPath= (root + "terrain\\mars_terrain_c.obj")
  os.rename(oldPath, newPathFormatted)

  ## Incrementing loop num
  loopNumInt = int(loopNum)
  loopNumInt += 1

  ## Writing the updated loop num to the txt
  file = open(loopTxtPath, "w")
  num_str = str(loopNumInt)
  file.write(num_str)
  file.close()

  print("Renamed files")