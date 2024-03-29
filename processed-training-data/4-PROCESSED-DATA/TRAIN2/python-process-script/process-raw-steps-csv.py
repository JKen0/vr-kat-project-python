import pandas as pd
import os 
import json 

# Get the current working directory
CURRENT_DIRECTORY = os.getcwd()

# Open the config file and load its content into a dictionary
config_file = open(CURRENT_DIRECTORY + '\\config\\config.json')
CONFIG_DATA = json.load(config_file)

# Close the file after loading the data
config_file.close()

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TRAIN2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"

FILES_ARRAY = [
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-60BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.91, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-60BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-80BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.22, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-80BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-100BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.52, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-100BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-110BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.68, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-110BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-62BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.51, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-62BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-82BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.68, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-82BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-98BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.85, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-98BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-LAR-112BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.93, "destinationFileName": "PROC-TRAIN2-STEPS-LR-LAR-112BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-SML-60BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.68, "destinationFileName": "PROC-TRAIN2-STEPS-LR-SML-60BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-SML-80BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.85, "destinationFileName": "PROC-TRAIN2-STEPS-LR-SML-80BPM.xlsx" },
    {"fileName": "RAW-TRAIN2-STEPS-LR-SML-110BPM.csv", "X_Vel": 0.0 , "Z_Vel": 0.93, "destinationFileName": "PROC-TRAIN2-STEPS-LR-SML-110BPM.xlsx" },
]

def getClassificationSpeed(bpm, upper_bound_slow, upper_bound_average):
    if(bpm < upper_bound_slow ):
        return 'SLOW'
    elif( bpm < upper_bound_average):
        return 'AVERAGE'
    else:
        return 'FAST'


for fileConfig in FILES_ARRAY:
    file_path = SOURCE_FOLDER_PATH + fileConfig["fileName"]

    fileNameSplit = fileConfig["fileName"].split("-")
    getBPM = ''.join(filter(str.isdigit, fileNameSplit[-1]))
    getBPM = float(getBPM)

    # calculae the classification classes
    classificationMotion = fileNameSplit[2]
    classificationMotionType = fileNameSplit[4]

    UPPER_BOUND_SLOW_BPM = CONFIG_DATA[classificationMotionType + '_' + classificationMotion + '_UPPER_BOUND_SLOW_BPM']
    UPPER_BOUND_MEDIUM_BPM = CONFIG_DATA[classificationMotionType + '_' + classificationMotion + '_UPPER_BOUND_AVERAGE_BPM']

    classificationMotionSpeed = getClassificationSpeed(getBPM, UPPER_BOUND_SLOW_BPM, UPPER_BOUND_MEDIUM_BPM)

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
