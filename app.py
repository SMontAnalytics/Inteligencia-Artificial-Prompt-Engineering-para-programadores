import streamlit as st
from google import genai

st.title("🍏 NutriSense: Tu Asesor Nutricional IA")

with st.form("nutri_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre:")
        edad = st.number_input("Edad:", min_value=1, max_value=120, value=25)
        sexo = st.selectbox("Sexo:", ["Masculino", "Femenino", "Otro"])
       
        idioma = st.selectbox("Idioma de la respuesta:", ["Español", "English", "Português", "Français", "Italiano"])
    
    with col2:
        peso = st.number_input("Peso (kg):", min_value=10.0, max_value=300.0, value=70.0)
        estatura = st.number_input("Estatura (cm):", min_value=50.0, max_value=250.0, value=170.0)
        abdomen = st.number_input("Circunferencia Abdominal (cm):", min_value=30.0, max_value=200.0, value=85.0)

    objetivos = st.text_area("¿Cuáles son tus objetivos?", placeholder="Ej: Bajar de peso...")
    
    submit_button = st.form_submit_button(label="Generar Plan Personalizado")

if submit_button:
    if not nombre or not objetivos:
        st.error("Por favor, completa todos los campos.")
    else:
        imc_valor, imc_cat = calcular_imc(peso, estatura)
        
        # Muestra métricas 
        st.divider()
        st.subheader(f"📊 Resumen de Métricas para {nombre}")
   
        with st.spinner(f"🥗 NutriSense está preparando tu plan en {idioma}..."):
            prompt = f"""
            Eres un Asesor Nutricional profesional. 
            Datos del Usuario: {nombre}, {sexo}, {edad} años, {peso}kg, {estatura}cm.
            IMC: {imc_valor:.2f} ({imc_cat}), Abdomen: {abdomen}cm.
            Objetivo: {objetivos}.
            
            RESTRICCIÓN CRÍTICA: Debes responder TODA la asesoría y el plan de alimentación 
            ESTRICTAMENTE en el idioma: {idioma}.
            
            Crea un plan de 3 días en formato Markdown, con un tono motivador y profesional.
            Explica la importancia de la medida abdominal según los datos del usuario.
            """
            
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown("---")
                # Renderiza la respuesta en el idioma elegido
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
