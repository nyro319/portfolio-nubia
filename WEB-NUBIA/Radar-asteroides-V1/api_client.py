import requests

class NASAClient:
    def __init__(self):
        # API key "DEMO_KEY" (cambiar a la mía personal si es necesario)
        self.base_url = "https://api.nasa.gov/neo/rest/v1/feed"
        self.api_key = "DEMO_KEY"

    def obtener_asteroides(self, fecha_inicio):
        params = {
            "start_date": fecha_inicio,
            "api_key": self.api_key
        }
        response = requests.get(self.base_url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error en la petición: {response.status_code}")
            return None