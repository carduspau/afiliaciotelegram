import telegram
import mysql.connector
import asyncio
from io import BytesIO
from PIL import Image
import requests
import telegram
import asyncio
import time
from datetime import datetime
import pytz


mydb = mysql.connector.connect(
  host="mysql-preuscat.alwaysdata.net",
  user="preuscat",
  password="PREUSCAT-AFILIACIO",
  database="preuscat_afiliacio"
)

if mydb.is_connected():
  print("Connexió a la base de dades establerta amb èxit")
mycursor = mydb.cursor()

sql = "SELECT * FROM enviats"
mycursor.execute(sql)
resultats = mycursor.fetchall()


barcelona_tz = pytz.timezone('Europe/Paris')
now = datetime.now(barcelona_tz)
datahora = now.strftime('%y%m%d_%H%M')


id = 0
for resultat in resultats:
    if resultat[1] == 0:
        id = resultat[0]
        estat = resultat[1]
        asin = resultat[2]
        titol = resultat[3]
        preuactual = resultat[4]
        preuanterior = resultat[5]
        img_url = resultat[6]
        descompte = resultat[7]
        
        sql_update = "UPDATE enviats SET estat = %s WHERE id = %s"
        mycursor.execute(sql_update, (datahora, id,))
        mydb.commit()
        
        break
      
preuactual = preuactual.replace(".", ",")
preuanterior = preuanterior.replace(".", ",")
      
if descompte > 80:
    alert = '🔴🔴🔴🔴 OFERTA 4rt GRAU!!'
if descompte <= 80 and descompte >= 50:
    alert = '🟠🟠🟠 OFERTA 3r GRAU!!'
if descompte < 50 and descompte > 0:
    alert = '🟡🟡 OFERTA 2n GRAU!!'
if descompte <= 0:
    alert = '🟢 OFERTA 1r GRAU!!'    
      
      
# Descarrega la imatge del web
response = requests.get(img_url)
image = Image.open(BytesIO(response.content))

# Redimensiona la imatge
image.thumbnail((500, 500))
output = BytesIO()
image.save(output, format='JPEG')
output.seek(0)
      
# Inicialitza el bot de Telegram amb el token
bot = telegram.Bot(token='6207396438:AAGBPSyUXZ6oaUoIhbBhgr8fvuxdrdeDRmE')

async def send_message():
    # Crea el botó
    url = 'https://preuscat.alwaysdata.net/redirect.php?asin='+asin+'&plataforma=telegram'
    button = telegram.InlineKeyboardButton(text='amazon.es', url=url)
    # Afegeix el botó a un InlineKeyboardMarkup
    keyboard = telegram.InlineKeyboardMarkup([[button]])
    # Envia el missatge amb el botó i la imatge
    message = f"{alert} [-{descompte}%]\n\n{titol}\n\nPreu anterior: {preuanterior}€\n ❗OFERTA: {preuactual}€❗"
    await bot.send_photo(chat_id='@preuscattokenprovesbot', photo=output, caption=message, reply_markup=keyboard)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(send_message())
