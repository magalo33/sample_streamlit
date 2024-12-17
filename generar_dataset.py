import re
from datasets import load_dataset
from dataclasses import dataclass
import subprocess
import random
import csv  # Importar módulo csv

# Definir una clase para estructurar los datos
@dataclass
class QAItem:
    id: str
    title: str
    context: str
    question: str
    answers: dict

# Cargar el dataset
dataset = load_dataset("ccasimiro/squad_es", "v1.1.0", trust_remote_code=True)

# Extraer los datos de entrenamiento
train_data = dataset["train"]

# Convertir cada ítem en un objeto de Python
qa_items = [QAItem(**item) for item in train_data]

# Función para extraer el vector de respuestas incorrectas
def extraer_respuestas_incorrectas(output, respuesta_correcta):
    """
    Procesa la salida del modelo para extraer las 3 respuestas incorrectas en forma de lista.
    """
    respuestas = re.findall(r"^\d+\.\s(.+)", output, re.MULTILINE)
    respuestas.append(respuesta_correcta)
    return mezclar_vector(respuestas)

# Función principal para ejecutar y procesar las respuestas

def procesar_respuestas(objetos):
    filas = 0
    with open("respuestas.csv", mode="w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.writer(archivo_csv, delimiter=";")
        writer.writerow(["Contexto", "Pregunta", "Opción 1", "Opción 2", "Opción 3", "Opción 4", "Respuesta Correcta"])
        
        for idx, obj in enumerate(objetos):
            respuesta_text = obj.answers['text']  # Accede al contenido de 'text'
            
            if filas < 200:  # Filtramos por índices específicos
                prompt = (f"Con este contexto: \"{(obj.context)}\", "
                          f"y teniendo en cuenta que la pregunta es: \"{(obj.question)}\" "
                          f"y la respuesta correcta es: \"{(respuesta_text[0])}\", "
                          f"genera 3 respuestas que no sean correctas. NO agregues texto indicando porque son incorrectas, solo dame las 3 respuestas generadas, tampoco indiques cual fue la respuesta correcta, solo dame las 3 respuestas generadas, lo mas seco y preciso posible, solo las 3 respuestas")
                
                cmd = [
                    "ollama",
                    "run",
                    "llama3.2"
                ]

                try:
                    result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8')
                    if result.returncode == 0:
                        response = result.stdout.strip()
                        vector_respuestas = extraer_respuestas_incorrectas(response, respuesta_text[0])
                        
                        # Escribir la línea en el archivo CSV
                        writer.writerow([
                            obj.context.replace("\"",""), 
                            obj.question.replace("\"",""), 
                            vector_respuestas[0], 
                            vector_respuestas[1], 
                            vector_respuestas[2], 
                            vector_respuestas[3], 
                            respuesta_text[0]
                        ])
                        filas += 1
                        
                    else:
                        print("Ocurrió un error al ejecutar el modelo")
                        filas -= 1

                except Exception as e:
                    print(f"Error al invocar Ollama: {e}")
                    filas -= 1

# Metodo que recibe una lista y mezcla el contenido para cambiar el orden en que se encuentra
def mezclar_vector(vector):
    vector_mezclado = vector[:]
    random.shuffle(vector_mezclado)
    return vector_mezclado

# Ejecutar la función para procesar las respuestas
procesar_respuestas(qa_items)
