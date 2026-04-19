from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nuestro catálogo de productos "Master"
CATALOGO = {
    "Camiseta Algodón": 15.00,
    "Pantalón Vaquero": 35.50,
    "Zapatillas de deporte": 59.99,
    "Paraguas": 12.00,
    "Sudadera con Capucha": 25.00
}

class DatosCompra(BaseModel):
    producto: str
    cantidad: int

@app.post("/generar-ticket")
def generar_ticket(datos: DatosCompra):
    # Obtenemos el precio del catálogo según el nombre enviado
    precio_unitario = CATALOGO.get(datos.producto, 0.0)
    
    subtotal_base = precio_unitario * datos.cantidad
    descuento = subtotal_base * 0.05 if datos.cantidad >= 10 else 0
    subtotal_con_desc = subtotal_base - descuento
    iva = subtotal_con_desc * 0.21
    total = subtotal_con_desc + iva
    
    return {
        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
        "producto": datos.producto.upper(),
        "precio_uni": precio_unitario,
        "cantidad": datos.cantidad,
        "subtotal": round(subtotal_base, 2),
        "descuento": round(descuento, 2),
        "iva": round(iva, 2),
        "total": round(total, 2)
    }