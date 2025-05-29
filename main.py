from fastapi import FastAPI, Query
import requests

app = FastAPI()

AEMET_API_KEY = "PON_AQUI_TU_TOKEN_AEMET"

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

    pred = datos[0]['prediccion']['dia'][0]
    viento = pred['viento'][0].get('valor', "Sin dato")
    estado = pred['estadoCielo'][0].get('descripcion', "Sin dato")
    precipitacion = pred['probPrecipitacion'][0].get('valor', "Sin dato")

    return {
        "municipio": datos[0]['nombre'],
        "viento_kmh": viento,
        "estado_cielo": estado,
        "precipitacion_prob": precipitacion
    }
