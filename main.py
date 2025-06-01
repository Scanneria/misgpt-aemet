from fastapi import FastAPI, Query
from pydantic import BaseModel
import requests

app = FastAPI(
    title="MisGPT AEMET",
    version="1.0.0"
)

AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzY2FubmVyaWF2MTcyQGdtYWlsLmNvbSIsImp0aSI6IjJkNTliN2FkLWQ2MjMtNGI2MC05ZTEyLTM3N2QzMzIxMjIxYiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQ4NTQ1Mjk3LCJ1c2VySWQiOiIyZDU5YjdhZC1kNjIzLTRiNjAtOWUxMi0zNzdkMzMyMTIyMWIiLCJyb2xlIjoiIn0.2YnJzBm6mYwfwgIjK2-fPqPnjjBUeBug2B4iC6Gy6-U"

class WeatherResponse(BaseModel):
    municipio: str
    viento_kmh: int
    estado_cielo: str
    precipitacion_prob: int

@app.get("/meteo", response_model=WeatherResponse)
def meteo(municipio_id: str = Query(..., description="Código INE del municipio")):
    try:
        headers = {
            "accept": "application/json",
            "api_key": AEMET_API_KEY
        }
        url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{municipio_id}"
        res = requests.get(url, headers=headers)
        if res.status_code != 200:
            raise Exception(f"AEMET respuesta {res.status_code}")

        datos_url = res.json().get("datos")
        if not datos_url:
            raise Exception("No se encontró el campo 'datos' en la respuesta AEMET")

        datos_res = requests.get(datos_url)
        if datos_res.status_code != 200:
            raise Exception(f"No se pudo acceder a datos_url: {datos_url}")

        datos = datos_res.json()
        if not datos or not datos[0].get("prediccion", {}).get("dia", []):
            raise Exception("Estructura JSON inesperada en datos")

        def obtener_valor(lista, campo):
            return next((item[campo] for item in lista if campo in item and item[campo] not in ["", None, 0]), 0)

        dia_hoy = datos[0]["prediccion"]["dia"][0]

        viento = obtener_valor(dia_hoy.get("viento", []), "velocidad")
        cielo = obtener_valor(dia_hoy.get("estadoCielo", []), "descripcion")
        lluvia = obtener_valor(dia_hoy.get("probPrecipitacion", []), "value")

        return WeatherResponse(
            municipio=datos[0].get("nombre", "Desconocido"),
            viento_kmh=int(viento),
            estado_cielo=cielo,
            precipitacion_prob=int(lluvia)
        )

    except Exception as e:
        return WeatherResponse(
            municipio="Error",
            viento_kmh=0,
            estado_cielo=str(e),
            precipitacion_prob=0
        )

