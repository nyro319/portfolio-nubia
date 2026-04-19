from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class DatosSalud(BaseModel):
    peso: float
    altura: float
    horas_sueno: float
    pasos_diarios: int # Nueva métrica

@app.post("/analizar")
def analizar_salud(datos: DatosSalud):
    # 1. IMC
    imc = datos.peso / (datos.altura ** 2)
    
    # 2. Hidratación recomendada (35ml por kg)
    agua_litros = (datos.peso * 35) / 1000
    
    # 3. Nivel de Actividad (Pasos)
    if datos.pasos_diarios < 5000:
        actividad_msg = "Sedentario. Intenta caminar más."
        actividad_status = "warning"
    elif 5000 <= datos.pasos_diarios < 10000:
        actividad_msg = "Activo. Buen ritmo diario."
        actividad_status = "safe"
    else:
        actividad_msg = "Muy activo. ¡Excelente nivel!"
        actividad_status = "pro"

    # 4. Sueño
    sueno_status = "safe" if 7 <= datos.horas_sueno <= 9 else "warning"
    sueno_msg = "Descanso reparador." if sueno_status == "safe" else "Ajusta tus horas de sueño."

    return {
        "imc": round(imc, 2),
        "imc_status": "normal" if 18.5 <= imc < 25 else "warning",
        "agua_recomendada": round(agua_litros, 1),
        "actividad_msg": actividad_msg,
        "actividad_status": actividad_status,
        "sueno_msg": sueno_msg,
        "sueno_status": sueno_status
    }