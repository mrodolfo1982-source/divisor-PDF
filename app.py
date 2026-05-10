import streamlit as st
from pypdf import PdfReader, PdfWriter
import io

st.set_page_config(page_title="PDF Multi-Splitter", page_icon="✂️")

st.title("✂️ Divisor de Documentos PDF")
st.write("Sube tu archivo y define los grupos de páginas que quieres separar en archivos distintos.")

uploaded_file = st.file_uploader("Elige un archivo PDF", type="pdf")

if uploaded_file:
    reader = PdfReader(uploaded_file)
    total_pages = len(reader.pages)
    st.info(f"El documento tiene {total_pages} páginas.")

    # Campo para ingresar los rangos
    st.subheader("Configura tus rangos")
    user_input = st.text_input(
        "Ingresa los rangos separados por comas (Ejemplo: 1-5, 10-20, 35):",
        placeholder="1-5, 10-20, 35"
    )

    if user_input:
        try:
            # Separamos la entrada por comas
            rangos = [r.strip() for r in user_input.split(",")]
            
            st.write("---")
            st.subheader("Archivos generados:")

            for rango in rangos:
                writer = PdfWriter()
                
                # Caso 1: Es un rango definido por un guion (ej. 1-10)
                if "-" in rango:
                    inicio, fin = map(int, rango.split("-"))
                    # Validamos límites
                    inicio = max(1, inicio)
                    fin = min(total_pages, fin)
                    
                    for i in range(inicio - 1, fin):
                        writer.add_page(reader.pages[i])
                    
                    nombre_archivo = f"paginas_{inicio}_a_{fin}.pdf"
                
                # Caso 2: Es una sola página (ej. 5)
                else:
                    pag = int(rango)
                    if 1 <= pag <= total_pages:
                        writer.add_page(reader.pages[pag - 1])
                    nombre_archivo = f"pagina_{pag}.pdf"

                # Si el writer tiene páginas, creamos el botón de descarga
                if len(writer.pages) > 0:
                    output = io.BytesIO()
                    writer.write(output)
                    output.seek(0)
                    
                    st.download_button(
                        label=f"⬇️ Descargar {nombre_archivo}",
                        data=output,
                        file_name=nombre_archivo,
                        mime="application/pdf",
                        key=f"btn_{rango}" # Key única para Streamlit
                    )

        except ValueError:
            st.error("Formato incorrecto. Asegúrate de usar números y guiones (ej. 1-5, 8, 10-12).")
        except Exception as e:
            st.error(f"Ocurrió un error: {e}")
