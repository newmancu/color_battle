import json
import time
import telebot
import os
import sys
import requests
import threading
import jwt
from queue import Queue

CONNECTIONS = 50
CHAT_ID = os.environ.get('CHAT_ID', '@color_battle')
th_queue = Queue(CONNECTIONS*2)
auth_token = None
jw = jwt.JWT()
lock = threading.Lock()

def send_requests(q: Queue, bot: telebot.TeleBot):
  global auth_token, jw, lock
  headers = {
    'Content-Type':'application/json',
  }
  while True:
    try:
      data = q.get()
      with lock:
        if auth_token is None or jw.decode(auth_token, do_verify=False)['exp'] < time.time():
          data_h = json.dumps({
              'username':os.environ.get('BOT_USERNAME', 'bot_1'),
              'password':os.environ.get('BOT_PASSWORD', 'bot_1')
            })
          res1 = requests.post(
            'http://web:8000/api/token/',
            headers={'Content-Type':'application/json'},
            data=data_h
          )
          if res1.status_code == 200:
            auth_token = res1.json()['access']

      res = requests.post(
        'http://web:8000/api/tg/new_player',
        headers={
          'Authorization': f'Bearer {auth_token}',
          **headers
        },
        data=json.dumps(data['data'])
      )
      if res.status_code in (200, 201):
        bot.reply_to(
          data['message'], 
          '\n\n'.join([f"{item['w_username']}:{item['w_password']}" for item in res.json()])
        )
      q.task_done()
    except Exception as er:
      sys.stderr.write(str(er) + '\n') 


API_TOKEN = os.environ.get(
  'TELEBOT_TOKEN', 
  '5593168916:AAGIwar0clkGguu0ylH4YLXs8bFWQnkYV4E'
)

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start', 'workers'])
def start_game(message: telebot.types.Message):
  try:
    r = bot.get_chat_member(CHAT_ID, message.from_user.id)
    if r.status == 'left':
      return bot.reply_to(
        message,
        f"Нехорошо отписываться от {CHAT_ID}"
        )
  except:
    return bot.reply_to(
      message,
      f"Сперва подпишись на {CHAT_ID}"
      )
  data = {
    'data': {
      'owner': message.from_user.id
    },
    'message': message
  }
  th_queue.put(data)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    bot.reply_to(message, """\
      Use /start or /workers to get your workers' 
      login and passwords
    """)

for i in range(CONNECTIONS):
  threading.Thread(
    target=send_requests,
    args=(th_queue, bot),
    daemon=True
  ).start()

th_queue.join()
sys.stdout.write(str('Bot started\n'))
bot.infinity_polling()