import datetime

from fastapi import APIRouter

from api.service.pretty_response import PrettyJSONResponse
from api.service.calculations import calculate_change, round_all_dict
from model.regression import predict_fields

from model.lstm import predict_aqi

router = APIRouter()
prefix = "/calc"


class Initiative:
    name: str
    aqi_curr: float
    aqi_pred: float
    fund_curr: float


@router.post('/fund_recalc')
async def fund_recalc(initiatives: list[dict]):
    # print request type and body
    print("Body: ", initiatives)

    now = datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    time = now.replace(month=now.month + 1, hour=0, minute=0, second=0, microsecond=0)

    processed = []
    for initiative in initiatives:
        # features = predict_fields(time, initiative.get("City"))
        current = round(predict_aqi(initiative.get("City"), now), 5)
        prediction = round(predict_aqi(initiative.get("City"), time), 5)
        print("Current: ", current)
        print("Prediction: ", prediction)
        print("Ratio: ", calculate_change(current, prediction))
        processed.append(
            {
                "Project": initiative.get("Project"),
                "City": initiative.get("City"),
                "Current Funding": initiative.get("Funding"),
                "Weight": calculate_change(current, prediction)
            }
        )
    print([x["Weight"] for x in processed])
    total_funding = sum([initiative.get("Current Funding") for initiative in processed])
    # sum_weights = sum([initiative.get("Weight") for initiative in processed])
    # mean_weight = sum_weights / len(processed)
    # for initiative in processed:
    #     initiative["Weight"] = initiative.get("Weight") / mean_weight

    for initiative in processed:
        initiative["Optimized Funding"] = round(initiative.get("Weight") * initiative.get("Current Funding") + initiative.get("Current Funding"), 2)

    processed = [{k:v for k, v in d.items() if k != "Weight"} for d in processed]
    processed = [round_all_dict(data) for data in processed]
    return PrettyJSONResponse(processed)


def setup(app):
    app.include_router(router, prefix=prefix)
