import streamlit as st
import pandas as pd
import datetime
import os

st.title("Registro Diario: Plan Maestro Integrado")
st.subheader("Agosto 2026")

archivo = "Plan Maestro Integrado - Entrenamiento, Alimentación y Chequeo Diario (Agosto 2026).xlsx"

# Leer el archivo Excel
if os.path.exists(archivo):
    df = pd.read_excel(archivo)
else:
    df = pd.DataFrame(columns=["Fecha", "Entrenamiento", "Alimentación", "Notas de Chequeo Diario"])

# Formulario
with st.form("registro_diario"):
    fecha = st.date_input("Fecha", datetime.date.today())
    entrenamiento = st.text_area("Detalles del Entrenamiento (Distancia, tiempos, sensaciones)")
    alimentacion = st.text_area("Registro de Alimentación")
    chequeo = st.slider("Nivel de Energía (1 al 10)", 1, 10, 5)
    
    submit = st.form_submit_button("Guardar Registro")

if submit:
    nuevo_registro = pd.DataFrame({
        "Fecha": [fecha],
        "Entrenamiento": [entrenamiento],
        "Alimentación": [alimentacion],
        "Notas de Chequeo Diario": [chequeo]
    })
    
    df = pd.concat([df, nuevo_registro], ignore_index=True)
    df.to_excel(archivo, index=False)
    st.success("¡Registro guardado con éxito!")

st.write("### Últimos ingresos")
st.dataframe(df.tail(3))
