# %%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from LSTM_on_Collected_data import LSTM_Phasic, Prepare_Data
# from read_gsr import main
# %%

# # Collect Data
# data_file_path = main()

data_file_path = "./Collected_Data/Horror_Srushti.csv"

# %%
# Prepare Data
prepare_data = Prepare_Data()
X = prepare_data.preprocess_sensor_data(data_file_path)

# %%
# Load Model
lstm = LSTM_Phasic()


# Predict
predictions = lstm.predict(X)

# %%
# Generate Graphs
print(predictions)

# histogram
plt.figure(figsize = (10,2))
plt.bar(x=np.arange(len(predictions)),height=predictions)
plt.title("Arousal Histogram")
plt.show()
