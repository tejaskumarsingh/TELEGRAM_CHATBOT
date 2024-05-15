import telebot
import openai
import os
from docx2pdf import convert
import requests
import random
import datetime
import time
import pyttsx3
import tempfile
import json
import urllib.request
from gtts import gTTS
import urllib.parse
news_api="ENTER YOU API KEY"
IMAGE_PATH=['D:\\mysite\\download (1).jpeg','D:\\mysite\\download (2).jpeg','D:\\mysite\\download (3).jpeg']
img=random.choice(IMAGE_PATH)
reminders={}
engine = pyttsx3.init()
openai.api_key = "ENTER YOUR API KEY"
def get_chatgpt_response(message):
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=message,
        max_tokens=4000,
        temperature=0.6,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
    )
    return response.choices[0].text
def voice_message(message):
    response = get_chatgpt_response(message.text)
    text=response
    if text:
        tts = gTTS(text=text,lang='en')
        temp_dir='E:\\Tejas Python Project'
        os.makedirs(temp_dir,exist_ok=True)
        output_file = os.path.join(temp_dir,'output.mp3')
        tts.save(output_file)
        with open(output_file, 'rb') as audio_file:
            bot.send_audio(message.chat.id, audio_file)
        os.remove(output_file)
    else:
        bot.reply_to(message,"no data found")
def moviea(message):
    movies = [
        "Vikram",
        "Drishyam",
        "Bhola",
        "The Kerela Story",
        "KGF",
        "KGF 2",
        "Sheershah",
        "Kashmir Files"
    ]
    name=random.choice(movies)
    bot.reply_to(message,name)
def echo_message(message):
    response = get_chatgpt_response(message.text)
    bot.reply_to(message, response)
def handle_mood(message):
    mood = message.text.strip().lower()
    prompt = f"I'm feeling {mood}. Can you suggest a bollywood song for me?"
    response = get_chatgpt_response(prompt)
    bot.reply_to(message, response)
def movie_recommend(message):
    name=message.text.strip().lower()
    prompt = f"Suggest me any movie about {name}. Only movies available in hindi."
    response = get_chatgpt_response(prompt)
    bot.reply_to(message, response)
if __name__ == "__main__":
    bot = telebot.TeleBot('5959929363:AAFL7RQcvdsym5mA9PmdXZtKxpfu1n0XB3g')
    @bot.message_handler(commands=['start'])
    def start(message):
        with open(img,'rb') as photo:
            bot.send_photo(message.chat.id,photo)
        text = """
𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐭𝐡𝐢𝐬 𝐁𝐨𝐭✨
𝐓𝐡𝐢𝐬 𝐜𝐡𝐚𝐭𝐛𝐨𝐭 𝐢𝐬 𝐩𝐫𝐨𝐣𝐞𝐜𝐭 𝐦𝐨𝐝𝐞𝐥 𝐛𝐨𝐭. 
𝐋𝐢𝐬𝐭 𝐨𝐟 𝐜𝐨𝐦𝐦𝐚𝐧𝐝𝐬 𝐭𝐨 𝐚𝐜𝐜𝐞𝐬𝐬 𝐭𝐡𝐞 𝐛𝐨𝐭. 
/𝐬𝐭𝐚𝐫𝐭 - To start the Bot. 
/𝐚𝐬𝐤[𝐒𝐏𝐀𝐂𝐄] [𝐐𝐔𝐄𝐒𝐓𝐈𝐎𝐍] - Ask any question. 
/𝐝𝐨𝐜𝐮𝐦𝐞𝐧𝐭 [𝐒𝐏𝐀𝐂𝐄] [𝐒𝐄𝐍𝐃 𝐃𝐎𝐂𝐔𝐌𝐄𝐍𝐓] - Send document and convert it into pdf. 
/𝐦𝐮𝐬𝐢𝐜 [𝐒𝐏𝐀𝐂𝐄] [𝐌𝐎𝐎𝐃] - Type mood and get suggested music according to it. 
/𝐦𝐨𝐯𝐢𝐞 [𝐒𝐏𝐀𝐂𝐄] [𝐆𝐄𝐍𝐑𝐄] - Type genre of movie and get suggested movie according to it. 
/𝐭𝐫𝐞𝐱 [𝐒𝐏𝐀𝐂𝐄] [𝐐𝐔𝐄𝐒𝐓𝐈𝐎𝐍] - Ask question and get reply in voice. 
/𝐰𝐞𝐚𝐭𝐡𝐞𝐫 [𝐒𝐏𝐀𝐂𝐄] [𝐋𝐎𝐂𝐀𝐓𝐈𝐎𝐍] - Get weather report 
/𝐧𝐞𝐰𝐬 [𝐒𝐏𝐀𝐂𝐄] [𝐋𝐎𝐂𝐀𝐓𝐈𝐎𝐍] - Get latest news
/𝐦𝐞𝐝𝐢 [𝐒𝐏𝐀𝐂𝐄] [𝐍𝐀𝐌𝐄] - Get info abput medicine.
"""
        bot.send_message(message.chat.id, text)

    @bot.message_handler(commands=['ask'])
    def run_api(message):
        echo_message(message)
    @bot.message_handler(commands=['exit'])
    def exit_bot(message):
        bot.send_message(message.chat.id, 'Exiting bot...')
        bot.stop_polling()
    @bot.message_handler(content_types=['document'])
    def handle_document(message):
        if message.document.mime_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            word_file_path = 'temp.docx'
            with open(word_file_path, 'wb') as file:
                file.write(downloaded_file)
            pdf_file_path = 'converted.pdf'
            convert(word_file_path, pdf_file_path)
            with open(pdf_file_path, 'rb') as file:
                bot.send_document(message.chat.id, file)
            os.remove(word_file_path)
            os.remove(pdf_file_path)
    @bot.message_handler(commands=['music'])
    def songs(message):
        handle_mood(message)
    @bot.message_handler(commands=['movie'])
    def moviess(message):
        movie_recommend(message)
    @bot.message_handler(commands=['movie1'])
    def movieee(message):
        moviea(message)
    @bot.message_handler(func=lambda message: message.text.startswith('/remind'))
    def handle_set_reminder(message):
        chat_id = message.chat.id
        command_parts = message.text.split(' ', 2)
        if len(command_parts) == 3:
            reminder_message = command_parts[1]
            time_str = command_parts[2]
            try:
                time = datetime.datetime.strptime(time_str, '%H:%M').time()
                current_time = datetime.datetime.now().time()
                if time >= current_time:
                    reminder_datetime = datetime.datetime.combine(datetime.datetime.now().date(), time)
                    reminders[chat_id] = (reminder_message, reminder_datetime)
                    bot.reply_to(message, f"Reminder set for {time_str}: {reminder_message}")
                else:
                    bot.reply_to(message, "Please enter a future time.")
            except ValueError:
                bot.reply_to(message, "Invalid time format. Please use HH:MM.")
        else:
            bot.reply_to(message, "Invalid command format. Please use /remind <message> HH:MM")

    def check_reminders():
        now = datetime.datetime.now()
        for chat_id, (reminder_message, reminder_datetime) in list(reminders.items()):
            if now >= reminder_datetime:
                bot.send_message(chat_id, f"Reminder: {reminder_message}")
                del reminders[chat_id]
    def reminder_checker():
        while True:
            check_reminders()
            time.sleep(5)
    @bot.message_handler(commands=['trex'])
    def handle_voice(message):
        voice_message(message)
    @bot.message_handler(commands=['weather'])
    def weather(message):
        name = message.text.strip().lower()
        url = "http://api.weatherapi.com/v1/current.json"
        api_weather_key = "55bb3557db2340cc923183355233005"
        location = name
        params = {
            "key": api_weather_key,
            "q": location,
            "aqi": "yes"
        }
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        location_name = data["location"]["name"]
        region = data["location"]["region"]
        country = data["location"]["country"]
        local_time = data["location"]["localtime"]
        current_temp_c = data["current"]["temp_c"]
        wind_speed_kph = data["current"]["wind_kph"]
        condition_text = data["current"]["condition"]["text"]
        air_quality_index = data["current"]["air_quality"]["us-epa-index"]
        last_updated_weather = data["current"]["last_updated"]
        response_message = f"Weather information for {location_name}:\n"
        response_message += f"Region: {region}\n"
        response_message += f"Country: {country}\n"
        response_message += f"Local Time: {local_time}\n"
        response_message += f"Current Temperature (Celsius): {current_temp_c}\n"
        response_message += f"Wind Speed (km/h): {wind_speed_kph}\n"
        response_message += f"Condition: {condition_text}\n"
        response_message += f"Air Quality Index: {air_quality_index}\n"
        response_message += f"Last Updated Weather: {last_updated_weather}"
        bot.reply_to(message, response_message)
    @bot.message_handler(commands=['news'])
    def news(message):
        category = message.text.split()[1]
        url = f"https://gnews.io/api/v4/top-headlines?category={urllib.parse.quote(category)}&lang=en&country=in&max=10&apikey={news_api}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
            articles = data["articles"]

            for i in range(len(articles)):
                response_message= f"Title: {articles[i]['title']}"
                response_message=f"Description: {articles[i]['description']}"
                bot.reply_to(message,response_message)
    @bot.message_handler(commands=['medi'])
    def medicine(message):
        m_name = message.text.strip().lower()
        prompt = f"Why is {m_name} medicine used?"
        response = get_chatgpt_response(prompt)
        bot.reply_to(message, response)
    bot.polling()
