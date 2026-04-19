import pandas as pd

class ProcesadorAsteroides:
    def __init__(self, datos_brutos):
        self.datos_brutos = datos_brutos

    def estructurar_datos(self):
        lista_final = []
        # La API agrupa por fechas, recorremos cada día
        for fecha in self.datos_brutos["near_earth_objects"]:
            for asteroide in self.datos_brutos["near_earth_objects"][fecha]:
                info = {
                    "nombre": asteroide["name"],
                    "diametro_min_km": asteroide["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                    "es_peligroso": asteroide["is_potentially_hazardous_asteroid"],
                    "velocidad_km_h": float(asteroide["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]),
                    "distancia_miss_km": float(asteroide["close_approach_data"][0]["miss_distance"]["kilometers"])
                }
                lista_final.append(info)
        return pd.DataFrame(lista_final)