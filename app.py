import streamlit as st
import pandas as pd

# Configuración limpia estilo App móvil
st.set_page_config(page_title="Mi Plan", layout="centered", initial_sidebar_state="collapsed")

# Estilos CSS para quitar bordes feos y hacer que parezca Asana
st.markdown("""
    <style>
    div[data-testid="stForm"] { border: none; padding: 0; }
    .stTextArea label { font-size: 1.15rem !important; color: #1E3A8A; font-weight: 600; margin-top: 10px;}
    </style>
""", unsafe_allow_html=True)

st.title("✅ Mi Día")

archivo = "Plan Maestro Integrado - Entrenamiento, Alimentación y Chequeo Diario (Agosto 2026).xlsx"

# 1. Cargar tu Excel original
try:
    df = pd.read_excel(archivo)
except Exception as e:
    st.error("⚠️ Sube tu Excel original a GitHub. El actual sigue dañado por los códigos viejos.")
    st.stop()

# 2. Selector de día (Toma la primera columna de tu Excel)
col_fecha = df.columns[0]
lista_dias = df[col_fecha].dropna().astype(str).unique()
dia_seleccionado = st.selectbox("📅 Selecciona la fecha:", lista_dias)

st.divider()

# 3. Obtener la fila exacta de ese día
idx = df[df[col_fecha].astype(str) == dia_seleccionado].index[0]
fila = df.loc[idx]

st.markdown(f"### Tareas para: {dia_seleccionado}")
st.write("Edita el texto para marcar con 'X' lo que ya hiciste.")

# 4. Construir la interfaz limpia (Tarjetas)
with st.form("registro_diario"):
    nuevos_datos = {}
    
    # Recorre cada columna de tu Excel (ignorando la fecha) y crea un bloque estilo "Tarea"
    for col in df.columns[1:]:
        texto_actual = str(fila[col]) if pd.notna(fila[col]) else ""
        
        # Genera un cuadro de texto amplio por cada tarea
        nuevos_datos[col] = st.text_area(label=f"🔹 {col}", value=texto_actual, height=120)
    
    st.markdown("<br>", unsafe_allow_html=True)
    enviado = st.form_submit_button("✅ Guardar Cambios del Día", type="primary", use_container_width=True)
    
    # Al guardar, actualiza el archivo
    if enviado:
        for col, nuevo_val in nuevos_datos.items():
            df.at[idx, col] = nuevo_val
        df.to_excel(archivo, index=False)
        st.success("¡Plan actualizado correctamente!")
