import pandas as pd

SOURCE_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"

FILES_ARRAY = [
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-60BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.91, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-60BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-80BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.22, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-80BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-100BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.52, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-100BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-110BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.68, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-110BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-MED-60BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.51, "destinationFileName": "PROC-TRAIN2-STEPS-LR-MED-60BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-MED-80BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.68, "destinationFileName": "PROC-TRAIN2-STEPS-LR-MED-80BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-MED-100BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.85, "destinationFileName": "PROC-TRAIN2-STEPS-LR-MED-100BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-MED-110BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.93, "destinationFileName": "PROC-TRAIN2-STEPS-LR-MED-110BPM.xlsx" },
]

for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]

    # Read the Excel file
    df = pd.read_csv(file_path)

    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']   

    # Update the columns based on 'Notes1' values
    df.loc[df['Notes1'] == 'STANDING', ['X_Vel', 'Z_Vel']] = 0
    df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel"], fileConfig["Z_Vel"]]   


    # save the modified csv to a spreadsheet
    destination_path = DESTINATION_FOLDER_PATH + fileConfig["destinationFileName"]
    df.to_excel(destination_path, index=False)    
