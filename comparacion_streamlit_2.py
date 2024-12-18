import streamlit as st
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, ConfusionMatrixDisplay
import pandas as pd
import matplotlib.pyplot as plt



# Cargar el dataset
color_titulo = "#df836f"
file_path = 'respuestas_final.csv'
@st.cache_data
def cargar_datos():
    data = pd.read_csv(file_path, sep=';', on_bad_lines='skip')
    return data.dropna()

data = cargar_datos()


# Columnas de interés
correct_col = 'Respuesta Correcta'
pred_col = 'Respuesta Ollama'
errores = data[data['Correcto'] == False]

# Comparar respuestas correctas con las del modelo Ollama
y_true = data[correct_col].values
y_pred = data[pred_col].values
accuracy = accuracy_score(y_true, y_pred)

st.sidebar.markdown(
    "<h1 style=\"font-size:25px;color:"+color_titulo+";\"><center>Evaluación del Rendimiento del Modelo Ollama</center></h1>"+
    "<h1 style=\"font-size:20px;color:"+color_titulo+";\"><center>Taller final del Módulo 2</center></h1>"+
    "<ul style=\"font-size:12px;\">"+
    "    <li>Sandra Luengas Aponte-ID UAO:2248280</li>"+
    "    <li>John Alexander Léon Torres-ID UAO: 2248372</li>"+
    "    <li>Jorge Leonardo Prada Dániel-ID UAO:2246604</li>"+
    "    <li>Miguel Arcesio Londoño Garzon-ID UAO: 2246382</li>"+
    "</ul>"
    ,
    unsafe_allow_html=True
    )


# Título de la aplicación

st.markdown("<h1 style=\"font-size:40px;color:"+color_titulo+";\"><center>Evaluación del Rendimiento del Modelo Ollama</center></h1>",unsafe_allow_html=True)

# Menú en la barra lateral
menu = st.sidebar.selectbox("Selecciona una opción", ["Descripción", "Planteamiento", "Contexto", "Exactitud", "Reporte de Clasificación", "Distribución", "Respuestas Incorrectas"])

# Contenido dinámico según la opción seleccionada
if menu == "Descripción":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Descripción del problema a solucionar:</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Se quiere evaluar el desempeño del modelo de inteligencia artificial LLAMA3.2, esto con el fin de medir la confiabilidad del modelo en cuanto a la resolución de preguntas de diferentes temas.</h2>",unsafe_allow_html=True)
elif menu == "Planteamiento":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Planteamiento de la solución:</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Se debe crear un dataset con preguntas y respuesta tipo ICFES, es decir preguntas con múltiple respuesta. Ya que este tipo de dataset no se encuentra publicado, se procede a tomar el dataset ccasimiro/squad_es, el cual consta de preguntas con su respectiva respuesta.  Para generar las múltiples respuestas, se recorre el dataset en un ciclo, y para cada registro, y se crea un prompt que consulte al modelo LLAMA3.2 , pidiéndole que cree 3 respuestas incorrectas de la pregunta. El prompt usado es el siguiente:</h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">prompt = (Con este contexto: {(obj.context)}, y teniendo en cuenta que la pregunta es: {(obj.question)} y la respuesta correcta es: {(respuesta_text[0])}, genera 3 respuestas que no sean correctas. NO agregues texto indicando porque son incorrectas, solo dame las 3 respuestas generadas, tampoco indiques cual fue la respuesta correcta, solo dame las 3 respuestas generadas, lo mas seco y preciso posible, solo las 3 respuestas.</h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Una vez obtenido el promt, se procede a consultar el modelo, y la respuesta se guarda en un arreglo, al cual se agrega la respuesta correcta para tener las 4 respuestas. Este arreglo se pasa por un método que dinámicamente cambia el orden de las respuestas, para evitar que la respuesta correcta siempre este en la ultima posición, de la siguiente manera: </h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; \">def mezclar_vector(vector):<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;vector_mezclado = vector[:]<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;random.shuffle(vector_mezclado)<br>&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;return vector_mezclado<br></h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Una vez obtenido el vector, se guarda cada registro en un archivo .csv con las siguientes columnas: \"Contexto\", \"Pregunta\", \"Opción 1\", \"Opción 2\", \"Opción 3\", \"Opción 4\", \"Respuesta Correcta\"</h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Luego de lo anterior, y mediante un ciclo que recorra todo el dataset generado, se debe consultar nuevamente al modelo llama3.2, pidiéndole que responda cual considera la respuesta correcta de cada una de las preguntas generadas en el script anterior. Esto se hace mediante el siguiente pronmt:  prompt = Basado en este contexto:  {row['Contexto']}, y teneindo en cuenta la siguiente pregunta: {row['Pregunta']}, y las siguientes opciones de respuesta a) {row['Opción 1']}. b) {row['Opción 2']}. c) {row['Opción 3']}.  d) {row['Opción 4']}. ¿cual consideras la respuesta correcta?. Por favor solo dame la respuesta, sin preambulo, sin explicacion del porque, solo la respuesta que consideras correcta.</h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Cada que el modelo contesta, se registra la fila, mas la nueva columna que contiene la respuesta del modelo LLAMA3.2 en un nuevo dataset con las siguientes columnas: \"Contexto\", \"Pregunta\", \"Opción 1\", \"Opción 2\", \"Opción 3\", \"Opción 4\", \"Respuesta Correcta\",\"Respuesta Ollama\"</h2>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">Este nuevo Dataset sera el insumo para generar las métricas y realizar la comparación</h2>",unsafe_allow_html=True)
elif menu == "Contexto":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Marco teórico</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">bla bla bla</h2>",unsafe_allow_html=True)
elif menu == "Exactitud":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Exactitud del modelo</h1>",unsafe_allow_html=True)
    st.markdown("<h2 style=\"font-size:20px;color:white; text-align:justify;\">El modelo muestra una exactitud del "+f"{accuracy:.2%}"+"</h2>",unsafe_allow_html=True)    
    st.markdown(
    """
    <h2 style=\"font-size:20px;color:white; text-align:justify;\">Interpretación</h2>
    <ul style="font-size:12px;">
        <li>El modelo clasificó correctamente aproximadamente 7 de cada 10 casos.</li>
        <li>Dado que el dataset contiene registros que se pueden interpretar como clases únicas, se puede tomar este valor como un dato confiable, sin embargo, se debe analizar este dato junto con otras métricas que se mostraran mas adelante.</li>
    </ul>
    """,
    unsafe_allow_html=True
    )
elif menu == "Reporte de Clasificación":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Reporte de Clasificación</h1>",unsafe_allow_html=True)
    report = classification_report(y_true, y_pred, zero_division=0, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    st.dataframe(report_df)  
    st.markdown(
    """
    <h2 style=\"font-size:20px;color:white; text-align:justify;\">Interpretación</h2>
    <ul style="font-size:12px;">
        <li>Precisión : 72%</li>
        <li>Recall: 70%</li>
        <li>F1-score: 71%</li>
        <li>Accuracy: 70%</li>
    </ul>
    <h2 style=\"font-size:15px;color:white; text-align:justify;\">Estas métricas indican que el modelo clasifica correctamente al rededor del 70% de las instancias.</h2>
        <ul style="font-size:15px;">
        <li>Existen muchas categorías con precisión, recall y F1-score perfectos (1.0). Esto podria indicar que para estas clases el modelo predice correctamente todas las instancias, sin embargo, al observarse un support bajo, no se puede confiar mucho en esta métrica.</li>
        <li>Se observa un número importante de F1-score de 0, lo que indica no predice las clases marcadas de esta manera.</li>
        <li>Algunas clases presentan Recall entre 0.5 y .066, aunque dista de ser perfecto, se interpretan como datos aceptables.</li>
        <li>El macro Avg esta al rededor el 54%, esto implica que el modelo tiene problemas para predecir clases poco frecunetes.</li>
        <li>El modelo en general muestra buen desempeño.</li>
        <li>El hecho de que el support sea bajo se origina en que cada pregunta consigura una clase que tiende a ser única.</li>
        <li>La forma en que generó el dataset, y la baja cantidad de registros impiden una buena precisión del modelo, por lo cual se debe generar un dataset mas grande y balancearlo; Esto deberia aumentar la precisión del modelo.</li>
    </ul>
    """,
    unsafe_allow_html=True
    )
elif menu == "Distribución":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Distribución de Correctos e Incorrectos</h1>",unsafe_allow_html=True)
    data['Correcto'] = data[correct_col] == data[pred_col]
    fig, ax = plt.subplots()
    correct_counts = data['Correcto'].value_counts()
    labels = ['Correcto', 'Incorrecto']
    colors = ['lightgreen', 'lightcoral']
    plt.pie(correct_counts, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90)
    plt.title('Distribución de Correctos e Incorrectos')
    st.pyplot(fig)       
    st.markdown(
    """
    <h2 style=\"font-size:20px;color:white; text-align:justify;\">Interpretación</h2>
    <ul style="font-size:15px;">
        <li>El 70.8% de las predicciones fueron correctas, lo que indica que el modelo tiene un desempeño que se puede interpretar como bueno.</li>
        <li>El valor de 70.8% (Dado que esta redondeado), es consistente con la exactitud.</li>
        <li>El 29.2% de las predicciones fueron incorrectas, lo que muestra una importante oportunidad de mejora.</li>
        <li>El porcentaje de predicciones incorrectas sugiere que el modelo no captura adecuadamente algunos patrones.</li>
        <li>Se requiere ajuste del dataset para realizar una nueva medición que aumente la confiabilidad al análisis hecho.</li>
    </ul>
    """,
    unsafe_allow_html=True
    )    
elif menu == "Respuestas Incorrectas":
    st.markdown("<h1 style=\"font-size:25px;color:"+color_titulo+";\">Total de respuestas incorrectas</h1>",unsafe_allow_html=True)
    st.dataframe(errores[["Contexto", "Pregunta", correct_col, pred_col]].head(10))



