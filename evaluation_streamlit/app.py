#Archivo principal de Streamlit

import requests
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
import numpy as np
import requests
import json

import streamlit as st

 # Estilos CSS personalizados
estilos = """
        <style>
            .resaltado {
                color: red;
                font-weight: bold;
            }
            .title {
                color: purple;
                font_weight: bold;

            }
        </style>
    """
pagina = ()

st.markdown(estilos, unsafe_allow_html=True)
st.markdown('<h1 class="title">Aplicación Web para Predicción de Arresto del Conductor</h1>', unsafe_allow_html=True)
st.write('''En esta sencilla aplicación web pondremos a prueba el dataset de seguridad vial que hemos
                utilizado para el desarrollo del TFG.''') 

    
# Página de información
def pagina_prediccion():


    st.markdown('### Predicción 1: Arresto ')
    st.write(
    "El modelo evalúa si el conductor fue arrestado basándose en los inputs introducidos.\
    Introduce los detalles de la parada para evaluar si el conductor fue arrestado o no con motivo de la parada."    
    )

    
    #driver_gender	driver_age	driver_race	  violation	  search_conducted	stop_duration	drugs_related_stop	stop_year	stop_hour	stop_hour_category


    # Input 1
    driver_race = st.radio(
        "Ingrese la raza del conductor",
        ("Asian", "Black", "Hispanic", "Other", "White")
    )   

    # Input 2
    violation = st.radio(
        "¿Cúal fue la infracción cometida?",
        ("APB", "Call for Service", "Equipment/Inspection Violation", "Motorist Assist/Courtesy",
         "Other Traffic Violation", "Registration Violation", "Special Detail/Directed Patrol", "Speeding",
         "Suspicious Person", "Violation of City/Town Ordinance", "Warrant")
    )

    # Input 3
    driver_age = st.number_input(
        "Ingrese la edad del conductor", min_value = 15, max_value = 88
    )

    # Input 4
    driver_genre = st.radio(
        "Indique el género del conductor",
        ("F", "M")

    )

    # Input 5
    drugs_related_stop = st.radio (
        "Indique si la parada tuvo relación con las drogas",
        ("Y", "N")
    )

    # Input 6
    search_conducted = st.radio (
        "Indique si se efectuó un registro durante la detención",
        ("Y", "N")
    )

    # Input 7
    stop_duration = st.select_slider(
        "Indique la duración de la parada en minutos",
        options=["0-15", "15-30", "+30"]
    )

    # Input 8
    stop_year = st.number_input(
        "Ingrese el año en el que se produjo la parada", min_value = 2005, max_value = 2011
    )

    stop_hour = st.number_input(
        "Ingrese la hora de la parada (en formato 24 horas)",min_value=0, max_value = 23
    )

    #stop_hour_category

    stop_hour_category = ''
    

    # Class values to be returned by the model
    class_values = {
        0: "no fue arrestado",
        1: "fue arrestado",
    }

    url = "http://host.docker.internal:8000/predict"

    headers = {'Content-Type': 'application/json'}

    # When 'Predecir' is selected
    if st.button("Predecir"):
        


        # Inputs to ML model
        inputs = {  

                    "driver_gender": driver_genre,
                    "driver_age": driver_age,
                    "driver_race": driver_race,
                    "violation": violation,
                    "search_conducted": search_conducted,
                    "stop_duration": stop_duration,
                    "drugs_related_stop": drugs_related_stop,
                    "stop_year": stop_year,
                    "stop_hour": stop_hour,
                    "stop_hour_category": stop_hour_category
                
            }
        
         #map genre
        gender = driver_genre
        coded_genre = 1 if gender == 'F' else 0
        inputs["driver_gender"] = coded_genre

        #map search conducted
        conducted = search_conducted
        coded_conducted = 1 if conducted == 'Y' else 0
        inputs["search_conducted"] = coded_conducted

        #map drugs related stop
        drugs = drugs_related_stop
        coded_drugs = 1 if drugs == 'Y' else 0
        inputs["drugs_related_stop"] = coded_drugs 

        #map duration
        duration = stop_duration

        if duration == '0-15':
            coded_duration = 0
        elif duration == '16-30':
            coded_duration = 1
        else:
            coded_duration = 2

        inputs["stop_duration"] = coded_duration

        #stop_hour_category

        if stop_hour >= 0 and stop_hour <=6:
            stop_hour_category = 'Madrugada'
        elif stop_hour > 6 and stop_hour <=12:
            stop_hour_category = 'Mañana'
        elif stop_hour > 12 and stop_hour <=18:
            stop_hour_category = 'Tarde'
        else:
            stop_hour_category = 'Noche'
        
        inputs["stop_hour_category"] = stop_hour_category

        # envío del diccionaro a la api
        response = requests.post(url, data=json.dumps(inputs), headers=headers)
        #predicción devuelta de la api
        json_response = response.json()
        prediction = class_values[json_response.get("prediction")]
        st.subheader(f"El conductor {prediction}!")
        
# Página principal de la aplicación
def main():

    pagina_prediccion()

# Ejecutar la aplicaciónn
if __name__ == '__main__':
    main()



