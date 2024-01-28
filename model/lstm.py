import datetime
import pickle

from model.regression import predict_fields

from model.training.regression import predict

with open("model/model.pickle", "rb") as f:
    model = pickle.load(f)


def predict_aqi(city: str, timestamp: datetime.datetime):
    fields = predict_fields(timestamp, city)
    input_features = {
        'tavg': fields.get("tavg"),
        'tmin': fields.get("tmin"),
        'tmax': fields.get("tmax"),
        'PM2.5': fields.get("PM2.5"),
        'PM10': fields.get("PM10"),
        'NO': fields.get("NO"),
        'NO2': fields.get("NO2"),
        'NOx': fields.get("NOx"),
        'NH3': fields.get("NH3"),
        'CO': fields.get("CO"),
        'SO2': fields.get("SO2"),
        'O3': fields.get("O3"),
        'Benzene': fields.get("Benzene"),
        'Toluene': fields.get("Toluene"),
        'Xylene': fields.get("Xylene"),
        'year': timestamp.year,
        'month': timestamp.month,
        'day': timestamp.day,
        'City_encoded': fields.get("City")
    }

    prediction = predict.load_model_and_predict(features=input_features)
    return round(prediction, 2)
