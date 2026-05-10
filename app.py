import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Splitter", page_icon="✂️")

st.title("✂️ Divisor de Documentos PDF")
st.write("Sube un archivo, elige el rango de páginas y descarga tu nuevo PDF.")

# Cargador de archivos
uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    
    st.info(f"El documento tiene {total_pages} páginas.")

    # Interfaz para elegir el rango
    col1, col2 = st.columns(2)
    with col1:
        start_page = st.number_input("Página de inicio", min_value=1, max_value=total_pages, value=1)
    with col2:
        end_page = st.number_input("Página de fin", min_value=1, max_value=total_pages, value=total_pages)

    if st.button("Procesar y Dividir"):
        if start_page <= end_page:
            writer = PdfWriter()
            
            # Agregar las páginas seleccionadas
            for i in range(start_page - 1, end_page):
                writer.add_page(reader.pages[i])
            
            # Guardar en un buffer de memoria para la descarga
            output_pdf = io.BytesIO()
            writer.write(output_pdf)
            output_pdf.seek(0)
            
            st.success("¡PDF procesado con éxito!")
            
            st.download_button(
                label="Descargar PDF dividido",
                data=output_pdf,
                file_name=f"dividido_{start_page}_a_{end_page}.pdf",
                mime="application/pdf"
            )
        else:
            st.error("La página de inicio no puede ser mayor que la de fin.")
