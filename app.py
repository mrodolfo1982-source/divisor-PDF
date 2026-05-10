import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Multi-Splitter", page_icon="✂️")

st.title("✂️ Divisor de PDF (Múltiples Rangos)")
st.write("Escribe los rangos que quieras extraer (ejemplo: **1-3, 5, 10-12**)")

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.info(f"El documento tiene {total_pages} páginas.")

    # Entrada de texto para los rangos
    user_input = st.text_input("Introduce los rangos o páginas individuales:", placeholder="Ej: 1-3, 5, 7-10")

    if st.button("Procesar y Dividir"):
        if user_input:
            try:
                writer = PdfWriter()
                pages_to_add = set() # Usamos un set para evitar páginas duplicadas

                # Limpiamos y separamos la entrada por comas
                parts = [p.strip() for p in user_input.split(",")]

                for part in parts:
                    if "-" in part:
                        # Es un rango (ej: 1-5)
                        start, end = map(int, part.split("-"))
                        for i in range(start, end + 1):
                            if 1 <= i <= total_pages:
                                pages_to_add.add(i - 1)
                    else:
                        # Es una página única (ej: 5)
                        p = int(part)
                        if 1 <= p <= total_pages:
                            pages_to_add.add(p - 1)

                # Ordenar las páginas y añadirlas al documento
                for page_num in sorted(list(pages_to_add)):
                    writer.add_page(reader.pages[page_num])

                if len(writer.pages) > 0:
                    output_pdf = io.BytesIO()
                    writer.write(output_pdf)
                    output_pdf.seek(0)

                    st.success(f"¡Listo! Se extrajeron {len(writer.pages)} páginas.")
                    st.download_button(
                        label="⬇️ Descargar PDF resultante",
                        data=output_pdf,
                        file_name="pdf_personalizado.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.warning("No se seleccionaron páginas válidas dentro del rango del documento.")

            except Exception as e:
                st.error(f"Hubo un error con el formato de los rangos. Revisa que solo uses números, guiones y comas.")
        else:
            st.error("Por favor, ingresa al menos una página o rango.")
