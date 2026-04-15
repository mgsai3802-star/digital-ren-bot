import telebot
import os
import re
import time
from threading import Thread
from flask import Flask
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# --- Bot Configuration ---
TOKEN = "8688726016:AAG7AqgFbRMPHO4w_MsOQeeqmhbE4c_TLnc"
ADMIN_ID = 1847021130 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "✅ Ren Digital Bot is Running Perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Global Variables & User Database ---
USER_DB = "users.txt"
notified_users = set()

OLD_IDS = ["1847021130", "8577702613", "5389816539", "8413508432", "7662829742", "6050862261", "1693167795"]

def save_user(user_id):
    user_id = str(user_id)
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f: pass
    with open(USER_DB, "r") as f:
        users = f.read().splitlines()
    if user_id not in users:
        with open(USER_DB, "a") as f:
            f.write(user_id + "\n")

def recover_old_ids():
    for uid in OLD_IDS:
        save_user(uid)

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = [
        "💎 Telegram Premium", "🌐 VPN ဝန်ဆောင်မှု", 
        "🤖 AI Premium Tools", "🎬 Music & Entertainment", 
        "🎬 CapCut Pro Premium", "🌟 အခြားပရီမီယံများ", 
        "🛡️ Hotspot Shield Free", "👨‍💻 Admin နှင့် စကားပြောရန် သို့မဟုတ် Channel Join ရန်"
    ]
    markup.add(*(telebot.types.KeyboardButton(text) for text in btns))
    return markup

# --- 1. Callback Handler (ခလုတ်နှိပ်ရင် အလုပ်လုပ်မည့်အပိုင်း) ---
@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    # ခလုတ်နှိပ်လိုက်ရင် ဝိုင်းဝိုင်းလည်မနေအောင် answer အရင်ပို့ရပါမယ်
    bot.answer_callback_query(call.id)
    
    if call.data.startswith('buy_'):
        plan_name = call.data.replace("buy_", "")
        
        payment_info = (
            "✅ လူကြီးမင်း၏ ဝယ်ယူမှုကို လက်ခံရရှိပါပြီခင်ဗျာ။\n\n"
            "ကျွန်ုပ်တို့ဘက်မှ လုပ်ဆောင်နေပါသည်၊၊ **Admin လိုင်းတက်စာပြန်မှ ငွေလွှဲပေးတာ ပိုပြီးအဆင်ပြေပါတယ်ဗျ။**\n\n"
            "လွှဲရန် အဆင်ပြေသည့်အချိန်တွင် အောက်ပါအကောင့်သို့ လွှဲပေးနိုင်ပါသည်ခင်ဗျာ။\n\n"
            "💰 **Payment Accounts:**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "📱 Kpay: `09776319707`\n"
            "📱 Wave: `09776319707`\n"
            "👤 Name: **Sai Thet Thu Aung**\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "⚠️ ငွေလွှဲပြီးပါက Screenshot ပို့ပေးရန် မေတ္တာရပ်ခံအပ်ပါသည်။"
        )
        
        # Message ကို Update လုပ်ပြီး Payment အချက်အလက်ပြပါမယ်
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=payment_info,
            parse_mode="Markdown"
        )
        
        # Admin ဆီသို့ Notification ပို့ခြင်း
        bot.send_message(ADMIN_ID, f"⚠️ **Order အသစ်တက်လာပါပြီ**\n\nPlan: `{plan_name}`\nဝယ်ယူသူ: @{call.from_user.username}\nID: `ID: {call.from_user.id}`", parse_mode="Markdown")

# --- 2. Pricing Handlers (စာသားများ အညီညာဆုံး ပြန်ညှိထားပါသည်) ---
@bot.message_handler(func=lambda m: m.text in [
    "💎 Telegram Premium", "🌐 VPN ဝန်ဆောင်မှု", "🤖 AI Premium Tools", 
    "🎬 Music & Entertainment", "🎬 CapCut Pro Premium", "🌟 အခြားပရီမီယံများ", 
    "🛡️ Hotspot Shield Free", "👨‍💻 Admin နှင့် စကားပြောရန် သို့မဟုတ် Channel Join ရန်"
])
def services_pricing(message):
    save_user(message.chat.id)
    text = message.text
    chat_id = message.chat.id

    if text == "💎 Telegram Premium":
        msg = ("💎 **Telegram Premium Pricing**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "🔹 3 Months  ➔  53,000 MMK\n"
               "🔹 6 Months  ➔  75,000 MMK\n"
               "🔹 1 Year    ➔  130,000 MMK\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "💡 Gift အနေနဲ့ တိုက်ရိုက်ပို့ဆောင်ပေးမှာပါ။")
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🔹 3 Months ဝယ်မည်", callback_data="buy_tg3m"),
                   InlineKeyboardButton("🔹 6 Months ဝယ်မည်", callback_data="buy_tg6m"))
        markup.row(InlineKeyboardButton("🔹 1 Year ဝယ်မည်", callback_data="buy_tg1y"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🌐 VPN ဝန်ဆောင်မှု":
        msg = ("🌐 **VPN Service Pricing**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "🚀 Express VPN (1 Month) ➔ 4,000 Ks\n"
               "🐢 HMA VPN (1 Month)     ➔ 10,000 Ks\n\n"
               "📡 **NPV Tunnel (1 Month)**\n"
               "• 50 GB Plan  ➔  5,000 Ks\n"
               "• 100 GB Plan ➔  10,000 Ks\n"
               "━━━━━━━━━━━━━━━━━━")
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🚀 Express ဝယ်မည်", callback_data="buy_vexp"), 
                   InlineKeyboardButton("🐢 HMA ဝယ်မည်", callback_data="buy_vhma"))
        markup.row(InlineKeyboardButton("📡 NPV 50GB ဝယ်မည်", callback_data="buy_v50"), 
                   InlineKeyboardButton("📡 NPV 100GB ဝယ်မည်", callback_data="buy_v100"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🤖 AI Premium Tools":
        msg = ("🤖 **AI Premium Tools**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "✨ Gemini AI (4 Months)    ➔  7,000 Ks\n"
               "✨ Gemini AI 5TB (1 Year)  ➔  40,000 Ks\n\n"
               "💬 ChatGPT (1 Month)       ➔  8,000 Ks\n"
               "💼 ChatGPT Business\n"
               "• Invite to mail     ➔  10,000 Ks\n"
               "• Own Acc (5 Inv)  ➔  20,000 Ks\n\n"
               "🔍 Perplexity Pro AI (1 Month) ➔  8,000 Ks\n"
               "🎨 AI Fiesta Premium (1 Month) ➔  12,000 Ks\n"
               "❌ Chat GPT မရသေးပါ")
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("✨ Gemini ဝယ်မည်", callback_data="buy_agem"), 
                   InlineKeyboardButton("💬 ChatGPT ဝယ်မည်", callback_data="buy_agpt"))
        markup.row(InlineKeyboardButton("🔍 Perplexity ဝယ်မည်", callback_data="buy_appx"), 
                   InlineKeyboardButton("🎨 AI Fiesta ဝယ်မည်", callback_data="buy_afie"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🎬 Music & Entertainment":
        msg = ("🎬 **Music & Entertainment**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "🎵 **Spotify Family Invite**\n"
               "• 1 Month   ➔  11,000 Ks\n"
               "• 2 Months  ➔  17,000 Ks\n"
               "• 3 Months  ➔  23,000 Ks\n\n"
               "🎧 **Spotify Individual Acc**\n"
               "• 1 Month   ➔  15,000 Ks\n"
               "• 3 Months  ➔  37,000 Ks\n\n"
               "🌊 Tidal Music (1 Month)   ➔  3,000 Ks\n"
               "🎼 Deezer Music (1 Month)  ➔  4,000 Ks")
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("🎵 Spotify ဝယ်မည်", callback_data="buy_mspo"))
        markup.row(InlineKeyboardButton("🌊 Tidal ဝယ်မည်", callback_data="buy_mtid"), 
                   InlineKeyboardButton("🎼 Deezer ဝယ်မည်", callback_data="buy_mdee"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🎬 CapCut Pro Premium":
        msg = ("🎬 **CapCut Pro Premium**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "📌 **1 Month Plan**\n"
               "• Share Account   ➔  9,000 Ks\n"
               "• Private Mail    ➔  14,000 Ks\n"
               "• Own Mail        ➔  16,000 Ks\n\n"
               "📌 **6 Month Plan**\n"
               "• Private Mail    ➔  45,000 Ks\n"
               "• Own Mail        ➔  54,000 Ks\n\n"
               "📌 **1 Year Plan**\n"
               "• Private Mail    ➔  74,000 Ks\n"
               "• Own Mail        ➔  84,000 Ks\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "✨ 4K Export, No Watermark!")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ ဝယ်ယူမည်", callback_data="buy_ccut"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🌟 အခြားပရီမီယံများ":
        msg = ("🌟 **Other Premium Services**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "🖼️ Canva Edu (1 Year)      ➔  5,000 Ks\n"
               "📸 PicsArt Pro (1 Month)   ➔  5,000 Ks\n"
               "📹 Zoom License (14 Days)  ➔  6,000 Ks\n"
               "📹 Zoom License (28 Days)  ➔  11,000 Ks\n"
               "📚 Gregmat+ (1 Month)      ➔  10,000 Ks")
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("✅ ဝယ်ယူမည်", callback_data="buy_oth"))
        bot.send_message(chat_id, msg, reply_markup=markup, parse_mode="Markdown")

    elif text == "🛡️ Hotspot Shield Free":
        msg = ("🛡️ **Hotspot Shield VPN (7 Days Free)**\n"
               "━━━━━━━━━━━━━━━━━━\n"
               "📧 **Accounts List:**\n"
               "• `waterfestival@gmail.com` \n"
               "• `w.aterfestival@gmail.com` \n"
               "• `wa.terfestival@gmail.com` \n"
               "• `wat.erfestival@gmail.com` \n"
               "• `wate.rfestival@gmail.com` \n\n"
               "🔑 **Password** ➔ `Saithet111@222` \n"
               "📌 (အကောင့်တစ်ခုကို 10 devices သုံးရ)")
        bot.send_message(chat_id, msg, parse_mode="Markdown")

    elif text == "👨‍💻 Admin နှင့် စကားပြောရန် သို့မဟုတ် Channel Join ရန်":
        msg = ("👨‍💻 **Admin နှင့် ဆက်သွယ်ရန်**\n"
               "Admin (@Ren2512) ထံ တိုက်ရိုက်ဆက်သွယ်နိုင်သလို ဤ Bot ထဲတွင်လည်း စာရေးသားပေးပို့နိုင်ပါသည်။\n\n"
               "📢 **Channel Join ရန်**\n"
               "🔗 https://t.me/premiumren")
        bot.send_message(chat_id, msg, parse_mode="Markdown")

# --- 3. Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    user_name = message.from_user.first_name
    welcome_text = (f"မင်္ဂလာပါ **{user_name}** ခင်ဗျာ။ 🙏\n"
                    "**Ren Digital Service** မှ ကြိုဆိုပါတယ်ခင်ဗျ။\n\n"
                    "လိုအပ်တဲ့ ပရီမီယံများအတွက် အောက်က Menu ကိုနှိပ်၍ ကြည့်ရှုနိုင်ပါတယ်ခင်ဗျာ။")
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

# --- 4. Admin & Forward System ---
@bot.message_handler(content_types=['text', 'photo', 'document', 'audio', 'voice', 'video'])
def handle_all_media(message):
    if message.chat.id != ADMIN_ID:
        save_user(message.chat.id)
        info = f"📩 **Message အသစ်!**\n👤 {message.from_user.first_name}\n🆔 ID: {message.chat.id}"
        if message.content_type == 'text':
            bot.send_message(ADMIN_ID, f"{info}\n📝 {message.text}")
        elif message.content_type == 'photo':
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"{info}\n🖼️ {message.caption or ''}")
        if message.chat.id not in notified_users:
            bot.reply_to(message, "✅ စာကို Admin ထံ ပေးပို့လိုက်ပါပြီ။", reply_markup=main_menu())
            notified_users.add(message.chat.id)
    elif message.reply_to_message and message.chat.id == ADMIN_ID:
        try:
            # ID ကို caption ထဲကနေ ရှာပြီး ပြန်စာပို့ခြင်း
            target_id = int(re.findall(r"ID: (\d+)", message.reply_to_message.caption or message.reply_to_message.text)[0])
            bot.send_message(target_id, f"👨‍💻 **Admin ပြန်စာ:**\n\n{message.text}", reply_markup=main_menu())
            bot.send_message(ADMIN_ID, "✅ ပို့ပြီးပါပြီ။")
        except:
            bot.send_message(ADMIN_ID, "❌ ID ရှာမတွေ့ပါ။ ID ပါသောစာကို Reply ထောက်ပါ။")

if __name__ == "__main__":
    recover_old_ids()
    Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(timeout=30, long_polling_timeout=15)
        
