import streamlit as st
from google import genai

api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Configura tu GEMINI_API_KEY en los Secrets de Streamlit.")
    st.stop()

client = genai.Client(api_key=api_key)

def calcular_imc(peso, estatura_cm):
    estatura_m = estatura_cm / 100
    imc = peso / (estatura_m ** 2)
    if imc < 18.5: cat = "Bajo peso"
    elif 18.5 <= imc < 24.9: cat = "Peso saludable"
    elif 25.0 <= imc < 29.9: cat = "Sobrepeso"
    else: cat = "Obesidad"
    return imc, cat

st.title("🍏 NutriSense IA")

with st.form("mi_formulario"):
    nombre = st.text_input("Nombre:")
    col1, col2 = st.columns(2)
    with col1:
        peso = st.number_input("Peso (kg):", value=70.0)
        estatura = st.number_input("Estatura (cm):", value=170.0)
    with col2:
        abdomen = st.number_input("Abdomen (cm):", value=80.0)
        idioma = st.selectbox("Idioma:", ["Español", "English", "Português"])
    
    objetivos = st.text_area("Objetivos:")
    enviar = st.form_submit_button("Generar Plan")

if enviar:
    imc_v, imc_c = calcular_imc(peso, estatura)
    
    # Renderizar métricas 
    st.markdown(f"### Resumen para {nombre}")
    st.metric("Tu IMC", f"{imc_v:.2f}", imc_c)

    with st.spinner("Generando..."):
        
        prompt = f"Eres un nutricionista profesional. Usuario: {nombre}, IMC: {imc_v:.2f}. Objetivo: {objetivos}. Responde en {idioma}."
        
        try:
            response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
           
            st.markdown("---")
            st.markdown(response.text) 
        except Exception as e:
            st.error(f"Error de API: {e}")
