from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib import colors
from datetime import datetime


def _format_cell_value(val):
    """Formatea valores: fechas -> dd/mm/YYYY, NaN/NaT -> '', otros -> str."""
    if val is None:
        return ""

    if isinstance(val, (datetime,)):
        return val.strftime("%d/%m/%Y")
    # pandas Timestamp (avoid importing pandas here)
    try:
        # pandas Timestamp has "to_pydatetime" and "strftime"
        if hasattr(val, "to_pydatetime"):
            return val.to_pydatetime().strftime("%d/%m/%Y")
    except Exception:
        pass
    # numeric or string
    try:
        # treat NaN
        import math
        if isinstance(val, float) and math.isnan(val):
            return ""
    except Exception:
        pass
    return str(val)

def _df_to_table_story(df, styles):
    """Convierte un DataFrame a una tabla básica de ReportLab.
       SIN semáforo ni estilos condicionales.
    """

    # Si el dataframe viene vacío → devolver un spacer
    if df is None or df.empty:
        from reportlab.platypus import Spacer
        return Spacer(1, 1)

    cols = list(df.columns)

    # Construir matriz de datos
    data = [cols]
    for _, row in df.iterrows():
        formatted_row = [_format_cell_value(row[c]) for c in cols]
        data.append(formatted_row)

    # Crear tabla
    table = Table(data, repeatRows=1)

    # Estilo básico
    tbl_style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("TOPPADDING", (0, 0), (-1, -1), 2),
    ])

    table.setStyle(tbl_style)
    return table




def crear_pdf_reporte(
    df_seleccion,
    secciones,
    time, 
    nombre_pdf=f"Reporte_ACK.pdf",
    texto_inicial= (
            "Este reporte presenta el análisis correspondiente a los diferentes indicadores GAP "
            "cada sección permite identificar los procesos pendientes que impiden la facturación."
            
        )
):
    """Crea un PDF con las siguientes características
    """

    # Valores por defecto

    




    # Documento
    doc = SimpleDocTemplate(
        nombre_pdf,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=60,
        bottomMargin=40,
    )

    story = []
    styles = getSampleStyleSheet()

    # Estilos
    style_title = ParagraphStyle("title", parent=styles["Title"], alignment=TA_CENTER, fontSize=20)
    style_sub = ParagraphStyle("subtitle", parent=styles["Heading2"], fontSize=14, alignment=TA_LEFT)
    style_text = ParagraphStyle("text", parent=styles["Normal"], alignment=TA_JUSTIFY, fontSize=10, leading=14)
    style_dif = ParagraphStyle("subtitle", parent=styles["Heading2"], fontSize=10, alignment=TA_LEFT)

    # Título
    story.append(Paragraph("Reporte de Análisis GAP", style_title))
    story.append(Paragraph(f"Fecha de actualización: {time}", style_dif))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1))
    story.append(Spacer(1, 12))

    # Texto inicial
    story.append(Paragraph(texto_inicial, style_text))
    story.append(Spacer(1, 16))

    # Generar secciones
    for titulo, resultado in secciones:
        # Subtítulo
        story.append(Paragraph(titulo, style_sub))
        story.append(Spacer(1, 4))



        # Texto por sección (editable)
        texto_cat = (f"Resultados obtenidos para la categoría <b>{titulo}</b>. "
                    "Esta sección contiene los registros clasificados según los criterios establecidos.")
                    
        texto_cat_r  =  (f"Responsable - {persona_responsable(titulo= titulo)}")
        
        story.append(Paragraph(texto_cat, style_text))
        story.append(Paragraph(texto_cat_r, style_dif))
        story.append(Spacer(1, 8))

        # Manejar si la sección trae múltiples dataframes (tuple) o uno solo
        if isinstance(resultado, tuple) or isinstance(resultado, list):
            for df in resultado:
                if df is not None and len(df) > 0:
                    # asegurarse siteName único por fila (por si no se hizo antes)
                    if 'siteName' in df.columns:
                        df = df.drop_duplicates(subset=['siteName'])

                    table = _df_to_table_story(df, styles)
                    story.append(table)
                    story.append(Spacer(1, 14))
        else:
            df = resultado
            if df is not None and len(df) > 0:
                if 'siteName' in df.columns:
                    df = df.drop_duplicates(subset=['siteName'])

                table = _df_to_table_story(df, styles)
                story.append(table)
                story.append(Spacer(1, 14))

    # Construir PDF
    final_doc = doc.build(story)
    print(f"PDF generado: {nombre_pdf}")

def persona_responsable(titulo):
    match titulo: 
        case "GAP DOC": 
            return "Liliana Acosta"
        case "GAP INV":
            return "Aldemar Valenzuela"
        case "GAP HW":
            return "Aldemar Valenzuela(Picking) - Liliana Acosta"
        case "GAP SiteOwner":
            return "Tommy Cantillo"
        case "GAP ONAIR":
            return "Tommy Cantillo"
        case _: 
            return "No hay sección asignada aun"
    
    


