import logging
import fastapi
import pandas as pd

from challenge.middleware.exception_handlers import add_exception_handlers
from challenge.models.prediction_request import PredictionRequest
from challenge.services.model_service import ModelService


app = fastapi.FastAPI()
add_exception_handlers(app)
logger = logging.getLogger("uvicorn")


def get_model_service():
    return ModelService()


@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }


@app.post("/predict", status_code=200)
async def post_predict(request: PredictionRequest,
                       model_service: ModelService = fastapi.Depends(get_model_service)) -> dict:
    input_data = pd.DataFrame(request.flights)
    predictions = model_service.predict(input_data)
    return {"predict": predictions}