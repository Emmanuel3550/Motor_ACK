from Generate_report import crear_pdf_reporte
import pandas as pd
from data_gaps import (
    cargar_archivo, gap_doc, gap_log, gap_hw, gap_owner, gap_air
)

if __name__ == "__main__":

    df = cargar_archivo()

    # Generar dataframes
    doc_df = gap_doc(df)
    log_df = gap_log(df)
    hw_df = gap_hw(df)
    owner_df = gap_owner(df)
    air_df = gap_air(df)

    # Crear estructura de secciones para el PDF
    secciones = [
        ("GAP DOC", doc_df),
        ("GAP LOG", log_df),
        ("GAP HW", hw_df),
        ("GAP OWNER", owner_df),
        ("GAP ONAIR", air_df),
    ]

    # Generar PDF
    crear_pdf_reporte(df, secciones, nombre_pdf="Reporte_Final2.pdf")
