from Generate_report import crear_pdf_reporte,_format_cell_value
from data_gaps import (
    cargar_archivo, gap_doc, gap_log, gap_hw, gap_owner, gap_air
)
from datetime import datetime 

from email_service import EmailService





if __name__ == "__main__":

    time = datetime.now().strftime("%Y-%m-%d")


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
        ("GAP INV", log_df),
        ("GAP HW", hw_df),
        ("GAP SiteOwner", owner_df),
        ("GAP ONAIR", air_df),
    ]
     
    
    log_0010, log_0100 = log_df
    hwc_0150, hwc_0200, hwc_0250 = hw_df 
    ow_0600, ow_0710  = owner_df

    charge ={"Tommy Cantillo": [ow_0600, ow_0710, air_df], "Aldemar Valenzuela":[log_0100,log_0010, hwc_0150], 
             "Laura Acosta": [doc_df, hwc_0200, hwc_0250]}
    correo = {"Tommy Cantillo": "lenisdacosta@gmail.com", "Aldemar Valenzuela": "lenissario18@gmail.com",
              "Laura Acosta": "lenisemmanueldavid@gmail.com"}
    for nombre, tareas in charge.items():
        email = correo.get(nombre)

        send_email = EmailService(email, body= tareas)

        send_email.individual_mail()
    
                

        
        


    




    # Generar PDF
    crear_pdf_reporte(df, secciones, time, nombre_pdf=f"Reporte_Final {time}.pdf")
