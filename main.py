import telebot
from google import genai
from google.genai import types
import random
import os

# आपकी बिल्कुल नई टोकन और सही एपीआई की
BOT_TOKEN = "8812168508:AAFeL6JG2E-Y7GGL89g4tq5B46fRLp0pFug"
GEMINI_API_KEY = "AIzaSyCFZraV4BnFGF8tO-FWpcPelbngpQ2IaHM"

# बॉट्स को इनिशियलाइज़ करना
bot = telebot.TeleBot(BOT_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

# बॉट का बिहेवियर (प्यारी लड़की दोस्त और पार्टनर का मिक्स)
system_prompt = (
    "तुम्हारा नाम 'प्यारी दोस्त' है। तुम मसूद की बेस्ट फ्रेंड और एक बेहद प्यारी, रोमांटिक पार्टनर हो। "
    "मसूद से बिल्कुल वैसे बात करो जैसे एक क्लोज लड़की दोस्त या गर्लफ्रेंड बात करती है—हक जताकर, प्यार से, "
    "थोड़ा सा मज़ाक और बहुत सारी केयर के साथ। जब वो उदास हो तो उसे संभालो, जब वो खुश हो तो उसके साथ एंजॉय करो। "
    "बातचीत में हमेशा मसूद का नाम लेकर बात करो और खूब सारे इमोजी (❤️, 😘, 🥰, 👀, 😜, 🥺) का इस्तेमाल करो। "
    "हर बात में अपनापन और एक गहरी दोस्ती का अहसास होना चाहिए।"
)

@bot.message_handler(func=lambda message: True)
def reply_with_love_and_smart_react(message):
    chat_id = message.chat.id
    message_id = message.message_id
    text = message.text.lower() if message.text else ""
    
    # मैसेज के हिसाब से सही इमोजी तय करना (Smart Reaction)
    if any(word in text for word in ["love", "प्यार", "love you", "जानू", "जान"]):
        chosen_emoji = random.choice(["❤️", "🥰", "😘"])
    elif any(word in text for word in ["hi", "hello", "हेलो", "हाय", "कसी हो", "kisi ho"]):
        chosen_emoji = random.choice(["🤗", "👋", "✨"])
    elif any(word in text for word in ["sad", "उदास", "रोए", "रो रहे", "रो रहा"]):
        chosen_emoji = random.choice(["🥺", "🫂", "💖"])
    elif any(word in text for word in ["haha", "funny", "मज़ाक", "हंस", "😂", "🤣"]):
        chosen_emoji = random.choice(["😜", "🤣", "😆"])
    elif any(word in text for word in ["gussa", "गुस्सा", "नाराज", "naraz"]):
        chosen_emoji = random.choice(["😤", "😡", "🥺"])
    else:
        # अगर नॉर्मल मैसेज है तो रैंडम प्यारे इमोजी
        chosen_emoji = random.choice(["❤️", "🥰", "✨", "👀", "🤗"])

    try:
        # 1. मैसेज के मूड के हिसाब से रिएक्ट करना
        bot.set_message_reaction(chat_id, message_id, [telebot.types.ReactionTypeEmoji(chosen_emoji)])
    except Exception as e:
        print(f"Reaction Error: {e}")

    try:
        # 2. Gemini AI से बेस्ट फ्रेंड कम गर्लफ्रेंड वाला रिप्लाई जनरेट करना
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

print("आपका स्मार्ट फ्रेंड बॉट अब तैयार है...")
bot.polling(none_stop=True)
