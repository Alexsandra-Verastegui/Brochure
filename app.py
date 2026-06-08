import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Brochure Académico", layout="wide")
st.title("📘 Automatización: Promoción de Evento Académico con IA")

# --- SUBIR CSV ---
uploaded_file = st.file_uploader("Sube el dataset (CSV con columnas Authors y Cited by)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Análisis de Autores")

    # Verificamos que existan las columnas necesarias
    if "Authors" in df.columns and "Cited by" in df.columns:
        # Agrupar por autor y calcular publicaciones y citas
        resumen = df.groupby("Authors").agg(
            publicaciones=("Authors", "count"),
            citas=("Cited by", "sum")
        ).reset_index()

        # Ordenar primero por publicaciones y luego por citas
        resumen_ordenado = resumen.sort_values(
            by=["publicaciones", "citas"],
            ascending=[False, False]
        )

        st.write(resumen_ordenado)

        # Seleccionar los 3 principales
        top_authors = resumen_ordenado.head(3)
        st.success(f"Autores principales: {', '.join(top_authors['Authors'])}")

        # --- GENERAR BROCHURE EN PDF ---
        st.subheader("📄 Generar Brochure en PDF")

        def generar_pdf(df_top):
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, "Conferencia Internacional de Machine Learning 2026", ln=True, align="C")

            pdf.set_font("Arial", '', 12)
            for _, row in df_top.iterrows():
                pdf.multi_cell(0, 10, f"{row['Authors']} - {row['publicaciones']} publicaciones, {row['citas']} citas")

            pdf.multi_cell(0, 10, "Institución: USIL & ISIL")
            pdf.multi_cell(0, 10, "Sponsors: Google Cloud, Microsoft, IBM")
            pdf.multi_cell(0, 10, "Certificación: 20 horas académicas")
            pdf.multi_cell(0, 10, "Cronograma: Junio - Septiembre 2026")

            pdf.output("Brochure_Academico.pdf")

        if st.button("Generar PDF"):
            generar_pdf(top_authors)
            st.success("✅ Brochure_Academico.pdf generado correctamente. Descárgalo desde tu carpeta de ejecución.")

    else:
        st.error("El CSV debe contener las columnas 'Authors' y 'Cited by'.")
