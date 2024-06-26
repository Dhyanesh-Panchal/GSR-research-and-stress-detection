# %%
import pandas as pd
import numpy as np
import os
from eda_helper import Processing

from tensorflow.keras.models import load_model
from tensorflow import keras
from neurokit2 import eda_process

# %%
# LSTM model class
class LSTM_Phasic:
    def __init__(self):
        self.model = None
        self.model_weights_path = './models/LSTM_Phasic_window_mixed_p5.h5'
        self.model = self.load_model()
        self.input_shape = (100, 1)
        self.model = keras.Sequential()
        self.model.add(keras.layers.LSTM(64, input_shape=self.input_shape, return_sequences=True))
        self.model.add(keras.layers.LSTM(64))
        self.model.add(keras.layers.Dense(128, activation="relu"))
        self.model.add(keras.layers.Dropout(0.2))
        self.model.add(keras.layers.Dense(64, activation="relu"))
        self.model.add(keras.layers.Dropout(0.3))
        self.model.add(keras.layers.Dense(2, activation="softmax"))
        self.model.load_weights(self.model_weights_path)


    def predict(self, X):
        # Predict probabilities
        probabilities = self.model.predict(X)

        # Convert probabilities to class labels
        predictions = (probabilities > 0.5).astype(int)
        # Convert predictions array to binary format
        # Use the first column of predictions array to represent 'H'
        predictions_binary = predictions[:, 0]
        return predictions_binary
# %%
# Data preparation class
class Prepare_Data:
    def __init__(self):
        self.processing = Processing()
        self.window_size = 100
        self.window_gap = 1

    def preprocess_sensor_data(self,source_data_fp: str):
        # conversion equation
        def convert_eq(x):
            resistance = (1400 + 2 * x) * 10000 / (700 - x)
            # resistance = (x*(5.0/1023.0))*0.2
            if not resistance:
                print(x)
            return (1 / resistance) * 10**6

        file_name = os.path.basename(source_data_fp)
        print(file_name)
        data = pd.read_csv(source_data_fp)
        # Filter Shorted Conditions(Values >600)
        data = data[data["GSR"] < 600]
        data = data[::100]
        data["skin_resistance"] = data["GSR"].apply(convert_eq)
        # data.to_csv(os.path.join(destination_folder, file_name), index=False)

        processed_data = eda_process(
            data["skin_resistance"], sampling_rate=20, method="neurokit"
        )[0]

        # Prepare for model
        phasic_windowed = self.processing.generate_windows_df(processed_data, window_size=self.window_size, window_gap=self.window_gap, column_name="EDA_Phasic")
        X = np.array(phasic_windowed).reshape(len(phasic_windowed),100,1)
        
        return X
 
# %%
