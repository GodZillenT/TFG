#Archivo principal de FastAPI
import pickle
import joblib
from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
from pathlib import Path
#from TFG.models.model import make_predict, __version__ as model_version
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import os
import numpy as np

app = FastAPI()

__version__ = "0.1.0"


# loading model
pickle_in_model = open("./models/best_catboost_model.pkl","rb")
model = pickle.load(pickle_in_model)


#loading preprocessing steps
pickle_in_pipe = open("./models/preprocessing_pipeline.pkl", "rb")
preprocessing = pickle.load(pickle_in_pipe)



class DriverData(BaseModel):
    driver_gender: int = Field(0, description="Género del conductor")
    driver_age: int = Field(58, description="Edad del conductor")
    driver_race: str = Field("White", description="Raza del conductor")
    violation: str = Field("Speeding", description="Tipo de violación")
    search_conducted: int = Field(0, description="Búsqueda realizada")
    stop_duration: int = Field(0, description="Duración de la detención")
    drugs_related_stop: int = Field(0, description="Detención relacionada con drogas")
    stop_year: int = Field(2007, description="Año de la detención")
    stop_hour: int = Field(10, description="Hora de la detención")
    stop_hour_category: str = Field("Mañana", description="Momento de la parada")


@app.get("/")
def home():
    return {"health_check": "OK", "model_version": __version__}

@app.post("/predict")
def prediccion(data: DriverData):

    df = pd.DataFrame([data.dict().values()], columns=data.dict().keys())
    
    df_preprocessed = preprocessing.transform(df)
 
    prediction = model.predict(df_preprocessed)  
 
    return {"prediction": int(prediction[0])}