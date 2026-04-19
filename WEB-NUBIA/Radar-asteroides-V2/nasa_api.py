from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# API KEY DE PRUEBA (La de la NASA es gratuita)
NASA_URL = "https://api.nasa.gov/neo/rest/v1/feed"
API_KEY = "DEMO_KEY" 

@app.get("/scan")
def scan_asteroids():
    hoy = datetime.now().strftime("%Y-%m-%d")
    params = {"start_date": hoy, "end_date": hoy, "api_key": API_KEY}
    
    try:
        response = requests.get(NASA_URL, params=params)
        data = response.json()
        
        asteroides_procesados = []
        elementos = data.get("near_earth_objects", {}).get(hoy, [])
        
        for ast in elementos:
            asteroides_procesados.append({
                "nombre": ast["name"],
                "velocidad": float(ast["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]),
                "peligro": ast["is_potentially_hazardous_asteroid"],
                "diametro_max": ast["estimated_diameter"]["meters"]["estimated_diameter_max"]
            })
            
        return {
            "fecha": hoy,
            "total": len(asteroides_procesados),
            "objetos": asteroides_procesados
        }
    except Exception as e:
        return {"error": str(e)}