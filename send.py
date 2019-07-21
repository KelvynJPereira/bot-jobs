# import necessary packages
import os.path as op
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

# Metodo para envio de e-mails
def send_resume(send_list_emails):

    # Instancia do objeto mensagem
    msg = MIMEMultipart()

    # Corpo da mensagem
    message = '''
    \rPrezado(a),\n
    \nSegue em anexo meu curriculum para análise, uma vez que busco uma nova colocação no mercado de trabalho.
    \nAcredito que minha experiência possa vir a ser útil para contribuir na conquista de metas e expectativas da instituição.
    \nDesde já, agradeço a atenção e aguardo um pronunciamento.
    \n\nAt.te,
    \nKelvyn Pereira.

    '''
    # Configuracao dos parametros da mensagem
    msg['From'] = "kelvynjs97@hotmail.com"
    password = "33048385kjsP"
    to_emails = send_list_emails  
    msg['Subject'] = "Curriculum"

    # Anexacao de arquivo
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open("bot-jobs\\my-resume\\curriculum.doc", "rb").read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="curriculum.doc"')
    msg.attach(part)

    # Adiciona as mensagens ao corpo do e-email
    msg.attach(MIMEText(message, 'plain'))
    
    # Inicia o server
    server = smtplib.SMTP('smtp.live.com: 587')
    server.starttls()
    
    # Realiza login no servidor com as credenciais informadas
    server.login(msg['From'], password)
    
    # Tratamento de errros
    try:
        # Envia e-mail utilizando o server
        for to in to_emails:
            server.sendmail(msg['From'], to , msg.as_string())
            print('Send to: '+to+'\n')
        # Desativa o servidor 
        server.quit()
        # Exibe resultados
        return 'Successfully send emails!\n'

    except:
       return 'Error sending emails!\n'
    

   

   


