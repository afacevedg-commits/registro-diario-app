import streamlit as st
import pandas as pd
import datetime
import os
from io import BytesIO

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Appnea - Registro Diario", page_icon="🤿", layout="centered")

# --- ESTILOS PERSONALIZADOS ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A; /* Azul oscuro profundo */
        text-align: center;
        margin-bottom: 0;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #3B82F6; /* Azul claro */
        text-align: center;
        margin-top: 0;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F3F4F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #DBEAFE;
        color: #1E3A8A;
        font-weight: bold;
        border-bottom: 2px solid #1E3A8A;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="main-header">Appnea - Plan Maestro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Registro de Entrenamiento y Bienestar</p>', unsafe_allow_html=True)

# --- FUNCIÓN PARA CARGAR EL ARCHIVO EXCEL ---
@st.cache_data
def load_data(file_name):
    try:
        xls = pd.ExcelFile(file_name)
        df_entrenamiento = pd.read_excel(xls, 'Entrenamiento')
        df_alimentacion = pd.read_excel(xls, 'Alimentación')
        df_chequeo = pd.read_excel(xls, 'Chequeo Diario')
        return df_entrenamiento, df_alimentacion, df_chequeo
    except FileNotFoundError:
        st.error("⚠️ No se encontró el archivo Excel base. Por favor, verifica el nombre.")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

# Nombre exacto de tu archivo
archivo = "Plan Maestro Integrado - Entrenamiento, Alimentación y Chequeo Diario (Agosto 2026)_3.xlsx"
df_ent, df_ali, df_cheq = load_data(archivo)

# Función para guardar datos usando BytesIO para evitar problemas de permisos
def guardar_datos(df_ent, df_ali, df_cheq):
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df_ent.to_excel(writer, sheet_name='Entrenamiento', index=False)
            df_ali.to_excel(writer, sheet_name='Alimentación', index=False)
            df_cheq.to_excel(writer, sheet_name='Chequeo Diario', index=False)
        
        with open(archivo, "wb") as f:
            f.write(output.getvalue())
        return True
    except Exception as e:
        st.error(f"Error al guardar: {e}")
        return False

# --- ESTRUCTURA DE PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🤿 Entrenamiento", "🥗 Alimentación", "📊 Chequeo Diario"])

# FECHA GLOBAL PARA EL DÍA (se usa en todas las pestañas)
fecha_hoy = st.sidebar.date_input("📅 Fecha de Registro", datetime.date.today())

# --- PESTAÑA 1: ENTRENAMIENTO ---
with tab1:
    st.subheader("Registro de Sesión")
    with st.form("form_entrenamiento"):
        col1, col2 = st.columns(2)
        with col1:
            dia = st.selectbox("Día de la semana", ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"])
            tipo_entrenamiento = st.selectbox("Tipo de Entrenamiento", [
                "Apnea Dinámica (DYN)", "Apnea Estática (STA)", "Apnea Profundidad (CWT/FIM)", 
                "Natación/Cardio", "Gimnasio/Fuerza", "Estiramiento/Yoga", "Descanso"
            ])
        with col2:
            duracion = st.number_input("Duración (minutos)", min_value=0, step=15)
            frecuencia_cardiaca = st.number_input("Frecuencia Cardíaca Promedio (ppm)", min_value=0)
            
        st.markdown("**Métricas Específicas (Apnea)**")
        col3, col4 = st.columns(2)
        with col3:
            distancia_total = st.number_input("Distancia Total (metros)", min_value=0)
            mejor_marca_tiempo = st.text_input("Mejor Marca (Tiempo) - ej. 3:45", "")
        with col4:
            mejor_marca_distancia = st.number_input("Mejor Marca (Distancia) (metros)", min_value=0)
            co2_tolerance = st.slider("Tolerancia al CO2 percibida", 1, 10, 5)
            
        observaciones_ent = st.text_area("Observaciones / Sensaciones de la sesión")
        
        submit_entrenamiento = st.form_submit_button("Guardar Entrenamiento", type="primary")

    if submit_entrenamiento:
        nuevo_registro_ent = pd.DataFrame({
            "Fecha": [fecha_hoy.strftime("%Y-%m-%d")],
            "Día": [dia],
            "Tipo de Entrenamiento": [tipo_entrenamiento],
            "Duración (min)": [duracion],
            "FC Promedio": [frecuencia_cardiaca],
            "Distancia Total (m)": [distancia_total],
            "Mejor Marca (Tiempo)": [mejor_marca_tiempo],
            "Mejor Marca (Distancia)": [mejor_marca_distancia],
            "Tolerancia CO2": [co2_tolerance],
            "Observaciones": [observaciones_ent]
        })
        df_ent = pd.concat([df_ent, nuevo_registro_ent], ignore_index=True)
        if guardar_datos(df_ent, df_ali, df_cheq):
            st.success("✅ Entrenamiento guardado con éxito.")
            st.dataframe(df_ent.tail(1))

# --- PESTAÑA 2: ALIMENTACIÓN ---
with tab2:
    st.subheader("Diario Nutricional")
    with st.form("form_alimentacion"):
        desayuno = st.text_area("Desayuno", placeholder="Ej: Avena con frutas, 2 huevos revueltos...")
        almuerzo = st.text_area("Almuerzo", placeholder="Ej: Pechuga de pollo, arroz integral, ensalada...")
        cena = st.text_area("Cena", placeholder="Ej: Pescado al horno, vegetales...")
        snacks = st.text_input("Snacks / Suplementos", placeholder="Ej: Batido de proteína, almendras...")
        
        col1, col2 = st.columns(2)
        with col1:
            hidratacion = st.number_input("Hidratación (Litros)", min_value=0.0, step=0.5, value=2.0)
        with col2:
            calidad_digestion = st.selectbox("Calidad de Digestión", ["Excelente", "Buena", "Regular", "Pesada"])
            
        submit_alimentacion = st.form_submit_button("Guardar Alimentación", type="primary")

    if submit_alimentacion:
        nuevo_registro_ali = pd.DataFrame({
            "Fecha": [fecha_hoy.strftime("%Y-%m-%d")],
            "Desayuno": [desayuno],
            "Almuerzo": [almuerzo],
            "Cena": [cena],
            "Snacks/Suplementos": [snacks],
            "Hidratación (L)": [hidratacion],
            "Calidad Digestión": [calidad_digestion]
        })
        df_ali = pd.concat([df_ali, nuevo_registro_ali], ignore_index=True)
        if guardar_datos(df_ent, df_ali, df_cheq):
            st.success("✅ Alimentación guardada con éxito.")
            st.dataframe(df_ali.tail(1))

# --- PESTAÑA 3: CHEQUEO DIARIO ---
with tab3:
    st.subheader("Métricas de Bienestar")
    with st.form("form_chequeo"):
        st.markdown("**Evaluación Subjetiva (1 = Muy Pobre, 10 = Excelente)**")
        col1, col2 = st.columns(2)
        with col1:
            horas_sueno = st.number_input("Horas de Sueño", min_value=0.0, step=0.5, value=7.5)
            calidad_sueno = st.slider("Calidad del Sueño", 1, 10, 7)
            nivel_energia_manana = st.slider("Energía al Despertar", 1, 10, 7)
        with col2:
            nivel_estres = st.slider("Nivel de Estrés Perceptual", 1, 10, 3)
            recuperacion_muscular = st.slider("Recuperación Muscular", 1, 10, 8)
            motivacion = st.slider("Motivación para Entrenar", 1, 10, 8)
            
        st.markdown("**Métricas Objetivas (Opcional)**")
        col3, col4 = st.columns(2)
        with col3:
            peso_matutino = st.number_input("Peso Matutino (kg)", min_value=0.0, step=0.1)
        with col4:
            fc_reposo = st.number_input("FC en Reposo (ppm)", min_value=0)
            
        notas_chequeo = st.text_area("Notas adicionales del día", placeholder="Sensaciones generales, molestias, logros...")
        
        submit_chequeo = st.form_submit_button("Guardar Chequeo Diario", type="primary")

    if submit_chequeo:
        nuevo_registro_cheq = pd.DataFrame({
            "Fecha": [fecha_hoy.strftime("%Y-%m-%d")],
            "Horas Sueño": [horas_sueno],
            "Calidad Sueño": [calidad_sueno],
            "Energía Mañana": [nivel_energia_manana],
            "Nivel Estrés": [nivel_estres],
            "Recuperación Muscular": [recuperacion_muscular],
            "Motivación": [motivacion],
            "Peso (kg)": [peso_matutino],
            "FC Reposo": [fc_reposo],
            "Notas Adicionales": [notas_chequeo]
        })
        df_cheq = pd.concat([df_cheq, nuevo_registro_cheq], ignore_index=True)
        if guardar_datos(df_ent, df_ali, df_cheq):
            st.success("✅ Chequeo Diario guardado con éxito.")
            st.dataframe(df_cheq.tail(1))
