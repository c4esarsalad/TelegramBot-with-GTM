import telebot
from config import token
import os
from logic import get_class

bot = telebot.TeleBot(token)

if not os.path.exists('user_photos'):
    os.makedirs('user_photos')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне фото")

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    
    if not message.photo:
        return bot.send_message(message.chat.id, "Вы забыли загрузить картинку")
    
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1]
    downloaded_file = bot.download_file(file_info.file_path)
    with open(file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    result = get_class(model_path="keras_model.h5", labels_path="labels.txt", image_path=file_name)
    bot.send_message(message, result)

bot.polling()
