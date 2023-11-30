from typing import List
from pydantic import BaseModel


class PredictionRequest(BaseModel):
    flights: List[dict]
