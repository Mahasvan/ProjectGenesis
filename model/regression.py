import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import datetime

from api.service.calculations import round_all_dict

# Load the dataset
df = pd.read_csv('model/dataset.csv')

# Convert 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Handle missing values (if any)
df = df.fillna(method='ffill')

df['Date'] = pd.to_datetime(df['Date'])
df['year'] = df['Date'].dt.year
df['month'] = df['Date'].dt.month
df['day'] = df['Date'].dt.day

df = df.fillna(method='ffill')

fields = ["tavg", "tmin", "tmax", "City", 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3',
          'Benzene', 'Toluene', 'Xylene']

labels = {
    "Bengaluru": 0,
    "Chennai": 1,
    "Delhi": 2,
    "Lucknow": 3,
    "Mumbai": 4,
}


def get_df_instance(timestamp, max=10, curr=0):
    if curr >= max:
        return None

    day = timestamp.day
    month = timestamp.month
    year = timestamp.year
    # get df entry where date is previous_timestamp
    df_previous = df[(df['day'] == day) & (df['month'] == month) & (df['year'] == year)]
    if df_previous.empty:
        df_previous = get_df_instance(timestamp.replace(year=timestamp.year - 1, hour=0, minute=0, second=0,
                                                        microsecond=0), curr + 1)
    return df_previous


# Function to predict the values for each pollutant
def predict_fields(timestamp, city):
    # check previous year data
    previous_timestamp = timestamp.replace(year=timestamp.year - 1, hour=0, minute=0, second=0, microsecond=0)
    day = previous_timestamp.day
    month = previous_timestamp.month
    year = previous_timestamp.year
    # get df entry where date is previous_timestamp
    df_previous = get_df_instance(previous_timestamp)
    df_previous = df_previous[df_previous['City'] == city]
    if df_previous.empty:
        df_previous = df.iloc[0]

    if isinstance(df_previous["City"], str):
        df_previous["City"] = labels[df_previous["City"]]
    else:
        df_previous["City"] = df_previous["City"].apply(lambda x: labels[x])
    prev_values = df_previous.to_dict()
    prev_values = {k: list(v.values())[0] for k, v in prev_values.items()}
    del prev_values["time"]
    del prev_values["Date"]
    prev_values = round_all_dict(prev_values)
    return prev_values


if __name__ == '__main__':
    timestamp = datetime.datetime(2023, 2, 28)
    print(list(predict_fields(timestamp)))
