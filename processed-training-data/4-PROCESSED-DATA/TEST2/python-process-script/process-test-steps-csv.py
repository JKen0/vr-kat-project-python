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

SOURCE_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\1-RAW-CSV\TEST2\\"
DESTINATION_FOLDER_PATH = CURRENT_DIRECTORY + "\\processed-training-data\\4-PROCESSED-DATA\TEST2\\"

# define BPM bounds between classes
UPPER_BOUND_SLOW_BPM = CONFIG_DATA['STEPS_UPPER_BOUND_SLOW_BPM']
UPPER_BOUND_MEDIUM_BPM = CONFIG_DATA['STEPS_UPPER_BOUND_AVERAGE_BPM']

FILES_ARRAY = [
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-90BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.3716, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-90BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-130BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.9812, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-130BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-92BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.114425, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-92BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-98BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.23825, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-98BPM.xlsx" },
    {"fileName": "RAW-TEST2-STEPS-LR-LAR-132BPM.csv", "X_Vel": 0.0 , "Z_Vel": 1.609725, "destinationFileName": "PROC-TEST2-STEPS-LR-LAR-132BPM.xlsx" },
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
    df.loc[df['Notes1'] == 'STANDING_A', ['X_Vel', 'Z_Vel', 'Notes1']] = [0, 0, 'STANDING']
    df.loc[df['Notes1'] == 'STANDING_A', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = ['STAND', 'SML', 'SLOW']

    df.loc[df['Notes1'] == 'MOTION_A', ['X_Vel', 'Z_Vel']] = [fileConfig["X_Vel"], fileConfig["Z_Vel"]]   
    df.loc[df['Notes1'] == 'MOTION_A', ['Class_Motion', 'Class_MotionType', 'Class_MotionSpeed']] = [classificationMotion, classificationMotionType, classificationMotionSpeed] 


    # save the modified csv to a spreadsheet
    destination_path = DESTINATION_FOLDER_PATH + fileConfig["destinationFileName"]
    df.to_excel(destination_path, index=False)    
