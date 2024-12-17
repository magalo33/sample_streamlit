import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay

# Cargar el dataset
file_path = 'respuestas_final.csv'
data = pd.read_csv(file_path, sep=';')

# Mostrar las primeras filas para verificar el contenido
print("Vista previa del dataset:")
print(data.head())

# Verificar valores nulos
data = data.dropna()

# Columnas de interés
correct_col = 'Respuesta Correcta'
pred_col = 'Respuesta Ollama'

# Comparar respuestas correctas con las del modelo Ollama
y_true = data[correct_col].values
y_pred = data[pred_col].values

# 1. Calcular Exactitud
accuracy = accuracy_score(y_true, y_pred)
print(f"Exactitud del modelo: {accuracy:.2%}")

# 2. Matriz de Confusión
conf_matrix = confusion_matrix(y_true, y_pred, labels=np.unique(y_true))

# Mostrar la matriz de confusión
print("Matriz de Confusión:")
print(conf_matrix)

display = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(y_true))
display.plot(cmap='viridis', xticks_rotation='vertical')
plt.title("Matriz de Confusión para el Modelo Ollama")
plt.show()

# 3. Reporte de Clasificación
report = classification_report(y_true, y_pred, zero_division=0)
print("Reporte de Clasificación:")
print(report)

# 4. Distribución de aciertos y errores
data['Correcto'] = data[correct_col] == data[pred_col]

# Gráfica de aciertos vs errores
plt.figure(figsize=(8, 5))
data['Correcto'].value_counts().plot(kind='bar', color=['green', 'red'])
plt.xticks([0, 1], ['Correcto', 'Incorrecto'], rotation=0)
plt.ylabel('Cantidad')
plt.title('Distribución de Aciertos e Incorrectos')
plt.show()

# 5. Análisis detallado: Respuestas incorrectas
errores = data[data['Correcto'] == False]
print(f"Total de respuestas incorrectas: {len(errores)}")

# Mostrar algunas respuestas incorrectas
print("Ejemplos de respuestas incorrectas:")
print(errores[["Contexto", "Pregunta", correct_col, pred_col]].head(10))
