import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Splitter", page_icon="✂️")

st.title("✂️ Divisor de Documentos PDF")
st.write("Configura tus rangos y descarga todos los archivos sin que desaparezcan.")

# --- INICIALIZAR ESTADOS ---
if 'num_rangos' not in st.session_state:
    st.session_state.num_rangos = 1
if 'archivos_listos' not in st.session_state:
    st.session_state.archivos_listos = []

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

# Si se sube un archivo nuevo, limpiamos los archivos generados anteriormente
if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.info(f"El documento tiene {total_pages} páginas.")

    # Sección de configuración de rangos
    rangos_input = []
    for i in range(st.session_state.num_rangos):
        st.write(f"**Rango {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            inicio = st.number_input(f"Inicio", min_value=1, max_value=total_pages, value=1, key=f"start_{i}")
        with col2:
            fin = st.number_input(f"Fin", min_value=1, max_value=total_pages, value=total_pages, key=f"end_{i}")
        rangos_input.append((inicio, fin))

    # Botones para gestionar filas
    col_a, col_b = st.columns([1, 4])
    with col_a:
        if st.button("➕ Añadir"):
            st.session_state.num_rangos += 1
            st.rerun()
    with col_b:
        if st.button("➖ Quitar") and st.session_state.num_rangos > 1:
            st.session_state.num_rangos -= 1
            st.rerun()

    st.write("---")

    # BOTÓN DE PROCESAR
    if st.button("Procesar y Preparar Descargas", type="primary"):
        # Limpiamos la lista previa para generar la nueva
        st.session_state.archivos_listos = []
        
        for idx, (inicio, fin) in enumerate(rangos_input):
            if inicio <= fin:
                writer = PdfWriter()
                for p in range(inicio - 1, fin):
                    writer.add_page(reader.pages[p])
                
                output = io.BytesIO()
                writer.write(output)
                output_data = output.getvalue() # Guardamos los bytes reales
                
                nombre = f"parte_{idx+1}_paginas_{inicio}_a_{fin}.pdf"
                st.session_state.archivos_listos.append({
                    "nombre": nombre,
                    "datos": output_data
                })
            else:
                st.error(f"Error en Rango {idx+1}: El inicio es mayor que el fin.")

    # MOSTRAR BOTONES DE DESCARGA (Si existen en memoria)
    if st.session_state.archivos_listos:
        st.subheader("📥 Descargas disponibles:")
        for idx, archivo in enumerate(st.session_state.archivos_listos):
            st.download_button(
                label=f"Descargar {archivo['nombre']}",
                data=archivo['datos'],
                file_name=archivo['nombre'],
                mime="application/pdf",
                key=f"download_{idx}_{archivo['nombre']}" # Key única para persistencia
            )
