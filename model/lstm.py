import datetime
import pickle

from model.regression import predict_fields

with open("model/model.pickle", "rb") as f:
    model = pickle.load(f)


def predict_aqi(city: str, timestamp: datetime.datetime):
    fields = predict_fields(timestamp, city)
    prediction = model.predict([fields])
    return prediction
