import terragen_rpc as tg
import random

# Constants - Path to save image and project to
ROOT_FOLDER = "C:\\Users\\rgj\\OneDrive\\Desktop\\Uni Stuff\\Year 3\\ECM3401 \
- Literature Review and Final Project\\DL CV Model for Smoothness\\Dataset \
Generation\\Final_Rendering\\"
IMAGE_PATH = ROOT_FOLDER + "images\\mars_image_c.tif"
PROJECT_PATH = ROOT_FOLDER + "mars_terragen_final.tgd"

project = tg.root()

children = project.children()

def vary():
  pureVary = random.randint(-20,20)
  variation = pureVary/100
  varyMultiplier = 1 + variation

  return varyMultiplier


crater = [[0] * 3 for i in range(5)]
rock = [0] * 3

for i in children:

  path = i.path()

  if path == "/Fractal terrain 01":
    mainTerrain = i

  # Craters - Passes each crater and associated nodes as elements of a 2D list
  elif path == "/Crater shader_1":
    crater[0][0] = i
  elif path == "/Crater rocks shader_1":
    crater[0][1] = i
  elif path == "/Crater rock rough shader_1":
    crater[0][2] = i
  elif path == "/Crater shader_2":
    crater[1][0] = i
  elif path == "/Crater rocks shader_2":
    crater[1][1] = i
  elif path == "/Crater rock rough shader_2":
    crater[1][2] = i
  elif path == "/Crater shader_3":
    crater[2][0] = i
  elif path == "/Crater rocks shader_3":
    crater[2][1] = i
  elif path == "/Crater rock rough shader_3":
    crater[2][2] = i
  elif path == "/Crater shader_4":
    crater[3][0] = i
  elif path == "/Crater rocks shader_4":
    crater[3][1] = i
  elif path == "/Crater rock rough shader_4":
    crater[3][2] = i
  elif path == "/Crater shader_5":
    crater[4][0] = i
  elif path == "/Crater rocks shader_5":
    crater[4][1] = i
  elif path == "/Crater rock rough shader_5":
    crater[4][2] = i

  # Rocks - passes each rock node into a list (0 - largest, 2 - smallest)
  elif path == "/Large Rock shader":
    rock[0] = i
  elif path == "/Medium Rock shader":
    rock[1] = i
  elif path == "/Small Rock shader":
    rock[2] = i

  # Lighting
  elif path == "/Sunlight 01":
    sun = i

  # Camera
  elif path == "/Render Camera":
    camera = i

  # Renderer
  elif path == "/Render 01":
    render = i


# Debugging
#print(mainTerrain.path())
#print("Craters: ", crater)
#print(rock)

mainTerrain.set_param('seed', random.randint(1,99999))

# Randomises number of craters
numCraters = random.randint(0,5)

# Changes chance of no craters from 1/6 to 1/12
# If numCraters is 0, 50% chance of it being changed to 1
#if numCraters == 0:
#  if random.randint(0,1) == 0:
#    numCraters = 1

# Debugging
#numCraters = 0 # Test that removes all craters
#numCraters = 1 # Test
#print(numCraters)

# Resets all craters to not show
for i in range(5):
  crater[i][0].set_param('enable', 0)

# Use a function taking the objects of each crater and changing them within the func
for i in range(numCraters):

  # Sets random size of crater diameters, giving a 1/10 chance of having a large crater
  if random.randint(0,9) == 0:
    d = random.randint(1250,2500)
  else:
    d = random.randint(125,1250)


  ## Crater

  # Enabled?
  crater[i][0].set_param('enable', 1)

  # Location
  crater[i][0].set_param('center', (random.randint(-17500,-13500), 0, random.randint(-1875,1875)))

  # Diameter
  crater[i][0].set_param('diameter', d)

  # Depth
  crater[i][0].set_param('depth', (d/5) * vary())

  # Rim height
  crater[i][0].set_param('rim_height', (d/5) * vary())

  # Rim skirt
  crater[i][0].set_param('rim_skirt', (d/2) * vary())


  ## Rock 

  # Rock placement seed
  crater[i][1].set_param('seed', random.randint(1,99999))

  # Rock scale
  # Reducing rock size for larger craters
  d = d/2
  if d > 1250:
    d = d/4
  crater[i][1].set_param('stone_scale', (d/40) * vary())

  # Density seed
  crater[i][1].set_param('density_seed', random.randint(1,99999))

  ## Roughness

  # Roughness seed
  crater[i][2].set_param('seed', random.randint(1,99999))

  # Lead-in scale
  crater[i][2].set_param('lead-in_scale', (d/20) * vary())

  # Feature scale
  crater[i][2].set_param('feature_scale', (d/40) * vary())


## Rocks

for i in range(3):

  # Seed
  rock[i].set_param('seed', random.randint(1,99999))

  # Density seed
  rock[i].set_param('density_seed', random.randint(1,99999))

# Stone scale variation (only for large and medium rocks)
rock[0].set_param('stone_scale', int(50 * vary()))
rock[1].set_param('stone_scale', int(10 * vary()))


## Sun

# Elevation

# 1/4 chance of being abnormal angle
if random.randint(0,3) == 0:

  # 3/1 chance of being low
  if random.randint(0,2) == 0:

    # Low
    # 1/4 chance of Extra Low
    # Extra Low
    if random.randint(0,3) == 0:
      elev = (float(random.randint(75,150)))/10

    # Normal Low
    else:
      elev = (float(random.randint(150,200)))/10
      
  # High
  else:
    #1/4 chance of Extra high
    # Extra High
    if random.randint(0,3) == 0:
      elev = (float(random.randint(650,850)))/10

    # Normal High
    else:
      elev = (float(random.randint(400,650)))/10

else:
  elev = (float(random.randint(200,400)))/10

sun.set_param('elevation', elev)


# Heading
head = random.randint(0,360)
sun.set_param('heading', head)


## Camera

# Height
height = random.randint(2250,2750)
camera.set_param('position', (-15000, height, 0))

# Rotation

# 1/4 chance of a large swing
if random.randint(0,3) == 0:
  
  # Each extraneous side

  # Large swing Backwards
  if random.randint(0,1) == 0:
    rotat = random.randint(-850,-800)
  
  # Large swing Forwards
  else:
    rotat = random.randint(-1000,-950)

else:
  rotat = random.randint(-950,-850)

# Sets the rotation to be to 1 d.p.
rotat = (float(rotat)) / 10

# Randomises y axis to decrease chance of systematic biases of camera being along an axis having any affect
yAxis = random.randint(0,360)

camera.set_param('rotation', (rotat, 0, 0))



## Render

# Change filenames of output files
render.set_param('output_image_filename', (IMAGE_PATH))


## Saving

tg.save_project(PROJECT_PATH)

print("Saved project")



