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

# Render တွင် Port Scan Error မတက်စေရန် Flask Keep-alive ဖွင့်ခြင်း
@app.route('/')
def index():
    return "✅ Ren Digital Bot is Running with Keep-alive!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# --- Global Variables ---
notified_users = set()
MAINTENANCE_MODE = False

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

# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
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
    msg = (
        "💎 **Telegram Premium Pricing**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "🔹 3 Months  ➔  53,000 MMK\n"
        "🔹 6 Months  ➔  75,000 MMK\n"
        "🔹 1 Year      ➔  130,000 MMK\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "💡 Gift အနေနဲ့ တိုက်ရိုက်ပို့ဆောင်ပေးမှာပါ။"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🌐 VPN ဝန်ဆောင်မှု")
def vpn_price(message):
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
        "❌Chat GPT မရသေးပါ"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🎬 Music & Entertainment")
def music_price(message):
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
    msg = (
        "🎬 **CapCut Pro Premium (All Devices)**\n"
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
        "✨ 4K Export, No Watermark, All Pro Effects!"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🌟 အခြားပရီမီယံများ")
def other_price(message):
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
    msg = (
        "🛡️ **Hotspot Shield VPN (7 Days Free)**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📧 **Accounts List:**\n"
        "• `renv@gmail.com` \n"
        "• `r.env@gmail.com` \n"
        "• `re.nv@gmail.com` \n"
        "• `ren.v@gmail.com` \n"
        "• `re.n.v@gmail.com` \n\n"
        "🔑 **Password** ➔ `Saithet111@222` \n"
        "📌 (အကောင့်တစ်ခုကို 10 devices သုံးရ)"
    )
    bot.reply_to(message, msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Admin နှင့် စကားပြောရန် သို့မဟုတ် Channel Join ရန်")
def admin_and_channel(message):
    text = (
        "👨‍💻 **Admin နှင့် ဆက်သွယ်ရန်**\n"
        "Admin (@Ren2512) ထံ တိုက်ရိုက်ဆက်သွယ်နိုင်သလို ဤ Bot ထဲတွင်လည်း စာရေးသားပေးပို့နိုင်ပါသည်။\n\n"
        "📢 **Channel Join ရန်**\n"
        "🔗 https://t.me/premiumren"
    )
    bot.reply_to(message, text, parse_mode="Markdown")

# --- Forward & Reply System (စာရော ပုံပါ ရအောင် ပြင်ထားသည်) ---

@bot.message_handler(content_types=['text', 'photo'])
def handle_all(message):
    if message.chat.id != ADMIN_ID:
        if MAINTENANCE_MODE:
            bot.reply_to(message, "🛠 Bot ကို ပြုပြင်နေပါသည်။ @Ren2512 ထံ တိုက်ရိုက်စာပို့ပေးပါ။")
            return
        
        c_name = message.from_user.first_name
        c_user = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        
        info_header = (
            f"📩 **Message အသစ်!**\n"
            f"👤 နာမည်: {c_name}\n"
            f"🔗 Username: {c_user}\n"
            f"🆔 ID: {message.chat.id}"
        )

        # Customer ဆီက စာသားလာရင်
        if message.content_type == 'text':
            admin_msg = f"{info_header}\n📝 စာသား: {message.text}"
            bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        
        # Customer ဆီက ဓာတ်ပုံလာရင်
        elif message.content_type == 'photo':
            caption = f"{info_header}\n🖼️ (Customer ထံမှ ဓာတ်ပုံ ပေးပို့ချက်)"
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=caption, parse_mode="Markdown")
        
        if message.chat.id not in notified_users:
            bot.reply_to(message, "✅ လူကြီးမင်း၏စာ (သို့မဟုတ် ဓာတ်ပုံ) ကို Admin ထံ ပေးပို့လိုက်ပါပြီ။")
            notified_users.add(message.chat.id)
            
    elif message.reply_to_message and message.chat.id == ADMIN_ID:
        try:
            # Reply ထောက်ထားတဲ့ စာ (သို့မဟုတ် Caption) ထဲကနေ ID ကို ရှာတယ်
            reply_to_text = message.reply_to_message.caption if message.reply_to_message.caption else message.reply_to_message.text
            found_ids = re.findall(r"ID: (\d+)", reply_to_text)
            
            if found_ids:
                target_id = int(found_ids[0])
                
                # Admin က စာပြန်ပို့ရင်
                if message.content_type == 'text':
                    bot.send_message(target_id, f"👨‍💻 **Admin မှ ပြန်ကြားစာ:**\n\n{message.text}")
                
                # Admin က ဓာတ်ပုံပြန်ပို့ရင်
                elif message.content_type == 'photo':
                    admin_caption = f"👨‍💻 **Admin မှ ပုံပို့လိုက်ပါတယ်:**\n\n{message.caption if message.caption else ''}"
                    bot.send_photo(target_id, message.photo[-1].file_id, caption=admin_caption)
                
                bot.send_message(ADMIN_ID, "✅ ပြန်စာပို့ပြီးပါပြီ။")
            else:
                bot.send_message(ADMIN_ID, "❌ ID ရှာမတွေ့ပါ။ ID ပါသော Bot စာကို Reply ထောက်ပေးပါ။")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Error: {str(e)}")

# --- Run Bot ---

if __name__ == "__main__":
    Thread(target=run_flask).start()
    print("🚀 Bot is starting with Long Polling + Keep-alive (Photo Support)...")
    
    bot.remove_webhook()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
