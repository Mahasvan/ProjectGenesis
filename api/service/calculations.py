import numpy as np


def calculate_change(aqi_curr, aqi_pred):
    # Calculate the change in AQI
    aqi_change = (aqi_pred - aqi_curr) / aqi_curr
    return aqi_change


def round_all(data: list) -> list:
    rounded_list = []
    for value in data:
        if isinstance(value, (np.int32, np.int64, np.float32, np.float64)):
            # Convert to Python native int or float
            rounded_list.append(np.round(value, 5).item())
        else:
            rounded_list.append(round(value, 5))
    return rounded_list

def round_all_dict(data: dict) -> dict:
    rounded_dict = {}
    for key, value in data.items():
        if isinstance(value, np.ndarray):
            # Convert to a Python list
            rounded_dict[key] = np.round(value, 5).tolist()
        elif isinstance(value, (np.int32, np.int64, np.float32, np.float64)):
            # Convert to Python native int or float
            rounded_dict[key] = np.round(value, 5).item()
        else:
            try:
                rounded_dict[key] = round(value, 5)
            except:
                print("Excepted on key: ", key)
                rounded_dict[key] = value

    return rounded_dict
