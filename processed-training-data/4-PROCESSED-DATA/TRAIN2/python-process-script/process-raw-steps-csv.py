import pandas as pd
import os 

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"
UPPER_BOUND_SLOW_BPM = 61
UPPER_BOUND_MEDIUM_BPM = 101

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

def getClassificationSpeed(bpm):
    if(bpm < UPPER_BOUND_SLOW_BPM ):
        return 'SLOW'
    elif( bpm < UPPER_BOUND_MEDIUM_BPM):
        return 'AVERAGE'
    else:
        return 'FAST'


for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]

    fileNameSplit = fileConfig["fileName"].split("-")
    getBPM = ''.join(filter(str.isdigit, fileNameSplit[-1]))
    getBPM = float(getBPM)

    classificationMotion = fileNameSplit[2]
    classificationMotionType = fileNameSplit[4]
    classificationMotionSpeed = getClassificationSpeed(getBPM)

    # Read the Excel file
    df = pd.read_csv(file_path)

    df['L_Pitch_Delta'] = df['L_Pitch'].diff()
    df['L_Roll_Delta'] = df['L_Roll'].diff()
    df['R_Pitch_Delta'] = df['R_Pitch'].diff()
    df['R_Roll_Delta'] = df['R_Roll'].diff()

    # Exclude rows where 'Notes1' is equal to 'CUTOFF'
    df = df[df['Notes1'] != 'CUTOFF']  

    # Update the columns based on 'Notes1' values
    df.loc[df['Notes1'] == 'STANDING', ['X_Vel', 'Z_Vel']] = [0, 0]
    df.loc[df['Notes1'] == 'STANDING', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['STAND', 'SML', 'SLOW']
    

    df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel"], fileConfig["Z_Vel"]]  
    df.loc[df['Notes1'] == 'MOTION_A', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = [classificationMotion, classificationMotionType, classificationMotionSpeed] 

    # save the modified csv to a spreadsheet
    destination_path = DESTINATION_FOLDER_PATH + fileConfig["destinationFileName"]
    df.to_excel(destination_path, index=False)    
