from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Configuración necesaria para que tu HTML (Frontend) pueda comunicarse con este código
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Permite peticiones desde cualquier origen
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definimos el "molde" de los datos que recibiremos de la web
class DatosNomina(BaseModel):
    nombre: str
    puesto: str
    nomina_mensual: float

# Tu clase original adaptada para no usar input()
class Empleado:
    def __init__(self, nombre, puesto, nomina):
        self.nombre = nombre
        self.puesto = puesto
        self.nomina = nomina
        self.anualbruta = self.nomina * 12

    def calcular_irpf(self):
        # Corregido: Según tu lógica, si > 30k es 21%, si < es 15%
        if self.anualbruta > 30000:
            return self.anualbruta * 0.21
        else:
            return self.anualbruta * 0.15

    def calcular_neto(self, retencion):
        return self.anualbruta - retencion

# El "Endpoint" o URL que la web llamará
@app.post("/calcular")
def api_calcular_nomina(datos: DatosNomina):
    # Creamos la instancia de tu clase con los datos de la web
    empleado = Empleado(datos.nombre, datos.puesto, datos.nomina_mensual)
    
    retencion = empleado.calcular_irpf()
    neto = empleado.calcular_neto(retencion)
    
    # Devolvemos el resultado en formato JSON
    return {
        "nombre": empleado.nombre,
        "puesto": empleado.puesto,
        "anual_bruta": empleado.anualbruta,
        "irpf": retencion,
        "neto_anual": neto
    }

# Para ejecutarlo: uvicorn main:app --reload