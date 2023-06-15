import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import plot_model

data_folder = 'C:\Dev\\vr-kat-project-python-2\processed-training-data\\4-PROCESSED-DATA'  # Specify the path to your data folder

file_names = [file for file in os.listdir(data_folder) if file.endswith('.xlsx') and os.path.isfile(os.path.join(data_folder, file))]

dataframes = []

for file_name in file_names:
    file_path = os.path.join(data_folder, file_name)
    df = pd.read_excel(file_path)  # Load each Excel file
    dataframes.append(df)

combined_df = pd.concat(dataframes)  # Combine the datasets into a single DataFrame

# Split the data into input (sensor data) and output (velocity)
INPUT_DATA = combined_df[['L_Roll', 'L_Pitch', 'R_Roll', 'L_Pitch']].values
OUTPUT_DATA = combined_df[['X_Vel', 'Z_Vel']].values

# Reshape the input data
NUMBER_TIMESTEPS = 10
NUMBER_FEATURES = 4
NUMBER_SAMPLES = X.shape[0] - NUMBER_TIMESTEPS + 1

input_Reshaped = np.zeros((NUMBER_TIMESTEPS, NUMBER_TIMESTEPS, NUMBER_FEATURES))

for i in range(NUMBER_TIMESTEPS):
    input_Reshaped[i] = INPUT_DATA[i:i+NUMBER_TIMESTEPS, :]

# Remove extra samples from y
y_Reformatted = OUTPUT_DATA[NUMBER_TIMESTEPS-1:]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(input_Reshaped, y_Reformatted, test_size=0.2, random_state=42)

# Define and train the RNN model
model = Sequential()
model.add(LSTM(units=40, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dense(units=2))  # Output layer with 2 units for 2 output values

model.compile(optimizer='adam', loss='mse')  # Configure the model

model.fit(X_train, y_train, epochs=10, batch_size=32)  # Train the model

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print("Test Loss:", loss)

# Make predictions
predictions = model.predict(X_test)

# Save the model
model.save('test-model.h5')