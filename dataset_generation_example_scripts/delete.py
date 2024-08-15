import os

ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 \
- Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset \
Generation\\Final_Rendering\\"
SOURCE = ROOT_FOLDER # + "Test_model\\"

def delete_main_images(firstNum, lastNum):
  """
  Deletes main large images from first to last including both
  :param firstNum: number of image to start deleting from
  :param lastNum: number of image to delete last
  """

  for i in range(firstNum, lastNum+1):
      
    imagePath = SOURCE + "images\\mars_image_c-" + str(i) + ".jpg"
    
    if os.path.exists(imagePath):
      os.remove(imagePath)
      print(f"{i} Deleted")
    else:
      print(f"{i} Not found")

def delete_patches(firstNum, lastNum, numPatches):
  """
  Deletes all patches of images from first to last including both, excluding
  the main larger image
  :param firstNum: number of image to start deleting from
  :param lastNum: number of image to delete last
  :param numPatches: number of patches per image to delete
  """

  # Loops through each main image number
  for i in range(firstNum, lastNum+1):

    # Loops through each patch number within an image number
    for j in range(numPatches):
      
      imagePath = SOURCE + f"images\\mars_image_c-{str(i)}~{str(j)}.jpg"

      if os.path.exists(imagePath):
        os.remove(imagePath)
        print(f"{i}-{j} Deleted")
      else:
        print(f"{i}-{j} Not found")

def move_main_image(root, loopNum):
  """
  Moves the main unpatched image from the images directory to a separate one
  just for main images
  :param root: root folder where dataset generation is taking place
  :param loopNum: loopNumber/image number to move
  """

  oldImagePath = root + f"images\\mars_image_c-{str(loopNum)}.jpg"
  newImagePath = root + f"main_images\\mars_image_c-{str(loopNum)}.jpg"


  if os.path.exists(oldImagePath):
    os.rename(oldImagePath, newImagePath)
    print(f"Main image {loopNum} moved")
  else:
    print(f"Main image {loopNum} not found")

def delete_terrain(root, loopNum):
  """
  Deletes the terrain .obj file after the labels have been generated to save
  storage space
  :param root: root folder where dataset generation is taking place
  :param loopNum: loopNumber/terrain number to delete
  """

  terrainPath = root + f"terrain\\mars_terrain_c-{str(loopNum)}.obj"

  if os.path.exists(terrainPath):
    os.remove(terrainPath)
    print(f"Terrain {loopNum} deleted")
  else:
    print(f"Terrain {loopNum} not found")

### Main ###
def main():

  #delete_patches(201, 210, 16)

  move_main_image(ROOT_FOLDER, 0)

  #delete_terrain(ROOT_FOLDER, 0)

if __name__ == "__main__":
    main()