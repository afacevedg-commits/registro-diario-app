import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("Plan Maestro - Agosto")

archivo = "Plan Maestro Integrado - Entrenamiento, Alimentación y Chequeo Diario (Agosto 2026).xlsx"

# Leer el archivo exacto sin inventar columnas
try:
    df = pd.read_excel(archivo)
except Exception as e:
    st.error(f"Error cargando el archivo: {e}")
    st.stop()

st.write("Visualiza tu plan y edita directamente las celdas para marcar tus tareas. Al terminar, presiona Guardar.")

# Mostrar el Excel real como una tabla editable
df_editado = st.data_editor(df, use_container_width=True, hide_index=True)

if st.button("Guardar Cambios", type="primary"):
    try:
        # Guardar sobre el mismo archivo
        df_editado.to_excel(archivo, index=False)
        st.success("¡Archivo actualizado correctamente!")
    except Exception as e:
        st.error(f"Error al guardar: {e}")
