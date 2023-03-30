"""
KOLANI Julien le jeudi 30 mars 2023
ETUDIANT EN 3EME Année Systèmes et réseaux Ecole Polytechnique de LOME
github: https://github.com/julienkolani/CAIABO_project
PROJET : CAIABO_project
Custom Artificial Intelligence Assistant Based On OPenAi 
"""
import json
import openai
import logging
import telegram
import datetime
from telegram.ext import Updater, MessageHandler, Filters

import dataBase

# Variables globales

token = 'Votre token télégram ' 

"""Vous allez biensur devoir utiliser vos propres token et clé d'API"""

openai.api_key = ' Api key '

now = datetime.datetime.now()
heure_actuelle = now.strftime('%Y-%m-%d %H:%M:%S')

ex_reponse = None

#petite parathense :
"""Ce code configure le module de journalisation (logging) pour que les informations de journalisation soient affichées dans un format spécifique.
Il est important de configurer la journalisation dans un bot Telegram pour suivre les erreurs et les événements de manière efficace.
"""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

#Telegram bot
bot = telegram.Bot(token)

def requestMessageToApi (message):
    memoire = dataBase.read_memoire_info()
    history = dataBase.read_history(message.chat_id)
    question = message.text

    # Création de la requête d'achèvement de conversation OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": json.dumps(memoire)},
            {"role": "assistant", "content": json.dumps(history)},
            {"role": "user", "content": question},
        ]
    )

    return response



def requestToDataBase(message,ex_reponse):
    print("MESSAGE DATABASE")
    print(message.chat_id, heure_actuelle , message.text , ex_reponse)
    if(dataBase.get_user(message.chat_id)):
        pass
    else :
      dataBase.add_user(message.chat_id)

    dataBase.create_message(message.chat_id, heure_actuelle , message.text , ex_reponse)

# Define the function that will handle incoming messages
def handle_message(update, context):
    message = update.message

    try : 
        username = message.from_user.first_name
    except:
        username = "Utilisateur"

    print(message.text)

    if message.text != None:
        question = message.text

        try: 
            response = requestMessageToApi(message)

            result = ''
            for choice in response.choices:
                result += choice.message.content

            ex_reponse = result

            requestToDataBase(message,ex_reponse)
        except openai.error.InvalidRequestError as e:

            dataBase.clean_discussions_now()
            message_user = f"La longueur maximale du contexte de ce modèle est de 4097 tokens. Nous allons donc effacer votre historique afin de vous permettre de continuer à discuter. Merci, {username}"
            result = message_user

        # Envoie de la reponse à l'utilisateur spécifique 
        bot.send_message(chat_id=message.chat_id, text=result)

updater = Updater(token, use_context=True)
message_handler = MessageHandler(Filters.text & (~Filters.command), handle_message)
updater.dispatcher.add_handler(message_handler)

# lancement de CAIABO
updater.start_polling()
updater.idle()


