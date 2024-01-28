import datetime

from fastapi import APIRouter

from api.service.pretty_response import PrettyJSONResponse

from model.lstm import predict_aqi

router = APIRouter()
prefix = "/models"


@router.get('/predict_aqi')
async def aqi(city: str, timestamp: datetime.datetime = datetime.datetime.now()):
    # get prediction for time + 1 month
    new_stamp = timestamp + datetime.timedelta(days=30)
    new_stamp.replace(hour=0, minute=0, second=0, microsecond=0)
    prediction = predict_aqi(city, new_stamp)

    response = {"response": prediction}
    return PrettyJSONResponse(content=response)


def setup(app):
    app.include_router(router, prefix=prefix)
