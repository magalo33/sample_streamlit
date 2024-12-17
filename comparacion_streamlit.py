import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay

# Streamlit UI
st.title("Evaluación del Rendimiento del Modelo Ollama")

# Cargar el dataset
file_path = 'respuestas_final.csv'
@st.cache_data
def cargar_datos():
    data = pd.read_csv(file_path, sep=';', on_bad_lines='skip')
    return data.dropna()

data = cargar_datos()

# Columnas de interés
correct_col = 'Respuesta Correcta'
pred_col = 'Respuesta Ollama'

# Comparar respuestas correctas con las del modelo Ollama
y_true = data[correct_col].values
y_pred = data[pred_col].values

# 1. Calcular Exactitud
accuracy = accuracy_score(y_true, y_pred)
st.write(f"### Exactitud del modelo: {accuracy:.2%}")

# 2. Matriz de Confusión
conf_matrix = confusion_matrix(y_true, y_pred, labels=np.unique(y_true))

st.write("### Matriz de Confusión")
fig, ax = plt.subplots()
cm_display = ConfusionMatrixDisplay(confusion_matrix=conf_matrix, display_labels=np.unique(y_true))
cm_display.plot(cmap='viridis', ax=ax, xticks_rotation='vertical')
st.pyplot(fig)

# 3. Reporte de Clasificación
st.write("### Reporte de Clasificación")
report = classification_report(y_true, y_pred, zero_division=0, output_dict=True)
report_df = pd.DataFrame(report).transpose()
st.dataframe(report_df)

# 4. Métricas por Clase: Precisión, Recall y F1-Score
st.write("### Métricas por Clase: Precisión, Recall y F1-Score")
metrics = report_df.drop(['accuracy', 'macro avg', 'weighted avg'], errors='ignore')
fig2, ax2 = plt.subplots(figsize=(12, 6))
clean_labels = [str(label).replace('$', '\\$') for label in metrics.index]
metrics[['precision', 'recall', 'f1-score']].plot(kind='bar', ax=ax2)
ax2.set_xticks(range(len(clean_labels)))
ax2.set_xticklabels(clean_labels, rotation=45)

plt.title("Precisión, Recall y F1-Score por Clase")
plt.xlabel("Clases")
plt.ylabel("Valor")
st.pyplot(fig2)

# 5. Distribución de aciertos y errores
data['Correcto'] = data[correct_col] == data[pred_col]

st.write("### Distribución de Aciertos e Incorrectos")
fig, ax = plt.subplots()
correct_counts = data['Correcto'].value_counts()
labels = ['Correcto', 'Incorrecto']
colors = ['lightgreen', 'lightcoral']
plt.pie(correct_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
plt.title('Distribución de Aciertos e Incorrectos')
st.pyplot(fig)

# 6. Visualización de respuestas incorrectas por preguntas
st.write("### Preguntas con Respuestas Incorrectas")
errores = data[data['Correcto'] == False]

if not errores.empty:
    st.write("Gráfico de barras para las preguntas con más errores:")
    error_counts = errores['Pregunta'].value_counts().head(10)
    fig, ax = plt.subplots()
    sns.barplot(x=error_counts.values, y=error_counts.index, ax=ax, palette='Reds_r')
    ax.set_title("Top 10 Preguntas con Respuestas Incorrectas")
    ax.set_xlabel("Cantidad de Errores")
    ax.set_ylabel("Pregunta")
    st.pyplot(fig)
else:
    st.write("No se encontraron respuestas incorrectas.")

# 7. Distribución de respuestas correctas/incorrectas por contexto
st.write("### Respuestas por Contexto")
context_counts = data.groupby(['Contexto', 'Correcto']).size().unstack(fill_value=0)

if not context_counts.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    context_counts.plot(kind='bar', stacked=True, color=['lightcoral', 'lightgreen'], ax=ax)
    plt.title("Respuestas Correctas e Incorrectas por Contexto")
    plt.xlabel("Contexto")
    plt.ylabel("Cantidad de Respuestas")
    st.pyplot(fig)
else:
    st.write("No hay suficientes datos para mostrar respuestas por contexto.")

# 8. Gráfico de calor para la matriz de confusión
st.write("### Gráfico de Calor - Matriz de Confusión")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="YlGnBu", xticklabels=np.unique(y_true), yticklabels=np.unique(y_true))
plt.title("Matriz de Confusión - Gráfico de Calor")
plt.xlabel("Predicciones")
plt.ylabel("Respuestas Correctas")
st.pyplot(fig)


# 9. Análisis detallado: Respuestas incorrectas
st.write(f"### Total de respuestas incorrectas: {len(errores)}")
st.write("### Ejemplos de respuestas incorrectas")
st.dataframe(errores[["Contexto", "Pregunta", correct_col, pred_col]].head(10))


st.write("## Conclusiones")
st.markdown("""
- **Exactitud del modelo**: El modelo tiene una exactitud del **70.79%**, lo que significa que clasifica correctamente aproximadamente **7 de cada 10 respuestas**.
- **Desempeño aceptable pero mejorable**: Aunque el desempeño es razonable, hay margen para mejorar, especialmente en contextos ambiguos o preguntas con respuestas similares.
- **Análisis de errores**: Las respuestas incorrectas están distribuidas principalmente en preguntas complejas o contextos similares, lo que sugiere posibles limitaciones del modelo en la interpretación semántica.
- **El reporte de clasificación muestra lo siguiente:**:
   - El modelo tiene un desempeño moderado, con un F1-score general del 0.7079.
   - Clasifica correctamente algunas clases, pero falla completamente en otras.   
- **De la Distribución de Aciertos e Incorrectos se puede decir lo siguiente:**:
   - La clasificación correcta representa 70.8% de las respuestas.
   - La clasificación incorrecta representa 29.2% de las respuestas.
   - El alto porcentaje de respuestas correctas refleja que el modelo generalmente entiende bien el problema y clasifica correctamente la mayoría de los casos.
   - El porcentaje de errores sugiere que el modelo aún tiene dificultades en una parte importante de los casos.
- **El gráfico de barras para las preguntas con más errores muestra lo siguiente:**:
   - La pregunta "La Basílica del Sagrado Corazón en Notre Dame está al lado de qué estructura?" es la que presenta más errores.
   - Varias preguntas están relacionadas con instituciones, departamentos o eventos específicos de Notre Dame, lo cual podría ser más difícil de contextualizar para el modelo si la información no está clara o está mal interpretada.
   - El modelo parece tener dificultad para responde preguntas cuyo contexto requiere cuantificar(cuatos, cuantas..)
   
   - Se recomienda ampliar el conjunto de datos para mejorar el rendimiento general.
""")
