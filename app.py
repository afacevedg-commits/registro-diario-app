import streamlit as st
import pandas as pd

# Configuración limpia estilo App móvil
st.set_page_config(page_title="Mi Plan", layout="centered", initial_sidebar_state="collapsed")

# Estilos CSS
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
    st.error("⚠️ Error al cargar el archivo. Verifica que tu Excel original esté subido en GitHub.")
    st.stop()

# 2. Selector de día
col_fecha = df.columns[0]
lista_dias = df[col_fecha].dropna().astype(str).unique()
dia_seleccionado = st.selectbox("📅 Selecciona la fecha:", lista_dias)

st.divider()

# 3. Obtener la fila exacta de ese día
idx = df[df[col_fecha].astype(str) == dia_seleccionado].index[0]
fila = df.loc[idx]

st.markdown(f"### Tareas para: {dia_seleccionado}")
st.write("Edita el texto para marcar lo que ya hiciste.")

# 4. Construir la interfaz (Tarjetas)
with st.form("registro_diario"):
    nuevos_datos = {}
    
    for col in df.columns[1:]:
        texto_actual = str(fila[col]) if pd.notna(fila[col]) else ""
        
        # Elimina los "nan" o "None" visualmente para que se vea limpio
        if texto_actual.lower() == "nan" or texto_actual.lower() == "none":
            texto_actual = ""
            
        nuevos_datos[col] = st.text_area(label=f"🔹 {col}", value=texto_actual, height=120)
    
    st.markdown("<br>", unsafe_allow_html=True)
    enviado = st.form_submit_button("✅ Guardar Cambios del Día", type="primary", use_container_width=True)
    
    if enviado:
        for col, nuevo_val in nuevos_datos.items():
            # ESTA ES LA LÍNEA CLAVE QUE SOLUCIONA EL ERROR:
            # Obliga a la columna a aceptar cualquier tipo de texto antes de inyectar el dato
            df[col] = df[col].astype(object) 
            
            # Ahora sí, guarda el dato
            df.at[idx, col] = nuevo_val
            
        try:
            df.to_excel(archivo, index=False)
            st.success("¡Plan actualizado correctamente!")
        except Exception as e:
            st.error(f"Error al guardar el archivo: {e}")
