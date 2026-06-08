streamlit
pandas
fpdf2
import streamlit as st
import pandas as pd
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Brochure Académico", layout="wide")

st.title("📘 Automatización: Promoción de Evento Académico con IA")

# --- SUBIR CSV ---
uploaded_file = st.file_uploader("Sube el dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Análisis de Autores")
    # Contar frecuencia de autores
    if "Authors" in df.columns:
        freq = df["Authors"].value_counts()
        st.write(freq)

        # Seleccionar los 3 principales
        top_authors = freq.head(3)
        st.success(f"Autores principales: {', '.join(top_authors.index)}")

        # --- ESTRATEGIA DEL EVENTO ---
        st.subheader("🎯 Estrategia de Promoción")
        st.markdown("""
        **Evento:** Conferencia Internacional de Machine Learning y Algoritmos Predictivos 2026  
        **Institución:** Universidad San Ignacio de Loyola (USIL) y Instituto San Ignacio de Loyola (ISIL)  
        **Sponsors:** Google Cloud, Microsoft, IBM  
        **Certificación:** 20 horas académicas emitidas por USIL e ISIL  
        **Cronograma de Promoción:**  
        - Junio 2026: Lanzamiento oficial  
        - Julio 2026: Inscripción temprana  
        - Agosto 2026: Agenda oficial  
        - Septiembre 2026: Conferencia Internacional  
        """)

        # --- GENERAR BROCHURE EN PDF ---
        st.subheader("📄 Generar Brochure en PDF")

        def generar_pdf(autores):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Conferencia Internacional de Machine Learning 2026", ln=True, align="C")

            pdf.set_font("Arial", '', 12)
            pdf.multi_cell(0, 10, f"Autores principales: {', '.join(autores)}")
            pdf.multi_cell(0, 10, "Institución: USIL & ISIL")
            pdf.multi_cell(0, 10, "Sponsors: Google Cloud, Microsoft, IBM")
            pdf.multi_cell(0, 10, "Certificación: 20 horas académicas")
            pdf.multi_cell(0, 10, "Cronograma: Junio - Septiembre 2026")

            pdf.output("Brochure_Academico.pdf")

        if st.button("Generar PDF"):
            generar_pdf(top_authors.index)
            st.success("✅ Brochure_Academico.pdf generado correctamente. Descárgalo desde tu carpeta de ejecución.")

    else:
        st.error("El CSV no contiene la columna 'Authors'. Verifica tu archivo.")

