import tkinter as tk 

from Generate_report import crear_pdf_reporte,_format_cell_value
from data_gaps import (
    cargar_archivo, gap_doc, gap_log, gap_hw, gap_owner, gap_air
)
from datetime import datetime 
from email_service import EmailService
from tkinter import filedialog 
import os 
from tkinter import messagebox 
from tkinter import ttk 
from tkinter import font

def cargar_ruta(): 
    ventana_ruta =  tk.Toplevel()
    ventana_ruta.withdraw()
    ventana_ruta.attributes("-topmost", True)

    ruta_archivo  = filedialog.askopenfilename(
                    parent = ventana_ruta,
                    title= "Selecciones el archivo", 
                    filetypes=[("Archivos de Excel", "*.xlsx"), ("Archivos de Excel", "*.xls")]
                    )
    ventana_ruta.destroy()

    if ruta_archivo: 
        print(f"Archivo seleccionado: {os.path.basename(ruta_archivo)}")
        return ruta_archivo
    else: 
        print("Error no hay archivo seleccionado")
        return None 




def  ejecutar_proceso(root):  
    root.withdraw()

    time = datetime.now().strftime("%Y-%m-%d")

    ruta_acceso = cargar_ruta()


    df = cargar_archivo(ruta_excel= ruta_acceso)

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
    correo = {"Tommy Cantillo": "Y", "Aldemar Valenzuela": "Z",  # Cambia las letras X,Y,Z por el email correcto
              "Laura Acosta": "X"}
    for nombre, tareas in charge.items():
        email = correo.get(nombre)

        send_email = EmailService(email, body= tareas)

        send_email.individual_mail()


    nombre = f"Reporte_Final {time}.pdf"
    
    crear_pdf_reporte(df, secciones, time, nombre_pdf=nombre )
    ruta_archivo = f"C:/Users/lenis/OneDrive/Documentos/Proyecto_salvacion/{nombre}"
    send_report = EmailService(receiver_email= "X", attachment= ruta_archivo)
    send_report.send_report()


    final_message = tk.Toplevel








if __name__ == "__main__":


    root = tk.Tk()
    root.title("Acciones pendientes")
    root.geometry("600x200")

    fuente_droid = font.Font(family="Droid Serif", size=18, weight="bold")
    label = tk.Label(root, text = "Haz click para iniciar con el procedimiento", font = fuente_droid)
    label.pack(pady=10)

    boton = tk.Button(root, text = "Presione aqui", command= lambda:ejecutar_proceso(root= root), font = ("Arial", 15), bg="orange", fg = "black")
    boton.pack(pady=10)


    root.mainloop()

