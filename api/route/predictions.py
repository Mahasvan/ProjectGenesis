import datetime

from fastapi import APIRouter

from api.service.pretty_response import PrettyJSONResponse
from api.service.calculations import round_all
from model.lstm import predict_aqi

router = APIRouter()
prefix = "/models"


@router.get('/predict_aqi')
async def aqi(city: str, timestamp: datetime.datetime = datetime.datetime.now()):
    aqis = []
    # get prediction for time + 1 month
    for i in range(1, 31):
        new_stamp = timestamp + datetime.timedelta(days=i)
        new_stamp.replace(hour=0, minute=0, second=0, microsecond=0)
        prediction = predict_aqi(city, new_stamp)
        aqis.append(prediction)

    aqis = round_all(aqis)
    print(aqis)
    return PrettyJSONResponse(content={"AQI": aqis})


def setup(app):
    app.include_router(router, prefix=prefix)
