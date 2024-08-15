import pandas as pd
from scipy.special import boxcox
from sklearn.preprocessing import MinMaxScaler
import math

NUM_PATCHES = 64
TRAINING_CSV = "source\\train.csv"

def initialise_scales(lambda_):
  """
  Scales data exactly as it was in training, so the predictions from the model
  in the program can be scaled to native domain

  :param lambda_: lambda value used to transform via box-cox 
  :return: scaler used to scale data
    lambda value used in box-cox transformation
  """

  # Loading in dataframe used in training
  df = pd.read_csv(TRAINING_CSV)

  ## Preprocessing dataframe
  ## Dropping rows with erroneous labels and ALL corner patches
  # Patches with no vertices
  df = df.drop(df[df["label"] == -20000.000].index)
  # Patches with 1 vertex
  df = df.drop(df[df["label"] == 0.0].index)
  # Patches with negative value labels
  df = df.drop(df[df["label"] < 0.0].index)

  ## Drop Corner patches
  # Top-Left
  df = df.drop(df[df["id"] % NUM_PATCHES == 0].index) # If patchNum = 0
  # Top-Right
  df = df.drop(df[(df["id"] - (math.sqrt(NUM_PATCHES) - 1)) % NUM_PATCHES == 0].index) # If patchNum = 7
  # Bottom-Left
  df = df.drop(df[(df["id"] + math.sqrt(NUM_PATCHES)) % NUM_PATCHES == 0].index) # If patchNum = 56
  # Bottom-Right
  df = df.drop(df[(df["id"] + 1) % NUM_PATCHES == 0].index) # If patchNum == 63


  ## Normalising using Box-Cox
  dfNorm = df.copy()
  labelsArr = dfNorm['label']

  transformedLabels, lm = boxcox(labelsArr)

  scaler = MinMaxScaler()

  labelsScaled = scaler.fit_transform(transformedLabels.reshape(-1,1))

  dfNorm['label'] = labelsScaled.flatten()

  return scaler, lm

