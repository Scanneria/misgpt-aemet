from fastapi import FastAPI, Query
import requests

app = FastAPI()

AEMET_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJzY2FubmVyaWF2MTcyQGdtYWlsLmNvbSIsImp0aSI6IjJkNTliN2FkLWQ2MjMtNGI2MC05ZTEyLTM3N2QzMzIxMjIxYiIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQ4NTQ1Mjk3LCJ1c2VySWQiOiIyZDU5YjdhZC1kNjIzLTRiNjAtOWUxMi0zNzdkMzMyMTIyMWIiLCJyb2xlIjoiIn0.2YnJzBm6mYwfwgIjK2-fPqPnjjBUeBug2B4iC6Gy6-U"

@app.get("/meteo")
def meteo(municipio_id: str = Query(..., description="Código INE del municipio")):
    headers = {
        "accept": "application/json",
        "api_key": AEMET_API_KEY
    }
    url = f"https://opendata.aemet.es/opendata/api/prediccion/especifica/municipio/diaria/{municipio_id}"

    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        return {"error": "No se pudo obtener respuesta de AEMET"}

    datos_url = res.json().get("datos")
    datos = requests.get(datos_url).json()

    return {
        "debug": "Respuesta completa desde AEMET",
        "municipio": datos[0].get("nombre", "Sin nombre"),
        "contenido_completo": datos[0]
    }

