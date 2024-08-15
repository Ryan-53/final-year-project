import pandas as pd
from scipy.special import inv_boxcox
from sklearn.preprocessing import MinMaxScaler
from keras_preprocessing.image import ImageDataGenerator
from keras.models import load_model
import pickle
from tensorflow import keras

IMAGE_SIZE = 135
TRAINING_CSV = "source\\train.csv"
SCALER_PATH = "source\\final_scaler.pkl"

def predict_image(csvPath, patchPath, modelPath, lambdaTxtPath):
  """
  Predicts the smoothest patch from a set of 64 patches from a single image

  :param csvPath: path of csv to create
  :param patchPath: path of folder that the patches are stored in
  :param modelPath: path of model to use for prediction
  :param lambdaTxtPath: path of txt file storing the lambda value used in the
    box-cox transformation
  :return: lowestPredPatch - patch number of the patch that the model predicts 
    to be the smoothest
    lowestPred - predicted value of the smoothest patch
  """
  # Loads in patches into a dataset that can be fed into model
  dfPatch_original = pd.read_csv(csvPath)

  patchDatagen = ImageDataGenerator(
    # Normalises rgb values to 0-1
    rescale=1./255
  )

  patchGen = patchDatagen.flow_from_dataframe(
    dataframe=dfPatch_original,
    directory=patchPath,
    x_col="filename",
    y_col="label",
    batch_size=1,
    class_mode=None,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    shuffle=False,
    color_mode='grayscale'
  )

  # Loads in trained model
  model = load_model(modelPath)

  # Loads lambda value in
  txtFile = open(lambdaTxtPath, "r")
  lambda_ = float(txtFile.read())
  txtFile.close()

  # Loads Min-Max scaler used to scale training data
  with open(SCALER_PATH, 'rb') as scalerFile:
    scaler = pickle.load(scalerFile)

  # Predicts patches range values
  patchGen.reset()
  pred = model.predict(patchGen, steps=len(dfPatch_original))

  # Creates a new df with the raw predicted value of each patch
  dfPredictedPatch = pd.DataFrame({'id':dfPatch_original['id'],
                                   'label':dfPatch_original['label'],
                                   'filename':dfPatch_original['filename'],
                                   'pred':pred.flatten()})

  # Inverses the Min-Max normalisation
  predInverseScaled = scaler.inverse_transform(
    dfPredictedPatch['pred'].values.reshape(-1,1)
    )

  # Inverses the box-cox transformation
  predInverseTransformed = inv_boxcox(predInverseScaled.flatten(), lambda_)

  # Creates a new df with a column for the predicted value of each patch
  dfPatch = dfPredictedPatch.copy()
  dfPatch['pred'] = predInverseTransformed

  # Finds the patch number of the lowest predicted value
  lowestPredPatch = dfPatch['pred'].idxmin()

  lowestPred = round(float(dfPatch['pred'].min()), 2)

  return lowestPredPatch, lowestPred