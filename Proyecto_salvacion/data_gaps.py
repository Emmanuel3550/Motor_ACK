
import pandas as pd

def cargar_archivo(ruta_excel = "C:/Users/lenis/Downloads/1_diciembre.xlsx"):
    df = pd.read_excel(ruta_excel, sheet_name="ACK_Report_Sabana")
    df = df.loc[:, [
        "main_smp","siteName","mos", "integracion", "Dias_Integracion",
        "GAP_LOG_INV","GAP_DOC","GAP_HW_Cierre","GAP_SiteOwner","GAP_OnAir"
    ]]
    df = df.rename(columns= {"Dias_Integracion" : "Dias desde la integracion"})

    return df


def gap_doc(df):
    df = df.loc[:, ["siteName", "mos", "integracion", "Dias desde la integracion", "GAP_DOC"]]
    df = df[df["GAP_DOC"] == "0000.Sin Radicar"]

    # ELIMINA REPECIÓN DE SITIOS
    df = df.drop_duplicates(subset=["siteName"])

    return df



def gap_log(df):
    df = df.loc[:, ["siteName", "mos", "integracion", "Dias desde la integracion", "GAP_LOG_INV"]]

    log_0010 = df[df["GAP_LOG_INV"] == "0010.Sin_Iniciar"].drop_duplicates(subset=["siteName"])
    log_0100 = df[df["GAP_LOG_INV"] == "0100.En_Revision_SS_E2E_Rechazado"].drop_duplicates(subset=["siteName"])

    return log_0010, log_0100

def gap_hw(df):
    df = df.loc[:, ["siteName", "mos", "integracion", "Dias desde la integracion", "GAP_HW_Cierre"]]

    hw_0150 = df[df["GAP_HW_Cierre"] == "0150.Proceso_Picking"].drop_duplicates(subset=["siteName"])
    hw_0200 = df[df["GAP_HW_Cierre"] == "0200.Creacion_Sesion_SS_E2E"].drop_duplicates(subset=["siteName"])
    hw_0250 = df[df["GAP_HW_Cierre"] == "0250.Evaluacion_SS_E2E"].drop_duplicates(subset=["siteName"])

    return hw_0150, hw_0200, hw_0250


def gap_owner(df):
    df = df.loc[:, ["siteName", "mos", "integracion", "Dias desde la integracion", "GAP_SiteOwner"]]

    owner_0600 = df[df["GAP_SiteOwner"] == "0600.Pendiente_Entrega_Infraestructura"].drop_duplicates(subset=["siteName"])
    owner_0710 = df[df["GAP_SiteOwner"] == "0710.Rechazo_1"].drop_duplicates(subset=["siteName"])

    return owner_0600, owner_0710

def gap_air(df):
    df = df.loc[:, ["siteName", "mos", "integracion", "Dias desde la integracion", "GAP_OnAir"]]
    air = df[df["GAP_OnAir"] == "12. Pendiente carga RR"]

    # Remover repetidos
    air = air.drop_duplicates(subset=["siteName"])

    return air
