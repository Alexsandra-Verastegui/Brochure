import streamlit as st
import pandas as pd
import os

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

# --- CONFIGURACIÓN DE LA APP ---
st.set_page_config(page_title="Brochure Académico", layout="wide")
st.title("📘 Automatización: Promoción de Evento Académico con IA")

# --- SUBIR CSV ---
uploaded_file = st.file_uploader("Sube el dataset (CSV con columnas Authors y Cited by)", type=["csv"])

os.makedirs("generated", exist_ok=True)

def generar_brochure(top_authors):

    fondo = Image.new("RGB", (1800, 1000), "#062743")
    draw = ImageDraw.Draw(fondo)

    for x in range(0, 1800, 50):
        draw.line((x, 0, x, 1000), fill=(20, 60, 90), width=1)

    for y in range(0, 1000, 50):
        draw.line((0, y, 1800, y), fill=(20, 60, 90), width=1)

    # ---------- IMÁGENES ----------
    robot = Image.open("assets/robot_ai.png").convert("RGBA")
    robot = robot.resize((720,900))

    usil = Image.open("assets/logo_usil.jpg")
    usil = usil.resize((130, 130))

    isil = Image.open("assets/logo_isil.png")
    isil = isil.resize((130, 130))

    google = Image.open("assets/google.png")
    google = google.resize((150, 60))

    microsoft = Image.open("assets/microsoft.png")
    microsoft = microsoft.resize((150, 60))

    ibm = Image.open("assets/ibm.png")
    ibm = ibm.resize((120, 60))

    fondo.paste(usil, (25, 20))
    fondo.paste(isil, (170, 20))
    fondo.paste(robot,(500,80),robot)

    draw.rounded_rectangle(
    (10, 10, 340, 150),
    radius=20,
    fill="#EAEAEA"
)
    
    # ---------- FUENTES ----------
    try:
        titulo = ImageFont.truetype("arial.ttf", 55)
        subtitulo = ImageFont.truetype("arial.ttf", 28)
        texto = ImageFont.truetype("arial.ttf", 20)
    except:
        titulo = ImageFont.load_default()
        subtitulo = ImageFont.load_default()
        texto = ImageFont.load_default()

    # ---------- TÍTULO ----------
    draw.text(
        (30, 180),
        "CONFERENCIA INTERNACIONAL DE",
        fill="white",
        font=subtitulo
    )

    draw.text(
        (30, 230),
        "MACHINE LEARNING",
        fill="#00BFFF",
        font=titulo
    )

    draw.text(
        (30, 300),
        "& ALGORITMOS PREDICTIVOS",
        fill="#00BFFF",
        font=titulo
    )

    draw.text(
        (30, 380),
        "2026",
        fill="white",
        font=subtitulo
    )

    # ---------- AUTORES ----------
    draw.text(
        (30, 450),
        "EXPOSITORES PRINCIPALES",
        fill="#00BFFF",
        font=subtitulo
    )

    x = 30
    y = 620

    for _, row in top_authors.iterrows():

        draw.rounded_rectangle(
            (x, y, x+330, y+260),
            radius=15,
            outline="#00BFFF",
            width=3
        )

        draw.text(
            (x+15, y+15),
            str(row["Authors"]),
            fill="#00BFFF",
            font=subtitulo
        )

        draw.text(
            (x+15, y+80),
            f"Publicaciones: {row['publicaciones']}",
            fill="white",
            font=texto
        )

        draw.text(
            (x+15, y+120),
            f"Citas: {row['citas']}",
            fill="white",
            font=texto
        )

        draw.text(
            (x+15, y+160),
            "Investigador destacado",
            fill="white",
            font=texto
        )

        x += 300

    # ---------- AGENDA ----------
    draw.text(
        (1050, 70),
        "AGENDA ACADÉMICA",
        fill="#00BFFF",
        font=subtitulo
    )

    agenda = [
        "15 Abril - Inauguración",
        "15 Abril - Conferencia Principal",
        "16 Abril - IA y Ciencia de Datos",
        "16 Abril - Casos de Éxito",
        "17 Abril - Tendencias Futuras",
        "17 Abril - Clausura"
    ]

    yy = 130

    for item in agenda:

        draw.rounded_rectangle(
            (1020, yy, 1550, yy+45),
            radius=10,
            outline="#00BFFF"
        )

        draw.text(
            (1040, yy+10),
            item,
            fill="white",
            font=texto
        )

        yy += 60

    # ---------- CERTIFICACIÓN ----------
    draw.rounded_rectangle(
        (1020, 520, 1550, 650),
        radius=15,
        outline="#00BFFF",
        width=3
    )

    draw.text(
        (1050, 550),
        "CERTIFICACIÓN",
        fill="#00BFFF",
        font=subtitulo
    )

    draw.text(
        (1050, 600),
        "20 HORAS ACADÉMICAS",
        fill="white",
        font=texto
    )

    # ---------- SPONSORS ----------
    draw.text(
        (30, 790),
        "CON EL RESPALDO DE",
        fill="white",
        font=subtitulo
    )

    fondo.paste(google, (30, 840))
    fondo.paste(microsoft, (220, 840))
    fondo.paste(ibm, (430, 840))

    brochure = "generated/brochure.png"
    fondo.save(brochure)

    return brochure

def generar_pdf_desde_imagen(imagen):

    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()

    pdf.image(
        imagen,
        x=0,
        y=0,
        w=297
    )

    archivo = "Brochure_Academico.pdf"
    pdf.output(archivo)

    return archivo

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Análisis de Autores")

    if "Authors" in df.columns and "Cited by" in df.columns:
        # Separar autores cuando vienen juntos con ;
        df["Authors"] = df["Authors"].str.split(";")

        # Expandir filas para que cada autor quede en una fila
        df_exploded = df.explode("Authors")
        df_exploded["Authors"] = df_exploded["Authors"].str.strip()

        # Agrupar por autor y calcular publicaciones y citas
        resumen = df_exploded.groupby("Authors").agg(
            publicaciones=("Authors", "count"),
            citas=("Cited by", "sum")
        ).reset_index()

        # Filtrar autores con más de 1 publicación
        resumen_filtrado = resumen[resumen["publicaciones"] > 1]

        # Ordenar por publicaciones y luego por citas
        resumen_ordenado = resumen_filtrado.sort_values(
            by=["publicaciones", "citas"],
            ascending=[False, False]
        )

        st.write(resumen_ordenado)

        # Seleccionar los 3 principales automáticamente
        top_authors = resumen_ordenado.head(3)
        st.success(f"Autores principales: {', '.join(top_authors['Authors'])}")

    # --- GENERAR BROCHURE EN PDF ---
    st.subheader("📄 Generar Brochure en PDF")

    if st.button("Generar PDF"):

        brochure = generar_brochure(top_authors)

        st.image(
            brochure,
            caption="Vista previa del brochure",
            use_container_width=True
        )

        pdf_file = generar_pdf_desde_imagen(brochure)

        with open(pdf_file, "rb") as f:

            st.download_button(
                label="📥 Descargar Brochure",
                data=f,
                file_name="Brochure_Academico.pdf",
                mime="application/pdf"
            )

        st.success("✅ Brochure generado correctamente.")
        
