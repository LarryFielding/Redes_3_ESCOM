import subprocess
import sys
from datetime import datetime

# para enviar el correo
 
import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

subject = "Hubo errores en dispositivos"
body = "Se adjunta el archivo con el reporte de errores"
sender_email = "equipo.redes3.escom@gmail.com"
receiver_email = "larryjaguey@gmail.com"
password = "abcdef1357"

# Create a multipart message and set headers
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject
#message["Bcc"] = receiver_email  # Recommended for mass emails



time_log ="PingPoller"+datetime.now().strftime("%m_%d_%Y_%H_%M_%S")+ ".txt"
log_file=open(time_log,'w')
no_error = True;

with open('ipTest.txt','r') as ips:
    for ip in ips:
        ip=ip.strip()
        res = subprocess.call(['ping','-c','6',ip])
        date_ping=datetime.now()
        print(res)
        if res == 0:
            print("La direccion "+ip+" respondio correctamente en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S \n"))
            
        else:
            no_error = False
            log_file.write("La direccion "+ip+" no respondió en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n"))
            log_file.write("Después de 6 intentos:\n")
            res = subprocess.call(['ping','-c','4',ip])
            if res == 0:
                log_file.write("\tRespondió correctamente.\n")
            else:
                log_file.write("\tLa direccion "+ip+" no respondió en: "+date_ping.strftime("%m/%d/%Y, %H:%M:%S\n"))
                log_file.write("\tDespués de 4 intentos:\n")
                res = subprocess.call(['ping','-c','2',ip])
                if res == 0:
                    log_file.write("\t\tRespondió correctamente\n")
                else:
                    log_file.write("\t\tFalló finalmente después de 10 intentos.\n")
log_file.close()

if not no_error:
    #enviar correo
    message.attach(MIMEText(body, "plain"))
    filename = time_log  # In same directory as script

    # Open file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        "attachment; filename=" +filename,
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
else:
    #nada
    2+3
