from typing import List, Optional
import pandas as pd
import smtplib  # Protocolo SMTP para enviar correos
from email.mime.multipart import MIMEMultipart  # Estructura de email con múltiples partes
from email.mime.text import MIMEText  # Cuerpo de texto del email
from email.mime.base import MIMEBase  # Permite adjuntar archivos al correo
from email import encoders  # Codifica archivos adjuntos para el envío
import os


class EmailService: 
    def __init__(self, receiver_email, subject = "Tabla de procesos pendientes" , body: Optional[List] = None, attachment = None, SENDER_EMAIL = "email@gmail.com", SENDER_PASSWORD = "contraseña de google(generada especificamente)"):
        """Inicializa la clase con los datos del correo electrónico."""
        self.SENDER_EMAIL= SENDER_EMAIL  # Correo del remitente
        self.SENDER_PASSWORD = SENDER_PASSWORD  # Contraseña del remitente (contraseña de aplicación)
        self.receiver_email = receiver_email  # Correo del destinatario
        self.subject = subject  # Asunto del correo
        self.body = body  # Contenido del mensaje
        self.attachment = attachment # archivo 
    

    

    def individual_mail(self): 
        info_envio = self.body  
        tablas_html = ""

        for df in info_envio:

            # --- LIMPIAR SALTOS DE LÍNEA ---
            df_limpio = df.copy().astype(str)
            df_limpio = df_limpio.applymap(lambda x: x.replace("\n", "").strip())

            # Convertir tabla limpia a HTML
            h = df_limpio.to_html(index=False, border=1)
            tablas_html += h + "<br><br>"

            # Cuerpo HTML bonito
        body_envio = f"""
            <html>
        <body style="font-family: Arial; font-size: 14px;">

            <h2 style="color:#2F5597;">Reporte de procesos pendientes</h2>

            <p>
                Estimado equipo,<br><br>
                Se presenta el reporte actualizado de los procesos pendientes:
            </p>

            {tablas_html}

            <p>
                En la reunión se revisarán las razones que impiden la ejecución del proceso
                y se discutirá un plan de trabajo.
            </p>

            <p>Saludos,<br>Automatización</p>

        </body>
        </html>
        """

        mensaje = MIMEMultipart()
        mensaje["From"] = self.SENDER_EMAIL
        mensaje["To"] = self.receiver_email
        mensaje["Subject"] = self.subject
        mensaje.attach(MIMEText(body_envio, "html"))

        try:
            servidor = smtplib.SMTP("smtp.gmail.com", 587)
            servidor.starttls()
            servidor.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)
            servidor.send_message(mensaje)
            servidor.quit()
            print("Correo enviado ✔️")
        except Exception as e:
            print("Error:", e)



    def send_report(self):

        """Envía un correo con el archivo adjunto."""
        msg = MIMEMultipart()  # Crea la estructura del mensaje
        msg["From"] = self.SENDER_EMAIL  # Define el remitente
        msg["To"] = self.receiver_email  # Define el destinatario
        msg["Subject"] = "Reporte de pendientes"  # Establece el asunto del mensaje


        # Adjuntar el archivo PDF al correo
        with open(self.attachment, "rb") as file:  # Abre el archivo en modo binario
            part = MIMEBase("application", "octet-stream")  # Define el tipo de archivo adjunto
            part.set_payload(file.read())  # Carga el archivo en el correo
            encoders.encode_base64(part)  # Codifica el archivo para envío seguro
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(self.attachment)}")  # Define el nombre del archivo
            msg.attach(part)  # Adjunta el archivo al email

        # Configurar el servidor SMTP de Gmail
        server = smtplib.SMTP("smtp.gmail.com", 587)  # Configura el servidor SMTP con el puerto adecuado
        server.starttls()  # Activa el modo seguro (TLS) para el envío del correo
        server.login(self.SENDER_EMAIL, self.SENDER_PASSWORD)  # Inicia sesión con las credenciales del remitente
        server.sendmail(self.SENDER_EMAIL, self.receiver_email, msg.as_string())  # Envía el correo con el adjunto
        server.quit()  # Cierra la conexión con el servidor SMTP

        print(f"\nEmail enviado a {self.receiver_email} con el análisis adjunto.")  # Mensaje de confirmación
        

    
 