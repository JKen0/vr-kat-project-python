import os
import pandas as pd
import numpy as np


# FETCH ALL DATA
PROCESS_TRAIN2_FOLDER = "C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA\TRAIN2\\"
ALL_FILE_NAMES = [file for file in os.listdir(PROCESS_TRAIN2_FOLDER) if file.endswith('.xlsx') and "AUGMENT" not in file and "STAND" not in file]



#  HEELPER FUNCTION 
def listToString(s, joinElement = ''):
 
    # initialize an empty string
    str1 = ""
 
    # traverse in the string
    for ele in s:
        if str1 == "":
            str1 += ele
        else:
            str1 += joinElement + ele
 
    # return string
    return str1



# LOOP THROUGH EACH FILE
# THIS WILL TAKE EVERY OTHER SENSOR DATA (THIS WILL HALF CYCLE TIME, DOUBLE SPEED, DOUBLE BPM)
for fileName in ALL_FILE_NAMES:
    fileNameSplit = fileName.split("-")
    getBPM = numeric_part = ''.join(filter(str.isdigit, fileNameSplit[-1]))

    newBPM = 2*int(getBPM)

    # Read the Excel file
    df = pd.read_excel(PROCESS_TRAIN2_FOLDER + fileName)

    # identify standing rows
    standingRows = df[df['Notes1'] == 'STANDING']

    # Identify the "MOTION_A" rows
    motionDataRows = df[df['Notes1'] == 'MOTION_A']

    # split the motionn data rows 
    evenRows = motionDataRows.iloc[0::2]
    oddRows = motionDataRows.iloc[1::2]

    # combined augmented data
    augmentedData = pd.concat([standingRows, evenRows, oddRows])
    # replace iteration with index
    augmentedData['Iteration'] = range(len(df))
    # replace new velocities
    augmentedData['X_Vel'] = 2*augmentedData['X_Vel']
    augmentedData['Z_Vel'] = 2*augmentedData['Z_Vel']

    #update classification class to the new BPM
    augmentedData['Classification'] = listToString(fileNameSplit[2:-1:2] + ['' + str(newBPM) + 'BPM'], '-')

    #create new filename
    arrayAugmentFileName = fileNameSplit[:-1] + ['' + str(newBPM) + 'BPM-AUGMENT.xlsx']
    stringAugmentFileName = listToString(arrayAugmentFileName, '-')

    #save file 
    augmentedData.to_excel(PROCESS_TRAIN2_FOLDER + stringAugmentFileName, index=False)




# LOOP THROUGH EACH FILE
# THIS WILL TAKE EVERY OTHER SENSOR DATA (THIS WILL HALF CYCLE TIME, DOUBLE HALF, HALF BPM)
# METHOD: INTERPOLATION 
for fileName in ALL_FILE_NAMES:
    fileNameSplit = fileName.split("-")
    getBPM = numeric_part = ''.join(filter(str.isdigit, fileNameSplit[-1]))

    newBPM = int(1/2*int(getBPM))

    # Read the Excel file
    df = pd.read_excel(PROCESS_TRAIN2_FOLDER + fileName)

    # identify standing rows
    standingRows = df[df['Notes1'] == 'STANDING']

    # Identify the "MOTION_A" rows
    motionDataRows = df[df['Notes1'] == 'MOTION_A']

    # new dataframe for interpolated rows
    interpolatedDF = pd.DataFrame(columns=df.columns)

    # Iterate over each pair of consecutive rows
    for i in range(len(motionDataRows)-1):
        row1 = motionDataRows.iloc[i]  # Current row
        row2 = motionDataRows.iloc[i+1]  # Next row
        
        interpolatedRow = row1.copy()  # Create a copy of the row

        interpolatedRow['Iteration'] = (row1['Iteration'] + row2['Iteration']) / 2
        interpolatedRow['L_Pitch'] = int((row1['L_Pitch'] + row2['L_Pitch']) / 2)
        interpolatedRow['L_Roll'] = int((row1['L_Roll'] + row2['L_Roll']) / 2)
        interpolatedRow['R_Pitch'] = int((row1['R_Pitch'] + row2['R_Pitch']) / 2)
        interpolatedRow['R_Roll'] = int((row1['R_Roll'] + row2['R_Roll']) / 2)

        interpolatedDF = pd.concat([interpolatedDF, row1.to_frame().T, interpolatedRow.to_frame().T])

    # Append the last row from the original DataFrame
    interpolatedDF = pd.concat([interpolatedDF, motionDataRows.iloc[-1].to_frame().T])

    # combined augmented data
    augmentedData = pd.concat([standingRows, interpolatedDF])

    # replace new velocities
    augmentedData['X_Vel'] = 1/2*augmentedData['X_Vel']
    augmentedData['Z_Vel'] = 1/2*augmentedData['Z_Vel']

    #update classification class to the new BPM
    augmentedData['Classification'] = listToString(fileNameSplit[2:-1:2] + ['' + str(newBPM) + 'BPM'], '-')


    #create new filename
    arrayAugmentFileName = fileNameSplit[:-1] + ['' + str(newBPM) + 'BPM-AUGMENT.xlsx']
    stringAugmentFileName = listToString(arrayAugmentFileName, '-')

    #save file 
    augmentedData.to_excel(PROCESS_TRAIN2_FOLDER + stringAugmentFileName, index=False)






