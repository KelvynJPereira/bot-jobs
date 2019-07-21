'''
-------------------------------------------------
   ____        __            __      __        
   / __ )____  / /_          / /___  / /_  _____
  / __  / __ \/ __/_______  / / __ \/ __ \/ ___/
 / /_/ / /_/ / /_/_____/ /_/ / /_/ / /_/ (__  ) 
/_____/\____/\__/      \____/\____/_.___/____/  

-------------------------------------------------
                                                 
Author: Kelvyn J. Pereira
Year: 2019-07-21
Version: 1.0
Github: https://github.com/KelvynJPereira/bot-jobs

'''

# Modulos necessarios
import os.path
import time
import sys
import requests
from bs4 import BeautifulSoup
from validate_email import validate_email
from datetime import date, timedelta
from send import send_resume

# Obetem data atual
def date_function():
    
    hoje = date.today()
    today = str(hoje)
    
    return hoje

# Realiza requisicao
def scraping_emails():

    page = requests.get('https://informevagaspe.blogspot.com/') # Request

    # Extracao de emails da pagina
    soup = BeautifulSoup(page.text,'html.parser')
    emails = soup.find_all('span', attrs={'style':'color: blue;'})

    # Filtragem de emails das tags
    verify_emails = []
    for email_filter in emails:
        email_filtred = email_filter.text # Extrai texto das tags
        email_filtred = email_filtred.replace(' ','') # Extrai espacos das extremidades

        # Validacao de e-mail
        if validate_email(email_filtred):
            verify_emails.append(email_filtred) # Adiciona itens filtrados ao array
        
    # Filtro de e-mails nao repetidos
    validated_emails = []
    for i in verify_emails:
        if i not in validated_emails:
            validated_emails.append(i)

    return  validated_emails

# Salva e-mails em arquivo
def save_emails(title, array_emails):
    data = open('bot-jobs\\email-scraping\\'+str(title)+'.txt', 'w')
    for write_email in array_emails:
        data.write(write_email+'\n')
    data.close
    return '\n'+str(today)+' e-mails saved successfully!\n' # Mudar pra title

# Seleciona e-mails ja enviados
def compare_emails(title, array_emails):

    # Leitura de arquivo do dia anterior
    data = open('bot-jobs\\email-scraping\\'+str(title)+'.txt', 'r')
    texto = data.readlines()

    temp_array = [] 
    # Armazenamento temporario de texto em array
    for temp in texto:
        temp = str(temp.strip()) # Retira possiveis espacos das strings
        temp_array.append(temp)

    actual_emails = array_emails # Array de novos e-mails capturados
    yesterday_emails = temp_array # Array de e-mails do dia anterior
    news_emails = list(set(actual_emails) - set(yesterday_emails)) # Array de novos emails capturados
    
    print(save_emails(today, news_emails)) # Salva arquivo de e-mails

    return news_emails # Retorna array de novos emails
           
# Looping do programa
print('\n')
while True:
   
    # Verifica a data atual
    date = date_function()
    today = date

    animation = "|/-\\"
    count = 0

    # Looping de verificacao do dia
    while today == date:
        today = date_function()

        # Progress bar
        count += 1
        time.sleep(0.1)
        sys.stdout.write("\rSearching jobs " + animation[count % len(animation)])
        sys.stdout.flush()

        # Realiza procedimentos 
        if today != date:
            
            # Consulta data do dia anterior
            yesterday = str(date.today() - timedelta(days=1))

            # Verifica se arquivo do dia anterior existe
            if  not os.path.exists('bot-jobs\\email-scraping\\'+str(yesterday)+'.txt'):

                # Realiza scraping no site
                list_emails = scraping_emails()

                salved_emails = save_emails(today, list_emails)  # Salva e-mails em arquivo
                print('\n'+salved_emails+'\n')
      
                # Envia curriculo para lista de e-mails
                send_response = send_resume(list_emails)

                #os.system('cls' if os.name == 'nt' else 'clear') # Limpa tela
                print(send_response+'\n') # Exibe resposta 

            else:
                list_emails = scraping_emails() # Realiza scraping no site
                news_emails_result = compare_emails(yesterday, list_emails) # Compara resultado com resultados anteriores
               
                # Envia curriculo para lista de e-mails
                send_response = send_resume(news_emails_result) 
                print(send_response+'\n') # Exibe resposta 
              