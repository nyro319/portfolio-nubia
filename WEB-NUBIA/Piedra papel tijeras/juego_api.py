from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Jugada(BaseModel):
    eleccion_usuario: str

@app.post("/jugar")
def jugar(datos: Jugada):
    opciones = ["piedra", "papel", "tijeras"]
    computadora = random.choice(opciones)
    usuario = datos.eleccion_usuario.lower()
    
    if usuario == computadora:
        resultado, status = "¡EMPATE!", "draw"
    elif (usuario == "piedra" and computadora == "tijeras") or \
         (usuario == "papel" and computadora == "piedra") or \
         (usuario == "tijeras" and computadora == "papel"):
        resultado, status = "¡GANASTE!", "win"
    else:
        resultado, status = "¡PERDISTE!", "lose"

    return {
        "usuario": usuario,
        "computadora": computadora,
        "resultado": resultado,
        "status": status
    }