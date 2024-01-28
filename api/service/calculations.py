def calculate_change(aqi_curr, aqi_pred):
    # Calculate the change in AQI
    aqi_change = (aqi_pred - aqi_curr) / aqi_curr
    return aqi_change

