import streamlit as st
import pandas as pd
from fpdf import FPDF

st.set_page_config(page_title="Brochure Académico", layout="wide")
st.title("📘 Automatización: Promoción de Evento Académico con IA")

uploaded_file = st.file_uploader("Sube el dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Análisis de Autores")
    if "Authors" in df.columns:
        freq = df["Authors"].value_counts()
        st.write(freq)

        top_authors = freq.head(3)
        st.success(f"Autores principales: {', '.join(top_authors.index)}")
