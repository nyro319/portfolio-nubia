from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/tabla/{numero}")
def obtener_tabla(numero: int):
    # Generamos la lista de objetos para que sea fácil de iterar en el front
    tabla = []
    for i in range(1, 11):
        tabla.append({
            "multiplicador": i,
            "resultado": numero * i
        })
    return {"numero": numero, "tabla": tabla}