from collections import namedtuple
import numpy as np

# Constants - Paths
ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 - Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset Generation\\Rendering_final_test\\"
INPUT = ROOT_FOLDER + "initial_test_set\\mars_terrain_c-101"
INPUT_OBJ = INPUT + ".obj"
DIFFS_TXT_PATH = ROOT_FOLDER + "initial_test_set\\labels\\"

# Constants - Settings
NUM_PATCHES = 64
NUM_GRIDLINES = 18 # 16=10, 64=18, 256=34


Point = namedtuple('Point', 'x y z')


def load_obj(file):
  """
  Takes an object file and creates a list of named tuples for every vertex

  :param file: path of object file to open
  :return: list of vertices
  """

  points = []
  i = 0
  found = False

  with open(file) as f:

    for line in f:
      if i % 1000000 == 0:
        print("Loading vertices -", int((i / 1000000) * 20), "%")
      i += 1

      line = line[:-1].split(' ')
      if line[0] == 'v':
        x, y, z = map(float, line[1:])
        points.append(Point(x, y, z))
        found = True
      elif found == True:
        break

  return points


def calc_corners(points):
  """
  Calculates vertices at corners of the object bounding box

  :param points: list of all vertices
  :return: list of the most extreme values of all the vertices
  """

  x_min = min(points, key=lambda point: point.x)
  x_max = max(points, key=lambda point: point.x)
  z_min = min(points, key=lambda point: point.z)
  z_max = max(points, key=lambda point: point.z)

  return [x_min.x, x_max.x, z_min.z, z_max.z]


def calc_gridlines(box, numGridlines):
  """
  Calculates x and z values of x and z lines which make up a 4x4 grid

  :param box: extreme values of the bounding box
  :param numGridlines: number of gridlines to calculate
  :return: list of values representing gridlines (length = numGridlines)
  """

  """ LINEAR CALCULATIONS
  # Initialise the grid with the edges defined
  grid = [None] * 10
  grid[0] = box[0]
  grid[4] = box[1] # 4 when 16 patches
  grid[5] = box[2] # 5 when 16 patches
  grid[9] = box[3] # 9 when 16 patches

  # Finds average of 2 gridlines to work out the gridline halfway between them
  # X gridlines
  grid[2] = (grid[4] + grid[0]) / 2
  grid[1] = (grid[2] + grid[0]) / 2
  grid[3] = (grid[4] + grid[2]) / 2

  # Y gridlines
  grid[7] = (grid[9] + grid[5]) / 2
  grid[6] = (grid[7] + grid[5]) / 2
  grid[8] = (grid[9] + grid[7]) / 2
  """

  halfGridlines = int(numGridlines / 2)

  # Initialise the grid with the edges defined
  grid = [None] * numGridlines
  grid[0] = box[0]
  grid[halfGridlines - 1] = box[1] # 4 when 16 patches
  grid[halfGridlines] = box[2] # 5 when 16 patches
  grid[numGridlines - 1] = box[3] # 9 when 16 patches


  # Finds average of 2 gridlines to work out the gridline halfway between them
  ## X Gridlines ##

  # Starts calculating from halfway point on x-axis
  xLine = int((numGridlines - 2) / 4)

  # Gridlines calculated in levels (halves the number of lines on one axis,
  # then halves again...). Level starts at halfway value and then halves once
  # all values on that level have been calculated.
  level = xLine

  # Number of last gridline on the x-axis is half the maximum number of
  # gridlines. -1 for list indexing
  xLastGridline = (halfGridlines) - 1

  # Loops over every X gridline until it has calculated the 2nd last gridline
  while(1):

    grid[xLine] = (grid[xLine + level] + grid[xLine - level]) / 2

    # If the last value in the level has been calculated, go down to the next
    # level
    if (xLine + level) >= xLastGridline:
      level = int(level / 2)

      # Set the gridline to the first gridline in the next level
      xLine = level
      
      # If the 2nd last X gridline has been calculated, end the loop
      if level < 1:
        break
    
    # If this value is not the last value on this level, set it as:
    # this value + last level number and don't change level
    else:
      xLine = xLine + (level * 2)

  
  ## Y Gridlines ##

  # Starts calculating from halfway point on y-axis
  yBuffer = (halfGridlines)
  yLine = yBuffer + int((numGridlines - 2) / 4)

  # Gridlines calculated in levels (halves the number of lines on one axis,
  # then halves again...). Level starts at halfway value and then halves once
  # all values on that level have been calculated.
  level = yLine - yBuffer

  # Number of last gridline on the y-axis is the maximum number of gridlines
  # -1 for list indexing
  yLastGridline = numGridlines - 1

  # Loops over every X gridline until it has calculated the 2nd last gridline
  while(1):

    grid[yLine] = (grid[yLine + level] + grid[yLine - level]) / 2

    # If the last value in the level has been calculated, go down to the next
    # level
    if (yLine + level) >= yLastGridline:
      level = int(level / 2)

      # Set the gridline to the first gridline in the next level + all the x
      # indexes
      yLine = level + yBuffer

      # If the 2nd last X gridline has been calculated, end the loop
      if level < 1:
        break
    
    # If this value is not the last value on this level, set it as:
    # this value + last level number and don't change level
    else:
      yLine = yLine + (level * 2)

  return grid


def calc_grid_height(points, grid, numPatches):
  """
  Calculates minimum and maximum heights within each grid boundary and then
  calculates difference between them

  :param points: list of all vertices
  :param grid: list of values representing gridlines (length = NUM_GRIDLINES)
  :param numPatches: number of patches being taken per image
  :return: list of each of the gridboxes difference in highest and lowest
    vertex points (length = NUM_PATCHES)
  """

  highest = [-10000.0] * numPatches
  lowest = [10000.0] * numPatches
  diff = [None] * numPatches

  print("Total number of vertices loaded:", len(points))
  
  # Adding number of vertices in each grid for debugging
  grid_totals = [0] * numPatches

  for i in range((len(points))-1):
    
    # Loading bar - 20% increments
    if i % 1000000 == 0:
      print(f"Processing vertices - {int((i / 1000000) * 20)} %")

    # Works out which grid box the point is in
    gridbox = locate_point(points[i], grid)

    # Adds 1 to the gridbox the current vertex is in
    grid_totals[gridbox] += 1

    # Checks if the y value is the highest or lowest point in the gridbox, if
    # it is, overwrite the current value of highest in that gridbox
    if points[i].y > highest[gridbox]:
      highest[gridbox] = points[i].y
    elif points [i].y < lowest[gridbox]:
      lowest[gridbox] = points[i].y

  # TEST - DEBUG
  print(f"Highest: {highest[0]} | Lowest: {lowest[0]}")

  # Calculates differnce between highest and lowest points in each gridbox
  for i in range(numPatches):
    difference = highest[i] - lowest[i]

    # Rounds to 3 d.p.
    diff[i] = round(difference, 3)

  # Prints number of vertices in each gridbox for debugging
  print(f"Grid Totals: {grid_totals}")

  return diff
    

def locate_point(vertex, grid):
  """
  Calculates which grid box the point is in

  :param vertex: point to locate
  :param grid: list of gridlines
  :return: grid box the point is located
  """

  numGridlines = len(grid)
  halfGridlines = int(numGridlines / 2)

  x_val = 0
  z_val = halfGridlines # Linear - 5 

  for i in range(halfGridlines - 1): # Linear - 4
    if vertex.x <= grid[i+1]: ##### < changed to <= #####
      x_val = i
      break
    #else ########## MAY NEED TO ERROR HANDLE HERE ###########

  for i in range(halfGridlines, numGridlines - 1): # Linear - 5 and 9
    if vertex.z <= grid[i+1]:
      z_val = i
      break

  # Finds the gridbox the x and z values correspond to (i.e. (x = 0, z = 9)
  # means top-left gridbox with an index value of 0 (bottom-right would be 15)
  # (left to right then top to bottom))
  gridbox = x_val + ((halfGridlines - 1) * (z_val - halfGridlines)) # 4 and 5

  return gridbox

def write_diffs_to_file(diffs, folderPath, loopNum):
  """
  Writes the difference values of 1 original image into a text file with each
  patch being on a new line

  :param diffs: list of height differences to write
  :param folderPath: path of folder where txt file to write heights is located
  :param loopNum: current iteration number
  """

  txtPath = folderPath + str(loopNum) + ".txt"

  file = open(txtPath, "w")
  
  # Writes each height difference label to a separate line (0 --> NUM_PATCHES)
  for i in range(len(diffs)):
    file.write(str(diffs[i]) + "\n")

  file.close()

  print(f"Generated labels for {loopNum}")

def calc_standard_deviation(points, grid, numPatches):
  """
  Calculates standard deviation of heights within each gridbox

  :param points: list of all vertices
  :param grid: list of values representing gridlines (length = NUM_GRIDLINES)
  :param numPatches: number of patches being taken per image
  :return: list of each of the gridboxes' standard deviation in height 
    (length = NUM_PATCHES)
  """

  print("Total number of vertices loaded:", len(points))

  # Adding number of vertices in each grid for debugging
  grid_totals = [0] * numPatches

  # Initialises a 2D array of {numPatches} lists of unknown length
  yValues = [[] for n in range(numPatches)]

  # Initialises a list of standard deviations for each patch
  stdDevPatch = [0.0] * numPatches

  # Iterates through every vertex in the terrain object
  for i in range((len(points))-1):

    # Loading bar - 20% increments
    if i % 1000000 == 0:
      print(f"Processing vertices - {int((i / 1000000) * 20)} %")

    # Works out which grid box the point is in
    gridbox = locate_point(points[i], grid)

    # Adds 1 to the gridbox the current vertex is in
    grid_totals[gridbox] += 1

    # Adding the y value of each point to a separate list for its gridbox
    yValues[gridbox].append(points[i].y)

  for i in range(numPatches):

    # Calculates standard deviation in height for each gridbox
    stdDev = np.std(yValues[i])

    # Rounds to 5 d.p.
    stdDevPatch[i] = round(stdDev, 5)

  # Prints number of vertices in each gridbox for debugging
  print(f"Grid Totals: {grid_totals}")

  return stdDevPatch


### MAIN ###
def main():

  # Loads all vertices into an array
  vertices = load_obj(INPUT_OBJ)

  # Calculates corners of bounding box
  box = calc_corners(vertices)

  # Calculates gridlines separating patches
  gridlines = calc_gridlines(box)

  height_diffs = calc_grid_height(vertices, gridlines, NUM_PATCHES)

  print(f"Height diffs: {height_diffs}")

  smoothest = [0, 10000] # Tuple of smoothest grid
  for i in range(len(height_diffs)):
    if height_diffs[i] < smoothest[1]:
      smoothest[0] = i
      smoothest[1] = height_diffs[i]

  print(f"Smoothest gridbox: {smoothest}")

  #labels = calc_standard_deviation(vertices, gridlines, NUM_PATCHES)

  #print(f"Standard deviation labels: {labels}")

  write_diffs_to_file(height_diffs, DIFFS_TXT_PATH, 100)

if __name__ == "__main__":
    main()