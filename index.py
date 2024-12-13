import streamlit as st

if "p_nombre" not in st.session_state:
    st.session_state.p_nombre = ""
if "p_apellido" not in st.session_state:
    st.session_state.p_apellido = ""
if "p_genero" not in st.session_state:
    st.session_state.p_genero = ""
if "p_edad" not in st.session_state:
    st.session_state.p_edad = ""
if "hoy" not in st.session_state:
    st.session_state.hoy = ""
if "ayer" not in st.session_state:
    st.session_state.ayer = ""
if "morir" not in st.session_state:
    st.session_state.morir = ""
if "suicidio" not in st.session_state:
    st.session_state.suicidio = ""



def step_1():
    st.title("Ingrese los datos del paciente")
    st.session_state.p_nombre = st.text_input("Nombre", value=st.session_state.p_nombre)
    st.session_state.p_apellido = st.text_input("Apellido", value=st.session_state.p_apellido)
    st.session_state.p_genero = st.selectbox('Género', ['Masculino', 'Femenino', 'Otro'], index=['Masculino', 'Femenino', 'Otro'].index(st.session_state.p_genero) if st.session_state.p_genero else 0)
    st.session_state.p_edad = st.text_input("Edad en años", value=st.session_state.p_edad)


def step_2():
    st.title("Cuéntenos un poco de su estado de ánimo")
    st.session_state.hoy = st.text_input("¿Cómo se siente hoy?", value=st.session_state.hoy)
    st.session_state.ayer = st.text_input("¿Cómo se ha sentido la última semana?", value=st.session_state.ayer)


def step_3():
    st.title("Cuéntenos un poco más")
    st.session_state.morir = st.selectbox('¿Ha pensado que es mejor estar muerto?', ['No', 'Si'], index=['No', 'Si'].index(st.session_state.morir) if st.session_state.morir else 0)
    st.session_state.suicidio = st.selectbox('¿Ha tenido pensamientos suicidas?', ['No', 'Si'], index=['No', 'Si'].index(st.session_state.suicidio) if st.session_state.suicidio else 0)



def respuesta():
    return (
        f"Nombre: {st.session_state.p_nombre}\n"
        f"Apellido: {st.session_state.p_apellido}\n"
        f"Género: {st.session_state.p_genero}\n"
        f"Edad: {st.session_state.p_edad}\n"
        f"Estado de ánimo hoy: {st.session_state.hoy}\n"
        f"Estado de ánimo última semana: {st.session_state.ayer}\n"
        f"Pensamientos sobre la muerte: {st.session_state.morir}\n"
        f"Pensamientos suicidas: {st.session_state.suicidio}\n"
    )    



def main():    
    
    ver = False
    
    st.sidebar.markdown(
    """
    <h1 style="font-size:15px;color:#900C3F;"><center>PROCESAMIENTO DE DATOS SECUENCIALES CON DEEP LEARNING</center></h1>
    <h1 style="font-size:20px;color:#900C3F;"><center>Taller final del Módulo 2</center></h1>
    <ul style="font-size:12px;">
        <li>Sandra Luengas Aponte-ID UAO:2248280</li>
        <li>John Alexander Léon Torres-ID UAO: 2248372</li>
        <li>Jorge Leonardo Prada Dániel-ID UAO:2246604</li>
        <li>Miguel Arcesio Londoño Garzon-ID UAO: 2246382</li>
    </ul>
    """,
    unsafe_allow_html=True
    )

    st.sidebar.title("Froid-IA")
    current_step = st.sidebar.selectbox("Diligencie los siguientes campos", ["Datos del paciente", "Estado de ánimo", "Pensamientos"])

    if current_step == "Datos del paciente":
        step_1()

    elif current_step == "Estado de ánimo":
        step_2()

    elif current_step == "Pensamientos":
        ver = True
        step_3()

    if not st.session_state.p_nombre or st.session_state.p_nombre.strip() == "":
        ver = False
    elif not st.session_state.p_apellido or st.session_state.p_apellido.strip() == "":
        ver = False    
    elif not st.session_state.p_genero or st.session_state.p_genero.strip() == "":
        ver = False          
    elif not st.session_state.p_edad or st.session_state.p_edad.strip() == "":
        ver = False     
    elif not st.session_state.hoy or st.session_state.hoy.strip() == "":
        ver = False    
    elif not st.session_state.ayer or st.session_state.ayer.strip() == "":
        ver = False                       

    # Mostrar todos los datos recopilados
    if ver:        
        if st.sidebar.button("Analizar"):
            
            st.write("Datos recopilados:")
            st.write("Nombre:", st.session_state.p_nombre)
            st.write("Apellido:", st.session_state.p_apellido)
            st.write("Género:", st.session_state.p_genero)
            st.write("Edad:", st.session_state.p_edad)
            st.write("Hoy:", st.session_state.hoy)
            st.write("Última semana:", st.session_state.ayer)
            st.write("Pensar en la muerte:", st.session_state.morir)
            st.write("Pensamientos suicidas:", st.session_state.suicidio)
            st.write("----------------------------------------------------")
            
            
            
            st.write(respuesta())
            
            
            
            
            
            st.session_state.p_nombre = ""
            st.session_state.p_apellido = ""
            st.session_state.p_genero = ""
            st.session_state.p_edad = ""
            st.session_state.hoy = ""
            st.session_state.ayer = ""
            st.session_state.morir = ""
            st.session_state.suicidio = ""


if __name__ == "__main__":
    main()
