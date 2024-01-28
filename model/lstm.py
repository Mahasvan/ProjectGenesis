import datetime
import pickle

from model.regression import predict_fields

with open("lstm.pkl", "wb") as f:
    model = pickle.load(f)


def predict_aqi(city: str, timestamp: datetime.datetime):
    fields = predict_fields(timestamp, city)
    prediction = model.predict([fields])
    return prediction
