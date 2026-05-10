import streamlit as st
from pypdf import PdfReader, PdfWriter, PdfMerger
import io

st.set_page_config(page_title="Herramientas PDF", page_icon="📄")

st.title("🛠️ Herramientas PDF")
st.write("Divide o une tus documentos de forma rápida y segura.")

# Creamos dos pestañas
tab1, tab2 = st.tabs(["✂️ Dividir PDF", "📂 Unir PDFs"])

# --- PESTAÑA 1: DIVIDIR ---
with tab1:
    st.header("Dividir Documento")
    uploaded_file = st.file_uploader("Sube el PDF que quieres recortar", type="pdf", key="splitter")

    if uploaded_file:
        reader = PdfReader(uploaded_file)
        total_pages = len(reader.pages)
        st.info(f"Páginas totales: {total_pages}")

        col1, col2 = st.columns(2)
        with col1:
            start_page = st.number_input("Desde página", min_value=1, max_value=total_pages, value=1)
        with col2:
            end_page = st.number_input("Hasta página", min_value=1, max_value=total_pages, value=total_pages)

        if st.button("Generar PDF Dividido"):
            if start_page <= end_page:
                writer = PdfWriter()
                for i in range(start_page - 1, end_page):
                    writer.add_page(reader.pages[i])
                
                output_pdf = io.BytesIO()
                writer.write(output_pdf)
                output_pdf.seek(0)

                st.download_button(
                    label="⬇️ Descargar Selección",
                    data=output_pdf,
                    file_name="pdf_dividido.pdf",
                    mime="application/pdf"
                )
            else:
                st.error("El rango es inválido.")

# --- PESTAÑA 2: UNIR ---
with tab2:
    st.header("Unir Varios Documentos")
    uploaded_files = st.file_uploader("Sube dos o más archivos PDF", type="pdf", accept_multiple_files=True, key="merger")

    if uploaded_files:
        st.write(f"Archivos listos para unir: {len(uploaded_files)}")
        
        # Mostrar nombres de archivos cargados
        for f in uploaded_files:
            st.text(f"• {f.name}")

        if len(uploaded_files) >= 2:
            if st.button("Combinar Archivos"):
                merger = PdfMerger()
                for pdf in uploaded_files:
                    merger.append(pdf)
                
                output_merge = io.BytesIO()
                merger.write(output_merge)
                output_merge.seek(0)

                st.success("¡Unión completada!")
                st.download_button(
                    label="⬇️ Descargar PDF Combinado",
                    data=output_merge,
                    file_name="pdf_unido.pdf",
                    mime="application/pdf"
                )
        else:
            st.warning("Por favor, sube al menos dos archivos para unirlos.")
