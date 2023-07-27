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

def normalize_sensor_data(sensor_input):
    return (sensor_input + 180)/360