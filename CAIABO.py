import logging
import telegram
from telegram.ext import Updater, MessageHandler, Filters
import openai

token = '5729959955:AAHLojA6jmjsbbiim4lI_69swT8hxi9ML9A'

openai.api_key = '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'

# Configure the logging module
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Initialize the Telegram bot
bot = telegram.Bot(token)

# Define the function that will handle incoming messages
def handle_message(update, context):
    message = update.message
    print(message.text)
    if message.text != None:
        question = message.text

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are a chatbot named CAIABO"},
                    {"role": "user", "content": question},
                ]
        )

        result = ''
        for choice in response.choices:
            result += choice.message.content

        # Send the response message
        bot.send_message(chat_id=message.chat_id, text=result)

# Initialize the Telegram bot updater and add the message handler
updater = Updater(token, use_context=True)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
updater.dispatcher.add_handler(message_handler)

# Start the bot
updater.start_polling()
updater.idle()
