import pandas as pd
import os 

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TEST2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TEST2\\"

FILES_ARRAY = [
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-90BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.3716, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-90BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-130BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.9812, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-130BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-MED-90BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.114425, "destinationFileName": "PROC-TEST2-STEPS-LR-MED-90BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-MED-100BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.23825, "destinationFileName": "PROC-TEST2-STEPS-LR-MED-100BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-MED-130BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.609725, "destinationFileName": "PROC-TEST2-STEPS-LR-MED-130BPM.xlsx" },
]

for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]

    # Read the Excel file
    df = pd.read_csv(file_path)

    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']   

    # Update the columns based on 'Notes1' values
    df.loc[df['Notes1'] == 'STANDING_A', ['X_Vel', 'Z_Vel', 'Notes1']] = [0, 0, 'STANDING']
    df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel"], fileConfig["Z_Vel"]]   


    # save the modified csv to a spreadsheet
    destination_path = DESTINATION_FOLDER_PATH + fileConfig["destinationFileName"]
    df.to_excel(destination_path, index=False)    
