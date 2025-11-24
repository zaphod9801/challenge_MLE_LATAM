import fastapi
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, validator
from typing import List
import pandas as pd
from challenge.model import DelayModel

app = fastapi.FastAPI()
model = DelayModel()

class Flight(BaseModel):
    OPERA: str
    TIPOVUELO: str
    MES: int

    @validator('MES')
    def validate_mes(cls, v):
        if v < 1 or v > 12:
            raise ValueError('MES must be between 1 and 12')
        return v

    @validator('TIPOVUELO')
    def validate_tipovuelo(cls, v):
        if v not in ['I', 'N']:
            raise ValueError('TIPOVUELO must be I or N')
        return v
    
    @validator('OPERA')
    def validate_opera(cls, v):
        valid_airlines = ['American Airlines', 'Air Canada', 'Air France', 'Aeromexico', 'Aerolineas Argentinas', 'Austral', 'Avianca', 'Alitalia', 'British Airways', 'Copa Air', 'Delta Air', 'Gol Trans', 'Iberia', 'K.L.M.', 'Qantas Airways', 'United Airlines', 'Grupo LATAM', 'Sky Airline', 'Latin American Wings', 'Plus Ultra Lineas Aereas', 'JetSmart SPA', 'Oceanair Linhas Aereas', 'Lacsa']
        if v not in valid_airlines:
            raise ValueError(f'OPERA must be one of {valid_airlines}')
        return v

class PredictionRequest(BaseModel):
    flights: List[Flight]

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )

@app.get("/health", status_code=200)
async def get_health() -> dict:
    return {
        "status": "OK"
    }

@app.post("/predict", status_code=200)
async def post_predict(request: PredictionRequest) -> dict:
    data = pd.DataFrame([flight.dict() for flight in request.flights])
    features = model.preprocess(data=data)
    predictions = model.predict(features=features)
    return {"predict": predictions}