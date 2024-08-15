import csv

PATCH_FOLDER = "patches"
CSV_PATH = "bin\\patch.csv"

def write_csv(csvPath, patchPath):
  """
  Creates a csv file with the filenames of the patches of the input image

  :param csvPath: path of csv to create
  :param patchPath: path of folder that the patches are stored in
  """

  with open(csvPath, 'w', newline='') as csvFile:
    
    writer = csv.writer(csvFile)
    header = ["id", "label", "filename"]

    writer.writerow(header)

    # Loops through all patches
    for i in range(64):

      filename = f"{i}.jpg"

      writer.writerow([i, "0", filename])

def main():
  
  write_csv(CSV_PATH, PATCH_FOLDER)

if __name__ == "__main__":

  main()