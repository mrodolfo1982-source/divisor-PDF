import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Multi-Splitter", page_icon="✂️")

st.title("✂️ Divisor de Documentos PDF")
st.write("Sube tu archivo y define los grupos de páginas que quieres separar.")

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.info(f"El documento tiene {total_pages} páginas.")

    st.subheader("Configura tus rangos")
    user_input = st.text_input(
        "Ingresa los rangos separados por comas:",
        placeholder="Ejemplo: 1-5, 10-20, 35",
        help="Usa guiones para rangos y comas para separar archivos distintos."
    )

    # Añadimos el botón para procesar
    if st.button("Generar archivos de descarga"):
        if user_input:
            try:
                # Separamos la entrada por comas
                rangos = [r.strip() for r in user_input.split(",") if r.strip()]
                
                st.write("---")
                st.subheader("Archivos listos para descargar:")

                for index, rango in enumerate(rangos):
                    writer = PdfWriter()
                    
                    # Caso 1: Rango (ej. 1-10)
                    if "-" in rango:
                        partes = rango.split("-")
                        inicio = int(partes[0])
                        fin = int(partes[1])
                        
                        # Validamos límites para evitar errores
                        inicio = max(1, inicio)
                        fin = min(total_pages, fin)
                        
                        for i in range(inicio - 1, fin):
                            writer.add_page(reader.pages[i])
                        
                        nombre_archivo = f"paginas_{inicio}_a_{fin}.pdf"
                    
                    # Caso 2: Página única (ej. 5)
                    else:
                        pag = int(rango)
                        if 1 <= pag <= total_pages:
                            writer.add_page(reader.pages[pag - 1])
                        nombre_archivo = f"pagina_{pag}.pdf"

                    # Generar botón si hay páginas
                    if len(writer.pages) > 0:
                        output = io.BytesIO()
                        writer.write(output)
                        output.seek(0)
                        
                        st.download_button(
                            label=f"⬇️ Descargar {nombre_archivo}",
                            data=output,
                            file_name=nombre_archivo,
                            mime="application/pdf",
                            key=f"btn_{index}_{rango}" # Key única mejorada
                        )
                    else:
                        st.warning(f"El rango '{rango}' está fuera de los límites del PDF.")

            except ValueError:
                st.error("Formato incorrecto. Verifica que solo uses números, guiones y comas (ej. 1-5, 10).")
        else:
            st.warning("Por favor, escribe al menos un rango antes de presionar el botón.")
