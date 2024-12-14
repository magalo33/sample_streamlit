import streamlit as st
from PyPDF2 import PdfReader

import subprocess


"""
    dependencias nesesarias en el archivo requirements
    streamlit
    PyPDF2
"""

#Se cargan las variables de manera global
if "nivel" not in st.session_state:
    st.session_state.nivel = ""    
if "titulo" not in st.session_state:
    st.session_state.titulo = ""
if "tema" not in st.session_state:
    st.session_state.tema = ""    
if "paginas" not in st.session_state:
    st.session_state.paginas = "" 
if "enfatizar" not in st.session_state:
    st.session_state.enfatizar = ""   
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None      
        
#Metodo para generar el prompt a partir de los campos diligenciados
def prompt_generado():
    prompt = (
    "Basado en el documento anexo, genera preguntas tipo ICFES(recuerda que Las preguntas del ICFES son de selección múltiple con única respuesta, es decir, tienen un enunciado y cuatro opciones de respuesta, de las cuales solo una es la correcta) "
    "Para generar las preguntas, ten en cuenta los siguentes puntos: \n\n"
    f"nivel educativo: {st.session_state.nivel},"
    f"Titulo del texto: {st.session_state.titulo},"
    f"Tema del texto: {st.session_state.tema},"
    f"Numero de paginas: {st.session_state.paginas},"
    f"Tema por enfatizar: {st.session_state.enfatizar}"
    ) 
    return prompt     

#Método que consulta al modelo para generar las preguntas
def generar_preguntas():
    if st.session_state.uploaded_file is not None:
        # Extraer texto del documento
        reader = PdfReader(st.session_state.uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        
        # limpiar el texto
        text = text.strip()

        # Se termina de generar el prompt                
        prompt = prompt_generado()+f"""
        
            Texto del documento:
            {text}
            Por favor, genera al menos 10 preguntas ICFES completas, cada una con su enunciado y sus cuatro opciones (A, B, C, D), indicando claramente cuál es la respuesta correcta.
        """

        # comando para ejecutar ollama
        cmd = [
            "ollama",
            "run",
            "llama3.2"
        ]

        st.write("Generando preguntas...")

        try:
            # Se ejecuta el comando y se envia el prompt
            result = subprocess.run(cmd, input=prompt, capture_output=True, text=True, encoding='utf-8')
            if result.returncode == 0:
                response = result.stdout.strip()
                st.subheader("Preguntas generadas:")
                #Se imprime la respuesta generada por el modelo de IA
                st.text(response)
            else:
                st.error("Ocurrió un error al ejecutar el modelo:")
                st.error(result.stderr)

        except Exception as e:
            st.error("Error al invocar Ollama:")
            st.error(str(e))


     

def main():    
    
    #Crear un panel a la izquierda con los datos del trabajo e integrantes del grupo
    st.sidebar.markdown(
    """
    <h1 style="font-size:15px;color:#900C3F;"><center>PROCESAMIENTO DE DATOS SECUENCIALES CON DEEP LEARNING</center></h1>
    <h1 style="font-size:20px;color:#900C3F;"><center>Taller final del Módulo 2<br>PROTOTIPO DE APLICACIÓN</center></h1>
    <ul style="font-size:12px;">
        <li>Sandra Luengas Aponte-ID UAO:2248280</li>
        <li>John Alexander Léon Torres-ID UAO: 2248372</li>
        <li>Jorge Leonardo Prada Dániel-ID UAO:2246604</li>
        <li>Miguel Arcesio Londoño Garzon-ID UAO: 2246382</li>
    </ul>
    """,
    unsafe_allow_html=True
    )


    #Tirulo de la página
    st.markdown(
    """
    <h1 style="font-size:20px;color:#900C3F;"><center>GENERADOR DE EVALUACIONES TIPO ICFES</center></h1>
    """,
    unsafe_allow_html=True
    )

    #Se crean los elementos visuales de la página
    st.session_state.nivel = st.selectbox("Seleccione el Nivel Educativo", ["Básico", "Intermedio", "Avanzado"])
    st.session_state.titulo = st.text_input("Título del texto", value=st.session_state.titulo)
    st.session_state.tema = st.text_input("Tema", value=st.session_state.tema)  
    st.session_state.paginas = st.text_input("Número de Páginas", value=st.session_state.paginas)        
    st.session_state.enfatizar = st.text_input("Tema por Enfatizar", value=st.session_state.enfatizar) 
    st.session_state.uploaded_file = st.file_uploader("Seleccione el documento base (PDF)", type=["pdf"]) 
    if st.button("GENERAR PREGUNTAS"):
        generar_preguntas()
    
#Se inicia la ejecución del programa
if __name__ == "__main__":
    main()
