import pandas as pd
import subprocess
import csv

# Cargar el archivo CSV
file_path = 'respuestas.csv' 
df = pd.read_csv(file_path, delimiter=';')

# Método para recorrer fila por fila 
# Crear el prompt para consultarle a Ollama
# y generar un dataset con la linea completa
# y la respuesta de ollama
with open("respuestas_final.csv", mode="w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=";")
        writer.writerow(["Contexto", "Pregunta", "Opción 1", "Opción 2", "Opción 3", "Opción 4", "Respuesta Correcta","Respuesta Ollama"])

        for index, row in df.iterrows():
            prompt = f"Basado en este contexto:  \"{row['Contexto']}\", y teneindo en cuenta la siguiente pregunta: \"{row['Pregunta']}\", y las siguientes opciones de respuesta a) \"{row['Opción 1']}.\" b) \"{row['Opción 2']}.\" c) \"{row['Opción 3']}.\"  d) \"{row['Opción 4']}.\" ¿cual consideras la respuesta correcta?. Por favor solo dame la respuesta, sin preambulo, sin explicacion del porque, solo la respuesta que consideras correcta."
            
            cmd = [
                "ollama",
                "run",
                "llama3.2"
            ]

            try:
                result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8')
                if result.returncode == 0:
                    response = result.stdout.strip()
                    writer.writerow([
                        row['Contexto'], 
                        row['Pregunta'], 
                        row['Opción 1'], 
                        row['Opción 2'], 
                        row['Opción 3'], 
                        row['Opción 4'], 
                        ((row['Respuesta Correcta'].lower()).replace(".","")).strip(),
                        (((response.replace("a) ","").replace("b) ","").replace("c) ","").replace("d) ","").replace("\"","")).lower()).replace(".","")).strip()
                    ])
                    
                    
                else:
                    print("Ocurrió un error al ejecutar el modelo")

            except Exception as e:
                print(f"Error al invocar Ollama: {e}")
