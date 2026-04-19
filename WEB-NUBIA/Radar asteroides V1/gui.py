import customtkinter as ctk
from api_client import NASAClient
from procesador import ProcesadorAsteroides
from datetime import datetime

# Configuración de apariencia
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AsteroidApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("NEO Tracker - NASA Monitoring System")
        self.geometry("900x600")

        # --- Layout Principal ---
        # Configuramos 2 columnas: una estrecha para el menú y otra ancha para los datos
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Sidebar (Menú lateral)
        # CORRECCIÓN: column=0 (con igual, no con dos puntos)
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="RADAR\nASTEROIDES", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.btn_actualizar = ctk.CTkButton(self.sidebar, text="Escanear Espacio", command=self.cargar_datos)
        self.btn_actualizar.grid(row=1, column=0, padx=20, pady=10)

        # Panel Principal
        self.main_frame = ctk.CTkFrame(self, corner_radius=15, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Título y Estado
        self.status_label = ctk.CTkLabel(self.main_frame, text="Sistema listo para escaneo", font=("Courier", 14))
        self.status_label.grid(row=0, column=0, pady=(0, 20))

        # TextBox para resultados
        self.result_text = ctk.CTkTextbox(self.main_frame, font=("Courier", 13), border_width=2)
        self.result_text.grid(row=1, column=0, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)

    def cargar_datos(self):
        self.status_label.configure(text="Conectando con la NASA...", text_color="#3B8ED0")
        self.update() 
        
        try:
            # Obtenemos la fecha actual
            fecha_hoy = datetime.now().strftime("%Y-%m-%d")
            
            # Instanciamos tus clases de lógica
            cliente = NASAClient()
            datos = cliente.obtener_asteroides(fecha_hoy)
            
            if datos:
                procesador = ProcesadorAsteroides(datos)
                df = procesador.estructurar_datos()
                
                # Limpiamos la pantalla
                self.result_text.delete("1.0", "end")
                
                # Formateamos el reporte
                reporte = f"INFORME DE VIGILANCIA ESPACIAL - {fecha_hoy}\n"
                reporte += "="*65 + "\n"
                reporte += f"{'OBJETO':<20} | {'VELOCIDAD (km/h)':<18} | {'ESTADO':<15}\n"
                reporte += "-"*65 + "\n"
                
                for _, row in df.iterrows():
                    peligro_str = "PELIGRO" if row['es_peligroso'] else "Estable"
                    # Usamos f-strings para alinear las columnas
                    reporte += f"{row['nombre']:<20} | {row['velocidad_km_h']:<18.2f} | {peligro_str:<15}\n"
                
                self.result_text.insert("0.0", reporte)
                self.status_label.configure(text=f"OK: {len(df)} objetos en radar", text_color="#4CAF50")
            else:
                self.status_label.configure(text="ERROR: No se recibieron datos", text_color="#F44336")
        except Exception as e:
            self.status_label.configure(text=f"ERROR DE SISTEMA: {str(e)}", text_color="#F44336")

if __name__ == "__main__":
    app = AsteroidApp()
    app.mainloop()