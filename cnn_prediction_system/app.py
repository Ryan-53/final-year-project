import tkinter as tk
from tkinter import filedialog
import cv2
import os
from img_handler import crop_image, draw_rect
from model_handler import predict_image

SOURCE = "main_image"
MAIN_IMAGE_PATH = os.path.join(SOURCE, "full_image.jpg")
PATCH_FOLDER = "patches"
CSV_PATH = "bin\\patch.csv"
MODEL_PATH = "source\\Final_greyscale_model_compat_mode.h5"
LAMBDA_TXT_PATH = "source\\final_lambda.txt"
SAVE_PREDICTED_PATH = "saved_predictions\\predicted_image.jpg"

def imageUploader():
  """
  DESCRIBE THIS
  """
  # Provides function for when button is pressed
  # A file chooser is opened with only image files being allowed to be selected
  fileTypes= [("Image files", "*.png;*.jpg;*.jpeg")]
  inputMainImgPath = tk.filedialog.askopenfilename(filetypes=fileTypes)

  # If file is selected
  if len(inputMainImgPath):

    # Format path so it can be used in python
    mainImgPath = (str(inputMainImgPath)).replace("/", "\\")    

    # Copy Image to application source files
    os.system(f'copy "{mainImgPath}" "{MAIN_IMAGE_PATH}"')
    print(f"Image copied from {mainImgPath} to {MAIN_IMAGE_PATH}")

    # Crops image into patches and saves them into application source files
    crop_image(MAIN_IMAGE_PATH, PATCH_FOLDER)

    # Model used to predict the safest LS
    selectedPatch, predictionValue = predict_image(CSV_PATH, PATCH_FOLDER, MODEL_PATH, LAMBDA_TXT_PATH)

    # Draws a rectangle around patch selected by model
    procImg = draw_rect(selectedPatch)

    # Loads and saves image with highlighted patch
    img = cv2.resize(procImg, (1080, 1080))
    cv2.imwrite(SAVE_PREDICTED_PATH, img)
    print("Saved predicted image")
    print("Displaying predicted image")

    # Displays image with highlighted patch
    cv2.imshow("Patches", img)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # Update text with predicted value
    textDisplay.config(state=tk.NORMAL)
    textDisplay.delete("1.0", tk.END)  # Clear existing text
    textDisplay.insert(tk.END, f"Predicted smoothness value of highlighted patch:\n(predicted vertical range of terrain)\n[lower=smoother]\n\n{predictionValue}")
    textDisplay.config(state=tk.DISABLED)
    
    # Centering the text
    textDisplay.tag_configure("center", justify='center')
    textDisplay.tag_add("center", "1.0", "end")
    
 
  # If no file is selected
  else:
    print("No file is Choosen! Please choose a file.")

if __name__ == "__main__":
  
  # Defines tkinter object
  app = tk.Tk()
  app.title("CNN Surface Smoothness Image Predictor")
  app.geometry("700x350")
  app.tk.call('tk', 'scaling', 3.0)

  # Defines image chooser button
  app.option_add("*Button*Background", "lightblue")
  uploadButton = tk.Button(app, text="Upload Image to Model", command=imageUploader)
  uploadButton.pack(side=tk.TOP, pady=20)

  # Defines text boxes
  textDisplay = tk.Text(app, height=10, width=50, 
                        bg=app.cget("bg"), bd=0, highlightthickness=0,
                        font=("Helvetica", 9)
                        )
  textDisplay.pack(side=tk.BOTTOM, pady=20)


  # Displays text in text box
  textDisplay.insert(tk.END, "No image selected")
  textDisplay.config(state=tk.DISABLED)

  # Centering the text
  textDisplay.tag_configure("center", justify='center')
  textDisplay.tag_add("center", "1.0", "end")

  # Runs the app in a window
  app.mainloop()