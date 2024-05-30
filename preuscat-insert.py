import telegram
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.common.by import By
import re
import random
import time
from io import BytesIO
from PIL import Image
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import mysql.connector
from decimal import Decimal
from datetime import datetime
import pytz




#! 0 - PREPARATIUS
llista = []
llista_negatiu = []

# 0.1 - IDENTIFICACIÓ BASE DE DADES
mydb = mysql.connector.connect(
  host="",
  user="",
  password="",
  database=""
)

# 0.2 - COMPROVACIÓ DE LA CONNEXIÓ
if mydb.is_connected():
  print("Connexió a la base de dades establerta amb èxit")
mycursor = mydb.cursor()

# 0.3 - BUCLE DE PREVENCIÓ D'ERRORS
codierror = 0
while True:
    
    # 0.3.1 - SELECCIÓ D'ENLLAÇOS
    if codierror == 0:
        goldbox = "https://www.amazon.es/gp/goldbox/?pd_rd_w=mKDEB&content-id=amzn1.sym.6ef68c6a-454c-428b-b90f-02f0f860985c&pf_rd_p=6ef68c6a-454c-428b-b90f-02f0f860985c&pf_rd_r=WG2QZBRCGZ408W50F97E&pd_rd_wg=y9Raj&pd_rd_r=76ecf81a-ef58-40c9-aa3f-be98f5027021&ref=b2b_sow_sm_td_bnp_es_bnp&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-deals-under-20%2522%252C%2522priceRange%2522%253A%257B%2522from%2522%253A0%252C%2522to%2522%253A20%257D%252C%2522dealType%2522%253A%2522LIGHTNING_DEAL%2522%252C%2522sorting%2522%253A%2522FEATURED%2522%257D"
    elif codierror == 100:
        goldbox = "https://www.amazon.es/gp/goldbox/?pd_rd_w=yb7wR&content-id=amzn1.sym.6ef68c6a-454c-428b-b90f-02f0f860985c&pf_rd_p=6ef68c6a-454c-428b-b90f-02f0f860985c&pf_rd_r=SQSM3SEZTS49CKP0ZKDT&pd_rd_wg=KCbmI&pd_rd_r=a558a248-fcf4-49ce-a737-bc67c998437b&ref=b2b_sow_sm_td_bnp_es_bnp&deals-widget=%257B%2522version%2522%253A1%252C%2522viewIndex%2522%253A0%252C%2522presetId%2522%253A%2522deals-collection-all-deals%2522%252C%2522sorting%2522%253A%2522FEATURED%2522%257D"
    
    # 0.3.2 - ASIN NEGATIU
    if codierror == 201:
        llista_negatiu.append(asin)
        
    if codierror == 202:
        llista_negatiu.append(asin)
        
    if codierror == 203:
        llista_negatiu.append(asin)
        
    if codierror == 204:
        llista_negatiu.append(asin)
        
    if codierror == 301:
        llista_negatiu.append(asin)
    
    
#!1 - FER UNA LLISTA DELS ASINS QUE HI HA A GOLDBOX
    # 1.1 - OBRIR EL NAVEGADOR
    driver = webdriver.Chrome()

    # 1.2 - ANAR A LA PÀGINA GOLDBOX
    driver.get(goldbox)
    time.sleep(3)

    # 1.3 - EXTREURE ELS ELEMENTS QUE CONTINGUIN /dp/
    try:
        enlaces = driver.find_elements(By.XPATH, "//a[contains(@href, '/dp/')]")
    except:
        if codierror == 100:
            break
        else:
            codierror = 100
            continue

    # 1.4 - D'AQUESTS ELEMENTS, NOMÉS N'EXTREIEM L'ENLLAÇ
    for enlace in enlaces:
        enllac = enlace.get_attribute("href")
        asin = re.search(r"(?<=dp\/)[A-Z0-9]+", enllac).group(0)
        
        # 1.4.1 - POSEM ELS ENLLAÇOS EN UNA LLISTA
        if asin not in llista:
            if asin not in llista_negatiu:
                
                # 1.4.1.1 - L'ASIN NO HA DE SER A LA BBDD
                sql = "SELECT * FROM manual"
                mycursor.execute(sql)
                resultats = mycursor.fetchall()
                for resultat in resultats:
                    if asin == resultat[2]:
                        print(asin,': Ja és a la BBDD')
                    else:
                        llista.append(asin)

    #! 2 - EXTREURE LES DADES (TÍTOL, URL D'IMG, PREU ANTERIOR I PREU ACTUAL) D'UN ASIN

    # 2.1 - AGAFEM UN ASIN ALEATORI DE LA LLISTA
    try:
        asin = random.choice(llista)
        print ('-----------------------------')
        print (asin)
        print ('-----------------------------')
    except:
        codierror = 101
        continue

    # 2.2 - GENEREM L'ENLLAÇ D'AMAZON
    url = "https://www.amazon.es/dp/" + asin

    # 2.3 - DIRIGIM EL NAVEGADOR A L'ENLLAÇ I EXTREIEM L'HTML
    driver.get(url)
    time.sleep(3)
    html_content = driver.page_source

    # 2.4 - EXTREIEM L'ENLLAÇ DE LA IMATGE
    try:
        img_url = re.findall(r'"large":"(https.*?)"', html_content)[0]
    except:
        codierror = 201
        print(asin,': no-imatge')
        continue

    # 2.5 - EXTREIEM EL TÍTOL DEL PRODUCTE
    try:
        name = driver.find_element(By.CLASS_NAME, "product-title-word-break").text.strip()
    except:
        codierror = 202
        print(asin,': no-titol')
        continue

    # 2.6 - EXTREIEM EL PREU ACTUAL 
    try:
        preuactual = driver.find_element(By.CLASS_NAME, "priceToPay").text.strip()
    except:
        try:
            preuactual = driver.find_element(By.CLASS_NAME, "apexPriceToPay").text.strip()
        except:
            codierror = 203
            print(asin,': no-preuactual')
            continue

    # 2.6.1 - NETEJEM ELS RESULTATS DEL PREU ACTUAL
    preuactual = preuactual.replace("\n", ",")
    preuactual = preuactual.replace("€", "")
    preuactual = preuactual.replace(",", ".")
    float (preuactual)

    # 2.7 - EXTREIEM EL PREU ANTERIOR 
    try:
        preuanterior = driver.find_element(By.CSS_SELECTOR, "span.a-price[data-a-color='secondary'][data-a-size='s']").text.strip()
    except:
        try:
            preuanterior = driver.find_element(By.CSS_SELECTOR, "span.a-price.a-text-price.a-size-base[data-a-color='secondary'][data-a-strike='true']").text.strip()
        except:
            codierror = 204
            print (asin,': no-preuanterior')
            continue
    
    # 2.7.1 - NETEJEM ELS RESULTATS DEL PREU ANTERIOR
    preuanterior = preuanterior.replace("€", "")
    preuanterior = preuanterior.replace(",", ".")
    float (preuanterior)
    
    #? PREVENCIÓ D'ERRORS
    if preuanterior < preuactual:
        print (asin,': no descompte')
        codierror = 301
        continue

    #! 3 - ADAPTEM I PREPAREM LES VARIABLES PER A ENVIAR-LES A TELEGRAM

    # 3.1 - CREEM EL DESCOMPTE, COM A PERCENTATGE SENSE EL %, I EL CONVERTIM EN INT
    descompte = (float(preuactual)*100)/float(preuanterior)
    descompte = 100 - descompte
    descompte = int(round(descompte))

    # 3.2 - CREEM EL GRAU
    if descompte > 80:
        alert = '🔴🔴🔴🔴 OFERTA 4rt GRAU!!'
    if descompte <= 80 and descompte >= 50:
        alert = '🟠🟠🟠 OFERTA 3r GRAU!!'
    if descompte < 50 and descompte > 0:
        alert = '🟡🟡 OFERTA 2n GRAU!!'
    if descompte <= 0:
        alert = '🟢 OFERTA 1r GRAU!!'

    # 3.3 - BAIXEM LA IMATGE
    response = requests.get(img_url)
    image = Image.open(BytesIO(response.content))

    # 3.4 - REDIMENSIONEM LA IMATGE
    image.thumbnail((500, 500))
    output = BytesIO()
    image.save(output, format='JPEG')
    output.seek(0)

    # 3.5 - TRADUÏM EL TEXT A CATALÀ. OBRIM GOOGLE TRANSLATOR AMB EL TÍTOL AMB CASTELLÀ
    translate_url = f"https://translate.google.com/?hl=es&sl=es&tl=ca&text={name}&op=translate"
    driver.get(translate_url)
    time.sleep(3)

    # 3.5.1 - ACCEPTEM LES COOKIES
    wait = WebDriverWait(driver, 10)
    accept_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Aceptar todo')]")))
    accept_button.click()

    # 3.5.2 - ESPEREM A QUÈ APAREGUIN ELS ELEMENTS I ELS COPIEM
    translation = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='ryNqvb']")))
    name = translation.text

    # 3.6 - TANQUEM EL NAVEGADOR
    driver.quit()

    #! 4 - PREPAREM L'ENVIAMENT A LA BASE DE DADES

    # 4.1 - SELECCIONEM TOTS ELS RESULTATS DE LA BASE DE DADES
    sql = "SELECT * FROM enviats"
    mycursor.execute(sql)
    resultats = mycursor.fetchall()

    # 4.2 - AGAFEM L'ÚLTIM ID
    id = 0
    for resultat in resultats:
        id = id + 1
        
    # 4.3 - DATA I HORA
    barcelona_tz = pytz.timezone('Europe/Paris')
    now = datetime.now(barcelona_tz)
    datahora = now.strftime('%y%m%d_%H%M')

    # 4.3 - ADAPTEM ELS PREUS
    preuactual = Decimal(preuactual)
    preuanterior = Decimal(preuanterior)

    # 4.4 - INSERTEM LES DADES A LA BASE DE DADES
    mycursor = mydb.cursor()
    sql = "INSERT INTO enviats (id, estat, asin, titol, preuactual, preuanterior, img, descompte, datahora) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (id, '0', asin, name, preuactual, preuanterior, img_url, descompte, datahora)
    mycursor.execute(sql, val)
    mydb.commit()
    subprocess.call(["python", r"C:\Users\PC\Documents\preuscat\preuscat\preuscat-telegram.py"])
    break
