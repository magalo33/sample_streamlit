import streamlit as st

def step_1():
    st.title("Ingrese sus datos")
    nombre = st.text_input("Nombre")
    apellido = st.text_input("Apellido")
    genero = st.selectbox('Género', ('Masculino', 'Femenino', 'Otro'))
    edad = st.text_input("Edad en años")
    ver = False
    return nombre,apellido,genero,edad,ver

def step_2():
    st.title("Cuentenos un poco de se estado de ánimo")
    hoy = st.text_input("¿Como se siente hoy?")
    ayer = st.text_input("¿Como se ha sentido la ultima semana?")
    ver = False
    return hoy, ayer,ver

def step_3():
    st.title("Cuentenos un poco mas")
    morir = st.selectbox('¿Ha pensado que es mejor estar muerto?', ('No', 'Si'))
    suicidio = st.selectbox('¿Hatenido pensamientos suicidas?', ('No', 'Si'))
    ver = True
    return morir, suicidio,ver
    

def main():
    
    p_nombre = ""
    p_apellido = ""
    p_genero = ""
    p_edad = ""
    p_ver = False
    
    st.sidebar.title("Froid")
    current_step = st.sidebar.selectbox("Step", ["Datos del paciente", "Estado de ánimo", "Pensamientos"])
        
    if current_step == "Datos del paciente":
        nombre,apellido,genero,edad,ver = step_1()
        p_nombre = nombre
        p_apellido = apellido
        p_genero = genero
        p_edad = edad
        p_ver = ver
        
    
    elif current_step == "Estado de ánimo":
        hoy, ayer,ver = step_2()
        p_ver = ver
            
    elif current_step == "Pensamientos":
        morir, suicidio,ver = step_3()
        p_ver = ver
        print(str(p_ver))
        if not p_nombre or not p_apellido or not p_genero or not p_edad:
            p_ver = False
        print(str(p_ver))
        
        
    if p_ver:
        if st.sidebar.button("Analizar", key="analizar"):
            print(nombre)
    


if __name__ == "__main__":
    main()