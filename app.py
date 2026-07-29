import streamlit as st
import pandas as pd

st.set_page_config(page_title="Plan Maestro Integrado", layout="wide")
st.title("Plan Maestro Integrado - Agosto")

archivo = "Plan Maestro Integrado - Entrenamiento, Alimentación y Chequeo Diario (Agosto 2026).xlsx"

try:
    # Lee la primera hoja del archivo, sin importar cómo se llame (Sheet1, Plan Maestro, etc.)
    xls = pd.ExcelFile(archivo)
    nombre_hoja = xls.sheet_names[0]
    df = pd.read_excel(xls, sheet_name=nombre_hoja)
except Exception as e:
    st.error(f"Error al cargar el archivo: {e}")
    st.stop()

st.write("Edita directamente las celdas (por ejemplo en 'Chequeo Garmin') y presiona Guardar.")

# Muestra tu Excel exacto en la web para que lo edites directamente
df_editado = st.data_editor(df, use_container_width=True, num_rows="dynamic")

if st.button("Guardar Cambios", type="primary"):
    try:
        # Guarda los cambios sobre el mismo archivo respetando el nombre de tu hoja
        df_editado.to_excel(archivo, index=False, sheet_name=nombre_hoja)
        st.success("¡Registro actualizado con éxito!")
    except Exception as e:
        st.error(f"Hubo un error al guardar: {e}")
