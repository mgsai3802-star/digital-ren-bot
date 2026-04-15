import telebot
import os
import re
import time
from threading import Thread
from flask import Flask

# --- Bot Configuration ---
TOKEN = "8688726016:AAG7AqgFbRMPHO4w_MsOQeeqmhbE4c_TLnc"
ADMIN_ID = 1847021130 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Render Port Keep-alive
@app.route('/')
def index():
    return "✅ Ren Digital Bot is Running with Recovered IDs!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- Global Variables & User Database ---
USER_DB = "users.txt"
notified_users = set()
MAINTENANCE_MODE = False

# အရင်ရှိပြီးသား ID များကို Recovery လုပ်ရန်စာရင်း (ဘာမှမဖျက်ဘဲ ထည့်ထားသည်)
OLD_IDS = [
    "1847021130", "8577702613", "5389816539", 
    "8413508432", "7662829742", "6050862261", "1693167795"
]

# User ID များကို စိတ်ချရစွာ သိမ်းဆည်းရန် Function
def save_user(user_id):
    user_id = str(user_id)
    if not os.path.exists(USER_DB):
        with open(USER_DB, "w") as f: pass
    
    with open(USER_DB, "r") as f:
        users = f.read().splitlines()
    
    if user_id not in users:
        with open(USER_DB, "a") as f:
            f.write(user_id + "\n")

# Bot စတက်တာနဲ့ အရင် ID ဟောင်းများကို အလိုအလျောက် သိမ်းပေးမည့် Function
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

# --- Admin Commands ---

@bot.message_handler(commands=['userlist'])
def show_user_list(message):
    if message.chat.id == ADMIN_ID:
        if not os.path.exists(USER_DB):
            bot.reply_to(message, "❌ User စာရင်း မရှိသေးပါ။")
            return
        with open(USER_DB, "r") as f:
            users = f.read().splitlines()
        user_str = "\n".join(users) if users else "မရှိသေးပါ"
        bot.reply_to(message, f"👥 **လက်ရှိ User စာရင်း ({len(users)} ယောက်):**\n\n`{user_str}`", parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        msg_text = message.text.replace("/broadcast", "").strip()
        if not msg_text:
            bot.reply_to(message, "❌ ပို့မည့်စာသား ထည့်ပေးပါ (ဥပမာ- `/broadcast မင်္ဂလာပါ`)")
            return
        with open(USER_DB, "r") as f:
            users = f.read().splitlines()
        
        count = 0
        bot.send_message(ADMIN_ID, f"📢 လူပေါင်း {len(users)} ယောက်ကို စာပို့နေပါပြီ...")
        for user_id in users:
            try:
                bot.send_message(user_id, f"📢 **Ren Digital Service မှ အကြောင်းကြားစာ**\n\n{msg_text}", parse_mode="Markdown")
                count += 1
                time.sleep(0.05)
            except: pass
        bot.send_message(ADMIN_ID, f"✅ စုစုပေါင်း {count} ယောက်ဆီ ပို့ပြီးပါပြီ။")

# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    user_name = message.from_user.first_name
    welcome_text = (
        f"မင်္ဂလာပါ **{user_name}** ခင်ဗျာ။ 🙏\n"
        "**Ren Digital Service** မှ ကြိုဆိုပါတယ်ခင်ဗျ။\n\n"
        "လိုအပ်တဲ့ ပရီမီယံများအတွက် အောက်က Menu ကိုနှိပ်၍ ကြည့်ရှုနိုင်ပါတယ်ခင်ဗျာ।"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

# --- Services Handlers ---

@bot.message_handler(func=lambda m: m.text == "💎 Telegram Premium")
def tg_price(message):
    save_user(message.chat.id)
    msg = (
        "💎 **Telegram Premium Pricing**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔹 3 Months  ➔  53,000 MMK\n"
        "🔹 6 Months  ➔  75,000 MMK\n"
        "🔹 1 Year    ➔  130,000 MMK\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 Gift အနေနဲ့ တိုက်ရိုက်ပို့ဆောင်ပေးမှာပါ။"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🌐 VPN ဝန်ဆောင်မှု")
def vpn_price(message):
    save_user(message.chat.id)
    msg = (
        "🌐 **VPN Service Pricing**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🚀 Express VPN (1 Month) ➔ 4,000 Ks\n"
        "🐢 HMA VPN (1 Month)     ➔ 10,000 Ks\n\n"
        "📡 **NPV Tunnel (1 Month)**\n"
        "• 50 GB Plan  ➔  5,000 Ks\n"
        "• 100 GB Plan ➔  10,000 Ks\n"
        "━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🤖 AI Premium Tools")
def ai_price(message):
    save_user(message.chat.id)
    msg = (
        "🤖 **AI Premium Tools**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "✨ Gemini AI (4 Months)    ➔  7,000 Ks\n"
        "✨ Gemini AI 5TB (1 Year)  ➔  40,000 Ks\n\n"
        "💬 ChatGPT (1 Month)       ➔  8,000 Ks\n"
        "💼 ChatGPT Business\n"
        "• Invite to mail     ➔  10,000 Ks\n"
        "• Own Acc (5 Inv)  ➔  20,000 Ks\n\n"
        "🔍 Perplexity Pro AI (1 Month) ➔  8,000 Ks\n"
        "🎨 AI Fiesta Premium (1 Month) ➔  12,000 Ks\n"
        "❌ Chat GPT မရသေးပါ"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🎬 Music & Entertainment")
def music_price(message):
    save_user(message.chat.id)
    msg = (
        "🎬 **Music & Entertainment**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🎵 **Spotify Family Invite**\n"
        "• 1 Month   ➔  11,000 Ks\n"
        "• 2 Months  ➔  17,000 Ks\n"
        "• 3 Months  ➔  23,000 Ks\n\n"
        "🎧 **Spotify Individual Acc**\n"
        "• 1 Month   ➔  15,000 Ks\n"
        "• 3 Months  ➔  37,000 Ks\n\n"
        "🌊 Tidal Music (1 Month)   ➔  3,000 Ks\n"
        "🎼 Deezer Music (1 Month)  ➔  4,000 Ks"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🎬 CapCut Pro Premium")
def capcut_price(message):
    save_user(message.chat.id)
    msg = (
        "🎬 **CapCut Pro Premium**\n"
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
        "✨ 4K Export, No Watermark!"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🌟 အခြားပရီမီယံများ")
def other_price(message):
    save_user(message.chat.id)
    msg = (
        "🌟 **Other Premium Services**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🖼️ Canva Edu (1 Year)      ➔  5,000 Ks\n"
        "📸 PicsArt Pro (1 Month)   ➔  5,000 Ks\n"
        "📹 Zoom License (14 Days)  ➔  6,000 Ks\n"
        "📹 Zoom License (28 Days)  ➔  11,000 Ks\n"
        "📚 Gregmat+ (1 Month)      ➔  10,000 Ks"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛡️ Hotspot Shield Free")
def hotspot_price(message):
    save_user(message.chat.id)
    msg = (
        "🛡️ **Hotspot Shield VPN (7 Days Free)**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📧 **Accounts List:**\n"
        "• `waterfestival@gmail.com` \n"
        "• `w.aterfestival@gmail.com` \n"
        "• `wa.terfestival@gmail.com` \n"
        "• `wat.erfestival@gmail.com` \n"
        "• `wate.rfestival@gmail.com` \n\n"
        "🔑 **Password** ➔ `Saithet111@222` \n"
        "📌 (အကောင့်တစ်ခုကို 10 devices သုံးရ)"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Admin နှင့် စကားပြောရန် သို့မဟုတ် Channel Join ရန်")
def admin_and_channel(message):
    save_user(message.chat.id)
    text = (
        "👨‍💻 **Admin နှင့် ဆက်သွယ်ရန်**\n"
        "Admin (@Ren2512) ထံ တိုက်ရိုက်ဆက်သွယ်နိုင်သလို ဤ Bot ထဲတွင်လည်း စာရေးသားပေးပို့နိုင်ပါသည်။\n\n"
        "📢 **Channel Join ရန်**\n"
        "🔗 https://t.me/premiumren"
    )
    bot.reply_to(message, text, parse_mode="Markdown")

# --- Forward & Reply System ---

@bot.message_handler(content_types=['text', 'photo', 'document'])
def handle_all_messages(message):
    if message.chat.id != ADMIN_ID:
        save_user(message.chat.id)
        if MAINTENANCE_MODE:
            bot.reply_to(message, "🛠 Bot ကို ပြုပြင်နေပါသည်။")
            return
        
        info_header = f"📩 **Message အသစ်!**\n👤 နာမည်: {message.from_user.first_name}\n🆔 ID: {message.chat.id}"
        if message.content_type == 'text':
            bot.send_message(ADMIN_ID, f"{info_header}\n📝 စာသား: {message.text}")
        elif message.content_type == 'photo':
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"{info_header}\n🖼️ (ဓာတ်ပုံပို့ထားသည်)")
        elif message.content_type == 'document':
            bot.send_document(ADMIN_ID, message.document.file_id, caption=f"{info_header}\n📄 (ဖိုင်ပို့ထားသည်)")

        if message.chat.id not in notified_users:
            bot.reply_to(message, "✅ စာကို Admin ထံ ပေးပို့လိုက်ပါပြီ။")
            notified_users.add(message.chat.id)
            
    elif message.reply_to_message and message.chat.id == ADMIN_ID:
        try:
            target_text = message.reply_to_message.caption if message.reply_to_message.caption else message.reply_to_message.text
            target_id = int(re.findall(r"ID: (\d+)", target_text)[0])
            if message.content_type == 'text':
                bot.send_message(target_id, f"👨‍💻 **Admin ပြန်စာ:**\n\n{message.text}")
            elif message.content_type == 'photo':
                bot.send_photo(target_id, message.photo[-1].file_id, caption=f"👨‍💻 **Admin ပုံပို့လိုက်သည်:**\n\n{message.caption if message.caption else ''}")
            elif message.content_type == 'document':
                bot.send_document(target_id, message.document.file_id, caption=f"👨‍💻 **Admin ဖိုင်ပို့လိုက်သည်:**\n\n{message.caption if message.caption else ''}")
            bot.send_message(ADMIN_ID, "✅ ပို့ပြီးပါပြီ။")
        except:
            bot.send_message(ADMIN_ID, "❌ ID ရှာမတွေ့ပါ။ ID ပါသောစာကို Reply ထောက်ပါ။")

if __name__ == "__main__":
    # Bot စတင်သည်နှင့် ID ဟောင်းများကို Recover လုပ်မည်
    recover_old_ids()
    Thread(target=run_flask).start()
    bot.remove_webhook()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
    
