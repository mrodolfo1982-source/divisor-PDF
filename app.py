import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Splitter", page_icon="✂️")

st.title("✂️ Divisor de Documentos PDF")
st.write("Sube un archivo y añade tantos rangos como necesites.")

# Inicializar el número de rangos en la sesión si no existe
if 'num_rangos' not in st.session_state:
    st.session_state.num_rangos = 1

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.info(f"El documento tiene {total_pages} páginas.")

    # Lista para guardar los valores de cada fila
    rangos_seleccionados = []

    # Generar las filas dinámicamente
    for i in range(st.session_state.num_rangos):
        st.write(f"**Rango {i+1}**")
        col1, col2 = st.columns(2)
        with col1:
            inicio = st.number_input(f"Página de inicio", min_value=1, max_value=total_pages, value=1, key=f"start_{i}")
        with col2:
            fin = st.number_input(f"Página de fin", min_value=1, max_value=total_pages, value=total_pages, key=f"end_{i}")
        rangos_seleccionados.append((inicio, fin))
        st.write("---")

    # Botones para agregar o quitar rangos
    col_btn1, col_btn2 = st.columns([1, 4])
    with col_btn1:
        if st.button("➕ Añadir"):
            st.session_state.num_rangos += 1
            st.rerun()
    with col_btn2:
        if st.button("➖ Quitar") and st.session_state.num_rangos > 1:
            st.session_state.num_rangos -= 1
            st.rerun()

    st.write("##") # Espaciado

    if st.button("Procesar y Dividir", type="primary", use_container_width=True):
        st.subheader("Archivos generados:")
        
        for idx, (inicio, fin) in enumerate(rangos_seleccionados):
            if inicio <= fin:
                writer = PdfWriter()
                for p in range(inicio - 1, fin):
                    writer.add_page(reader.pages[p])
                
                output = io.BytesIO()
                writer.write(output)
                output.seek(0)
                
                nombre = f"parte_{idx+1}_paginas_{inicio}_a_{fin}.pdf"
                st.download_button(
                    label=f"⬇️ Descargar {nombre}",
                    data=output,
                    file_name=nombre,
                    mime="application/pdf",
                    key=f"dl_{idx}"
                )
            else:
                st.error(f"En el Rango {idx+1}, el inicio no puede ser mayor que el fin.")
