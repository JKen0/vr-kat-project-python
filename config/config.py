# config.py
import numpy as np
import os 
import json 

def count_sequences_above_threshold(data, threshold):
    num_sensors = data.shape[1]
    counts = np.zeros(num_sensors, dtype=int)

    for sensor_index in range(num_sensors):
        count = 0
        sequence_above_threshold = False

        for value in data[:, sensor_index]:
            if value > threshold:
                if not sequence_above_threshold:
                    count += 1
                    sequence_above_threshold = True
            else:
                sequence_above_threshold = False

        counts[sensor_index] = count

    return counts

def count_sequences_below_threshold(data, threshold):
    num_sensors = data.shape[1]
    counts = np.zeros(num_sensors, dtype=int)

    for sensor_index in range(num_sensors):
        count = 0
        sequence_above_threshold = False

        for value in data[:, sensor_index]:
            if value > threshold:
                if not sequence_above_threshold:
                    count += 1
                    sequence_above_threshold = True
            else:
                sequence_above_threshold = False

        counts[sensor_index] = count

    return counts

def normalize_sensor_data(sensor_input):
    return (sensor_input + 180)/360


def getClassificationSpeed(bpm, upper_bound_slow, upper_bound_average):
    if(bpm < upper_bound_slow ):
        return 'SLOW'
    elif( bpm < upper_bound_average):
        return 'AVERAGE'
    else:
        return 'FAST'
    
def calculateSensorDeltas(sensor_data):
    return np.diff(sensor_data, axis=0)

def calculateAbsSensorDeltas(delta_data):
    abs_delta_data = np.abs(delta_data)

    total_deltas_changes = np.sum(abs_delta_data, axis=0)

    return total_deltas_changes

def calculateMaxSensorData(sensor_data):
    return np.max(sensor_data, axis=0)

def calculateMinSensorData(sensor_data):
    return np.min(sensor_data, axis=0)

def prediction_class_label(prediction_prob, ALL_CLASSES):
    pred_class_index = np.argmax(prediction_prob, axis=-1) 

    pred_class_label = ALL_CLASSES[pred_class_index[0]]

    return pred_class_label

def prediction_class_label_binary(prediction_prob, ALL_CLASSES):
    prediction_class_int = int(np.rint(prediction_prob))

    pred_class_label = ALL_CLASSES[prediction_class_int]

    return pred_class_label

def processStepsMotionSpeed(sensor_data, total_deltas_data, threshold):

    input_total_sequences = count_sequences_above_threshold(sensor_data, threshold)
    input_total_sequences = np.reshape(input_total_sequences, (1,4))

    input_data_array = np.column_stack((total_deltas_data, input_total_sequences))

    # SUM THE TOTAL PITCH DELTAS
    SUM_SENSOR_DELTAS = np.sum(input_data_array[:, [0,2]], axis=1)

    # SUM THE TOTAL NUMBER OF SEQUENCES
    SUM_SEQUENCES = np.sum(input_data_array[:, [4, 6]], axis=1)

    return np.column_stack((SUM_SENSOR_DELTAS, SUM_SEQUENCES))

def processLSideStepsMotionSpeed(sensor_data, total_deltas_data, threshold):

    input_total_sequences = count_sequences_below_threshold(sensor_data, threshold)
    input_total_sequences = np.reshape(input_total_sequences, (1,4))

    input_data_array = np.column_stack((total_deltas_data, input_total_sequences))

    extracted_results = input_data_array[:, [1,5]]

    return extracted_results

def processRSideStepsMotionSpeed(sensor_data, total_deltas_data, threshold):
    
    input_total_sequences = count_sequences_below_threshold(sensor_data, threshold)
    input_total_sequences = np.reshape(input_total_sequences, (1,4))

    input_data_array = np.column_stack((total_deltas_data, input_total_sequences))

    extracted_results = input_data_array[:, [3,7]]

    return extracted_results