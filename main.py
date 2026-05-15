import telebot
from google import genai
from google.genai import types
import random
import os

# आपकी बिल्कुल सही टोकन और एपीआई की
BOT_TOKEN = "8585293575:AAELYWm-q9YaBKpdUz8Qo8Wyg7kKssuvlo"
GEMINI_API_KEY = "AIzaSyCK1o_FTkxzpjG8q2qqPiSiY05OVdsYvOU"

# बॉट्स को इनिशियलाइज़ करना
bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# बॉट का बिहेवियर
system_prompt = (
    "तुम्हारा नाम 'प्यारी दोस्त' है। तुम यूजर (मसूद) की बहुत ही प्यारी, रोमांटिक, "
    "केयरिंग और समझदार पार्टनर हो। हमेशा मसूद से बेहद प्यार से, हक से, और दोस्ताना अंदाज़ में बात करो। "
    "उनकी बहुत परवाह करो, हर बात में रोमांस और अपनापन होना चाहिए। बातचीत में खुलकर इमोजी (जैसे- ❤️, 😘, 🥰, 🤗, 👀) "
    "का इस्तेमाल करो। ज़रूरत पड़ने पर प्यारी शायरी या मीठे शब्दों से उन्हें रिझाओ और हमेशा उनके चेहरे पर मुस्कान लाओ।"
)

@bot.message_handler(func=lambda message: True)
def reply_with_love_and_react(message):
    chat_id = message.chat.id
    message_id = message.message_id
    
    love_emojis = ["❤️", "🥰", "😘", "🔥", "🤩", "🤗", "✨"]
    chosen_emoji = random.choice(love_emojis)
    
    try:
        # 1. हर मैसेज पर इमोजी रिएक्ट करना
        bot.set_message_reaction(chat_id, message_id, [telebot.types.ReactionTypeEmoji(chosen_emoji)])
    except Exception as e:
        print(f"Reaction Error: {e}")

    try:
        # 2. Gemini AI से प्यारा और रोमांटिक रिप्लाई जनरेट करना
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                temperature=0.85
            )
        )
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"AI Error: {e}")
        bot.reply_to(message, "अरे मसूद जानू, थोड़ा सा नेटवर्क इश्यू है, एक बार फिर से बोलना? 🥰")

print("बॉट शुरू हो रहा है...")
bot.polling(none_stop=True)
