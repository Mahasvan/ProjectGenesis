import datetime

from fastapi import APIRouter

from api.service.pretty_response import PrettyJSONResponse
from api.service.calculations import calculate_change
from model.regression import predict_fields

from model.training.regression import predict
router = APIRouter()
prefix = "/calc"


class Initiative:
    name: str
    aqi_curr: float
    aqi_pred: float
    fund_curr: float


@router.get('/fund_recalc')
async def fund_recalc(initiatives: list[dict]):
    now = datetime.datetime.utcnow()
    time = now.replace(month=now.month + 1, hour=0, minute=0, second=0, microsecond=0)

    processed = []
    for initiative in initiatives:
        features = predict_fields(time, initiative.get("City"))

        processed.append(
            {
                "name": initiative.get("Project"),
                "city": initiative.get("City"),
                "aqi_curr": "hmm",
                "aqi_pred": initiative.get("aqi_pred"),
                "fund_curr": initiative.get("Funding"),
                "weight": calculate_change(initiative.get("aqi_curr"), initiative.get("aqi_pred"))
            }
        )

    total_funding = sum([initiative.get("fund_curr") for initiative in processed])
    sum_weights = sum([initiative.get("weight") for initiative in processed])
    mean_weight = sum_weights / len(processed)
    for initiative in processed:
        initiative["weight"] = initiative.get("weight") / mean_weight

    for initiative in processed:
        initiative["fund_pred"] = initiative.get("weight") * total_funding

    response = {"response": processed}
    return PrettyJSONResponse(response)


def setup(app):
    app.include_router(router, prefix=prefix)
