import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

class CorreoElectronico:
    def __init__(self):
        self.servidorSMTP = "smtp.office365.com"
        self.puerto = 587
        self.usuario = "" #email, example: hello123@hotmail.com
        self.contraseña = ""  # hotmail passwd

    def enviarCorreo(self, destinatario, asunto, mensaje, archivoAdjunto=None):
        msg = MIMEMultipart()
        msg['From'] = self.usuario
        msg['To'] = destinatario
        msg['Subject'] = asunto

        msg.attach(MIMEText(mensaje, 'plain'))

        if archivoAdjunto:
            if not os.path.exists(archivoAdjunto):
                print(f"Error: No se encontró el archivo {archivoAdjunto} para adjuntar.")
                return
            with open(archivoAdjunto, 'rb') as f:
                parte = MIMEApplication(f.read(), Name=os.path.basename(archivoAdjunto))
                parte['Content-Disposition'] = f'attachment; filename="{os.path.basename(archivoAdjunto)}"'
                msg.attach(parte)

        try:
            servidor = smtplib.SMTP(self.servidorSMTP, self.puerto)
            servidor.starttls()
            servidor.login(self.usuario, self.contraseña)
            servidor.sendmail(self.usuario, destinatario, msg.as_string())
            servidor.quit()
            print("Correo enviado correctamente")
        except smtplib.SMTPAuthenticationError:
            print("Error: Falló la autenticación, verifica tu usuario y contraseña.")
        except Exception as e:
            print(f"Error al enviar el correo: {str(e)}")
