import numpy as np
import pandas as pd
from tqdm.notebook import tqdm as bar


class Processing:

    # Normalization functions

    @staticmethod
    def maximum_absolute_scaling(data: pd.DataFrame, colum_names):
        for colum_name in colum_names:
            # shift the data to zero mean
            data[colum_name] = data[colum_name] - np.mean(data[colum_name])
            # divide by max +ve value present to get in range [-1,1]
            print(np.max(data[colum_name].abs()))
            data[colum_name] = data[colum_name] / \
                np.max(np.absolute(data[colum_name]))

        return data

    # For windowing the Dataframe

    @staticmethod
    def generate_windows_df(df: pd.DataFrame, window_size: int, window_gap: int, column_name: str):
        def rolling_window(df: pd.DataFrame, window_size: int, window_gap: int):
            windows = []
            for i in bar(range(0, len(df)-window_size+1, window_gap), desc="generating window"):
                single_window = df.iloc[i:i+window_size]
                # print(single_window)
                windows.append(single_window)
            return windows

        if window_size < len(df):
            windowed_data = rolling_window(
                df, window_size, window_gap)
            array = []
            for frame in bar(windowed_data, desc="preparing dataframe"):
                array.append(list(frame[column_name]))

            window_df = pd.DataFrame(np.array(array))
        else:
            return df
        return window_df
