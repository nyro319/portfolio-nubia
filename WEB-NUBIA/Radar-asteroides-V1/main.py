from api_client import NASAClient
from procesador import ProcesadorAsteroides
from datetime import datetime

def ejecutar():
    print("BUSCADOR DE ASTEROIDES CERCANOS - NASA API")
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    
    # 1. Descarga
    cliente = NASAClient()
    datos = cliente.obtener_asteroides(fecha_hoy)
    
    if datos:
        # 2. Procesamiento
        procesador = ProcesadorAsteroides(datos)
        df = procesador.estructurar_datos()
        
        # 3. Mostrar resultados por consola
        print(f"\nSe han encontrado {len(df)} objetos hoy.")
        
        print("\nObjetos Potencialmente Peligrosos:")
        peligrosos = df[df["es_peligroso"] == True]
        
        if peligrosos.empty:
            print("Ningún objeto peligroso por ahora. ")
        else:
            print(peligrosos[["nombre", "velocidad_km_h", "distancia_miss_km" ]])

if __name__ == "__main__":
    ejecutar()