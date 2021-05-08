import os
import telebot
import requests
from bs4 import BeautifulSoup as bs

my_secret = os.environ['api telegram bot']
bot = telebot.TeleBot(my_secret, parse_mode=None)

kode = {
'0': ' Cerah / Clear Skies',
'1': ' Cerah Berawan / Partly Cloudy',
'2': ' Cerah Berawan / Partly Cloudy ',
'3': ' Berawan / Mostly Cloudy',
'4': ' Berawan Tebal / Overcast ',
'5': ' Udara Kabur / Haze ',
'10': ' Asap / Smoke',
'45': ' Kabut / Fog',
'60': ' Hujan Ringan / Light Rain',
'61': ' Hujan Sedang / Rain',
'63': ' Hujan Lebat / Heavy Rain ',
'80': ' Hujan Lokal / Isolated Shower',
'95': ' Hujan Petir / Severe Thunderstorm',
'97': ' Hujan Petir / Severe Thunderstorm'
}

cuaca = {
  'pagi' : '',
  'siang' : '', 
  'malam' : ''
}

#CUACA KOTAMOBAGU
def cuacakota():
  respon = requests.get("https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-SulawesiUtara.xml")
  rtext = respon.text

  soup = bs(rtext, 'xml')
  kotamobagu = soup.find(id="501615")
  weather = kotamobagu.find(id="weather")
  wh0 = weather.find(h="0")
  nilai0 = wh0.value.string
  cuaca['pagi'] = kode[nilai0]
  wh6 = weather.find(h="6")
  nilai6 = wh6.value.string
  cuaca['siang']=kode[nilai6]
  wh12 = weather.find(h="12")
  nilai12 = wh12.value.string
  cuaca['malam']=kode[nilai12]

  prakiraan = str(
    "Cuaca Hari ini" +
    "\n Pagi =" + cuaca['pagi'] +
    "\n Siang =" + cuaca['siang'] +
    "\n Malam =" + cuaca['malam']
  )

  print(nilai0)
  print(nilai6)
  print(nilai12)

  return prakiraan

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  bot.reply_to(message, "HALO")

@bot.message_handler(commands=['cuaca'])
def send_cuaca(message):
  
  bot.reply_to(message, cuacakota())

bot.polling()