import numpy as np
import pandas as pd
from tqdm.notebook import tqdm as tqdm


class Processing:

    # Normalization functions

    @staticmethod
    def maximum_absolute_scaling(data: pd.DataFrame, colum_names):
        for colum_name in tqdm(colum_names, desc="Scaling column values"):
            # shift the data to zero mean
            data[colum_name] = data[colum_name] - np.mean(data[colum_name])
            # divide by max +ve value present to get in range [-1,1]
            # print(np.max(data[colum_name].abs()))
            data[colum_name] = data[colum_name] / \
                np.max(np.absolute(data[colum_name]))

        return data

    # For windowing the Dataframe

    @staticmethod
    def generate_windows_df(df: pd.DataFrame, window_size: int, window_gap: int, column_name: str):
        def rolling_window(df: pd.DataFrame, window_size: int, window_gap: int):
            windows = []
            for i in tqdm(range(0, len(df)-window_size+1, window_gap), desc="generating window"):
                single_window = df.iloc[i:i+window_size]
                # print(single_window)
                windows.append(single_window)
            return windows

        if window_size < len(df):
            windowed_data = rolling_window(
                df, window_size, window_gap)
            array = []
            for frame in tqdm(windowed_data, desc="preparing dataframe"):
                array.append(list(frame[column_name]))

            window_df = pd.DataFrame(np.array(array))
        else:
            return df
        return window_df

    
    @staticmethod
    def prepare_data(subject_ID):
        def _pre_process(df: pd.DataFrame):
            phasic_windowed = Processing.generate_windows_df(df, window_size=100, window_gap=1, column_name="EDA_Phasic")

            X = np.array(phasic_windowed).reshape(len(phasic_windowed),100,1)
            # inserted the initial arousal value during the "start" of window
            # X = np.concatenate((X,np.array(df['class_2_arousal'][99:]).reshape(len(df['class_2_arousal']) - 99,1,1)) , axis=1)

            y = np.array(df["class_2_arousal"])[99:]

            return X,y
        data_df = pd.read_csv(f"https://raw.githubusercontent.com/Dhyanesh-Panchal/GSR-research-and-stress-detection/master/preprocessed_data/sub_{subject_ID}.csv").drop("Unnamed: 0",axis=1)
        data_df = data_df[data_df["video"].isin([5,6,7,8])]
        filtered_data = data_df[(data_df["arousal"]!=5) & (data_df["valence"]!=5)]
        filtered_data = filtered_data.reset_index().drop("index",axis=1)
        X,y = _pre_process(filtered_data)
        y = pd.get_dummies(y)
        return X,y

    @staticmethod
    def prepare_windows_with_labels(
        data,
        x_column="EDA_Phasic",
        y_columns=["arousal", "valence"],
        y_aggregator = "mean",
        window_size=100,
        window_gap=1,
    ):
        '''
        
        '''
        # prepare the x column
        x_df = Processing.generate_windows_df(data, window_size, window_gap, x_column)
        
        # prepare the y columns
        y_dfs = []
        for y_column in tqdm(y_columns, desc="Preparing Y Columns:"):
            y_df = Processing.generate_windows_df(data, window_size, window_gap, y_column)
            # Handle the aggregation based on the type of y_aggregator
            if isinstance(y_aggregator, str): # for standard functions
                y_df = y_df.agg(y_aggregator, axis=1)
            else:
                # For custom functions, use apply to avoid the FutureWarning
                y_df = y_df.apply(y_aggregator, axis=1)
            assert type(y_df) == pd.Series
            y_dfs.append(y_df)
        y_df = pd.concat(y_dfs, axis=1)
        y_df.columns = y_columns
        
        assert x_df.shape[0] == y_df.shape[0]
        # merge the x and y columns
        final_df = pd.concat([x_df,y_df], axis=1)

    
        return final_df