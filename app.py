import streamlit as st
from google import genai
from google.genai.errors import APIError

st.set_page_config(page_title="NutriSense - Asesor IA", page_icon="🍏", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #4CAF50; color: white; }
    </style>
    """, unsafe_allow_html=True)


# Intentamos obtener la clave de los secretos de Streamlit o de variables de entorno
api_key = st.secrets.get("GEMINI_API_KEY") or st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

if not api_key:
    st.warning("⚠️ Por favor, ingresa tu API Key para continuar.")
    st.stop()

client = genai.Client(api_key=api_key)

def calcular_imc(peso, estatura_cm):
    estatura_m = estatura_cm / 100
    imc = peso / (estatura_m ** 2)
    if imc < 18.5: cat = "Bajo peso"
    elif 18.5 <= imc < 24.9: cat = "Peso normal (Saludable)"
    elif 25.0 <= imc < 29.9: cat = "Sobrepeso"
    else: cat = "Obesidad"
    return imc, cat

st.title("🍏 NutriSense: Tu Asesor Nutricional IA")
st.write("Completa tus datos para recibir un análisis detallado y un plan de alimentación personalizado.")

with st.form("nutri_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        nombre = st.text_input("Nombre:")
        edad = st.number_input("Edad:", min_value=1, max_value=120, value=25)
        sexo = st.selectbox("Sexo:", ["Masculino", "Femenino"])
    
    with col2:
        peso = st.number_input("Peso (kg):", min_value=10.0, max_value=300.0, value=70.0)
        estatura = st.number_input("Estatura (cm):", min_value=50.0, max_value=250.0, value=170.0)
        abdomen = st.number_input("Circunferencia Abdominal (cm):", min_value=30.0, max_value=200.0, value=85.0)

    objetivos = st.text_area("¿Cuáles son tus objetivos?", placeholder="Ej: Bajar 5kg en dos meses, ganar masa muscular, etc.")
    
    submit_button = st.form_submit_button(label="Generar Plan Personalizado")

if submit_button:
    if not nombre or not objetivos:
        st.error("Por favor, completa todos los campos.")
    else:
        imc_valor, imc_cat = calcular_imc(peso, estatura)
        
        st.divider()
        st.subheader(f"📊 Resumen de Métricas para {nombre}")
        c1, c2, c3 = st.columns(3)
        c1.metric("IMC", f"{imc_valor:.1f}")
        c2.metric("Categoría", imc_cat)
        c3.metric("Abdomen", f"{abdomen} cm")
        
        with st.spinner("🥗 NutriSense está diseñando tu plan..."):
            prompt = f"""
            Eres un Asesor Nutricional profesional. 
            Usuario: {nombre}, {sexo}, {edad} años. 
            Peso: {peso}kg, Estatura: {estatura}cm, Abdomen: {abdomen}cm.
            IMC: {imc_valor:.2f} ({imc_cat}).
            Objetivo: {objetivos}.
            
            Crea un plan de alimentación de 3 días en formato Markdown. 
            Incluye una breve explicación de los riesgos de la circunferencia abdominal según su medida.
            Usa un tono motivador.
            """
            
            try:
                response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                st.markdown("---")
                st.markdown(response.text)
                
                st.download_button("Descargar Plan (TXT)", response.text, file_name="mi_plan_nutricional.txt")
                
            except Exception as e:
                st.error(f"Hubo un error con la IA: {e}")