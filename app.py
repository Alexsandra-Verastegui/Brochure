import streamlit as st
import pandas as pd
import os

from PIL import Image, ImageDraw, ImageFont
from fpdf import FPDF

# =========================
# CONFIGURACIÓN
# =========================
st.set_page_config(page_title="Brochure Académico", layout="wide")
st.title("📘 Automatización: Promoción de Evento Académico con IA")

os.makedirs("generated", exist_ok=True)

# =========================
# FUNCIÓN BROCHURE
# =========================
def generar_brochure(top_authors):

    ancho = 1800
    alto = 1000

    fondo = Image.new("RGB", (ancho, alto), "#062743")
    draw = ImageDraw.Draw(fondo)

    # Fondo tipo tecnológico
    for x in range(0, ancho, 50):
        draw.line((x, 0, x, alto), fill=(20, 60, 90), width=1)

    for y in range(0, alto, 50):
        draw.line((0, y, ancho, y), fill=(20, 60, 90), width=1)

    # =========================
    # CARGAR IMÁGENES
    # =========================
    try:
        robot = Image.open("assets/robot_ai.png").convert("RGBA")
        robot = robot.resize((500, 700))

        usil = Image.open("assets/logo_usil.jpg")
        usil = usil.resize((120, 120))

        isil = Image.open("assets/logo_isil.png")
        isil = isil.resize((120, 120))

        google = Image.open("assets/google.png")
        google = google.resize((150, 60))

        microsoft = Image.open("assets/microsoft.png")
        microsoft = microsoft.resize((150, 60))

        ibm = Image.open("assets/ibm.png")
        ibm = ibm.resize((120, 60))

    except Exception as e:
        st.error(f"Error cargando imágenes: {e}")
        return None

    # =========================
    # LOGOS
    # =========================
    draw.rounded_rectangle(
        (10, 10, 320, 150),
        radius=20,
        fill="#F0F0F0"
    )

    fondo.paste(usil, (25, 20))
    fondo.paste(isil, (160, 20))

    # =========================
    # ROBOT
    # =========================
    fondo.paste(robot, (600, 120), robot)

    # =========================
    # FUENTES
    # =========================
    try:
        titulo = ImageFont.truetype("arial.ttf", 65)
        subtitulo = ImageFont.truetype("arial.ttf", 28)
        texto = ImageFont.truetype("arial.ttf", 20)
    except:
        titulo = ImageFont.load_default()
        subtitulo = ImageFont.load_default()
        texto = ImageFont.load_default()

    # =========================
    # TÍTULO
    # =========================
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
        (30, 310),
        "& ALGORITMOS PREDICTIVOS",
        fill="#00BFFF",
        font=subtitulo
    )

    draw.text(
        (30, 360),
        "2026",
        fill="white",
        font=subtitulo
    )

    descripcion = """
Explora. Aprende. Conecta. Transforma.

Un encuentro académico internacional
basado en análisis bibliométrico para
identificar a los investigadores más
influyentes en Machine Learning,
Inteligencia Artificial y Ciencia de Datos.
"""

    draw.multiline_text(
        (30, 410),
        descripcion,
        fill="white",
        font=texto,
        spacing=6
    )

    # =========================
    # AUTORES
    # =========================
    draw.text(
        (30, 560),
        "EXPOSITORES PRINCIPALES",
        fill="#00BFFF",
        font=subtitulo
    )

    x = 30
    y = 620

    for _, row in top_authors.iterrows():

        draw.rounded_rectangle(
            (x, y, x + 300, y + 220),
            radius=15,
            outline="#00BFFF",
            width=3
        )

        draw.text(
            (x + 15, y + 20),
            str(row["Authors"]),
            fill="#00BFFF",
            font=subtitulo
        )

        draw.text(
            (x + 15, y + 80),
            f"Publicaciones: {row['publicaciones']}",
            fill="white",
            font=texto
        )

        draw.text(
            (x + 15, y + 120),
            f"Citas: {row['citas']}",
            fill="white",
            font=texto
        )

        draw.text(
            (x + 15, y + 160),
            "Investigador destacado",
            fill="white",
            font=texto
        )

        x += 320

    # =========================
    # AGENDA
    # =========================
    draw.text(
        (1150, 60),
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

    yy = 120

    for item in agenda:

        draw.rounded_rectangle(
            (1100, yy, 1700, yy + 45),
            radius=10,
            outline="#00BFFF"
        )

        draw.text(
            (1120, yy + 10),
            item,
            fill="white",
            font=texto
        )

        yy += 60

    # =========================
    # CERTIFICACIÓN
    # =========================
    draw.rounded_rectangle(
        (1100, 520, 1700, 650),
        radius=15,
        outline="#00BFFF",
        width=3
    )

    draw.text(
        (1130, 550),
        "CERTIFICACIÓN",
        fill="#00BFFF",
        font=subtitulo
    )

    draw.text(
        (1130, 600),
        "20 HORAS ACADÉMICAS",
        fill="white",
        font=texto
    )

    # =========================
    # FRASE
    # =========================
    draw.rounded_rectangle(
        (1100, 700, 1700, 860),
        radius=20,
        fill="#F2F2F2"
    )

    draw.multiline_text(
        (1150, 740),
        '"La inteligencia artificial\nno es el futuro,\nes el presente."',
        fill="black",
        font=subtitulo
    )

    # =========================
    # SPONSORS
    # =========================
    draw.text(
        (30, 900),
        "CON EL RESPALDO DE",
        fill="white",
        font=subtitulo
    )

    fondo.paste(google, (250, 900))
    fondo.paste(microsoft, (430, 900))
    fondo.paste(ibm, (640, 900))

    brochure = "generated/brochure.png"
    fondo.save(brochure)

    return brochure

# =========================
# PDF
# =========================
def generar_pdf_desde_imagen(imagen):

    pdf = FPDF("L", "mm", "A4")
    pdf.add_page()
    pdf.image(imagen, x=0, y=0, w=297)

    archivo = "Brochure_Academico.pdf"
    pdf.output(archivo)

    return archivo

# =========================
# SUBIR CSV
# =========================
uploaded_file = st.file_uploader(
    "Sube el dataset CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    if "Authors" in df.columns and "Cited by" in df.columns:

        df["Authors"] = df["Authors"].str.split(";")

        df_exploded = df.explode("Authors")
        df_exploded["Authors"] = df_exploded["Authors"].str.strip()

        resumen = df_exploded.groupby("Authors").agg(
            publicaciones=("Authors", "count"),
            citas=("Cited by", "sum")
        ).reset_index()

        resumen = resumen.sort_values(
            by=["publicaciones", "citas"],
            ascending=[False, False]
        )

        st.dataframe(resumen)

        top_authors = resumen.head(3)

        st.success(
            f"Autores seleccionados: {', '.join(top_authors['Authors'])}"
        )

        if st.button("Generar Brochure PDF"):

            brochure = generar_brochure(top_authors)

            st.image(
                brochure,
                caption="Vista previa",
                use_container_width=True
            )

            pdf_file = generar_pdf_desde_imagen(brochure)

            with open(pdf_file, "rb") as f:

                st.download_button(
                    "📥 Descargar PDF",
                    f,
                    file_name="Brochure_Academico.pdf",
                    mime="application/pdf"
                )

    else:
        st.error(
            "El CSV debe contener las columnas Authors y Cited by."
        )
