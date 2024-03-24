import requests
import os
import json
import telebot
import dotenv
import random

dotenv.load_dotenv()

BOT_TOKEN = os.environ.get('BOT_TOKEN')
BIN_CHANNEL_ID = os.environ.get('BIN_CHANNEL_ID')
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    if checkuserinmychannel(user_id):
        bot.send_message(message.chat.id, 'Welcome to TERABOX DOWNLOADER (SEEU)\nSent Tera link for file')
    else:
        bot.send_message(message.chat.id, 'Join channel to use this bot @terao2\nThen click /start again')

def checkuserinmychannel(user_id):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/getChatMember?chat_id=@terao2&user_id={user_id}'
    response = requests.get(url)
    data = response.json()
    if data['result']['status'] in ['member', 'creator', 'administrator']:
        return True
    else:
        return False
    
@bot.message_handler(func=lambda message: True)
def send_file(message):
    user_id = message.from_user.id
    if checkuserinmychannel(user_id):
        bot.send_message(message.chat.id, 'url decoding please wait...')
        user_id = message.from_user.id
        file_link = generate_link(message.text, message.chat.id)
        if file_link is not None:
            chat_id = message.chat.id
            send_media(chat_id, file_link)
            store_in_bin(file_link)
    else:
        bot.send_message(message.chat.id, 'Join my channel to use this bot @terao2')

def send_media(chat_id, file_link):
    bot.send_message(chat_id, '📥')
    file_name = download_file(file_link)
    file_extension = file_name.split('.')[1]
    if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
        bot.send_photo(chat_id, open(file_name, 'rb'))
    elif file_extension in ['mp4', 'avi', 'mkv', '3gp']:
        bot.send_video(chat_id, open(file_name, 'rb'))  
    elif file_extension in ['mp3', 'wav', 'flac', 'm4a']:
        bot.send_audio(chat_id, open(file_name, 'rb'))      
    else:
        bot.send_document(chat_id, open(file_name, 'rb'))
    os.remove(file_name)

def download_file(file_link):
    response = requests.get(file_link)
    file_name = f'{random.randint(1, 10000)}.{response.headers["Content-Type"].split("/")[1] if "Content-Type" in response.headers else "jpg"}'
    with open(file_name, 'wb') as file:
        file.write(response.content)
    return file_name

def check_file_size(file_path, max_size_in_bytes):
  """
  This function checks if a file is smaller than the specified maximum size.

  Args:
      file_path: Path to the file.
      max_size_in_bytes: Maximum allowed file size in bytes.

  Returns:
      True if the file size is within the limit, False otherwise.
  """
  try:
    file_stats = os.stat(file_path)
    file_size = file_stats.st_size
    return file_size <= max_size_in_bytes
  except FileNotFoundError:
    print("File not found!")
    return False

def generate_link(file_link, chat_id):
    url = "https://bot-nine-rho.vercel.app/api?data=" + file_link
    response = requests.get(url, timeout=10000)
    data = response.json()
    try:
        return data['direct_link']
    except:
        bot.send_message(chat_id, 'Error in generating link. Please try again')
        return None

def store_in_bin(file_link):
    file_name = download_file(file_link)
    file_extension = file_name.split('.')[1]
    with open(file_name, 'rb') as file:
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            bot.send_photo(BIN_CHANNEL_ID, file)
        elif file_extension in ['mp4', 'avi', 'mkv', '3gp']:
            bot.send_video(BIN_CHANNEL_ID, file)  
        elif file_extension in ['mp3', 'wav', 'flac', 'm4a']:
            bot.send_audio(BIN_CHANNEL_ID, file)      
        else:
            bot.send_document(BIN_CHANNEL_ID, file)
    os.remove(file_name)

bot.infinity_polling()
