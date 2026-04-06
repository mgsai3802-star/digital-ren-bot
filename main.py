import telebot
from flask import Flask, request
import os

# --- Bot Configuration ---
TOKEN = "8688726016:AAG7AqgFbRMPHO4w_MsOQeeqmhbE4c_TLnc"
ADMIN_ID = 1847021130 

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

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

# --- Services Handlers (ဈေးနှုန်းများ) ---

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
        "🎨 AI Fiesta Premium (1 Month) ➔  12,000 Ks"
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
        "• dren@gmail.com\n"
        "• drena@gmail.com\n"
        "• dren.a@gmail.com\n"
        "• dre.na@gmail.com\n"
        "• dr.ena@gmail.com\n\n"
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

# --- Forward & Reply System (ဒီအပိုင်းကို သေချာပြန်ပြင်ပေးထားပါတယ်) ---

@bot.message_handler(func=lambda message: True)
def handle_all(message):
    if message.chat.id != ADMIN_ID:
        if MAINTENANCE_MODE:
            bot.reply_to(message, "🛠 Bot ကို ပြုပြင်နေပါသည်။ @Ren2512 ထံ တိုက်ရိုက်စာပို့ပေးပါ။", parse_mode="Markdown")
            return
        
        c_name = message.from_user.first_name
        c_user = f"@{message.from_user.username}" if message.from_user.username else "No Username"
        
        # ID ကို Backtick ( ` ) ဖြင့် အုပ်ထားမှ Admin က Reply ပြန်လို့ရမှာပါ
        admin_msg = (
            f"📩 **Message အသစ်!**\n"
            f"👤 နာမည်: {c_name}\n"
            f"🔗 Username: {c_user}\n"
            f"🆔 ID: `{message.chat.id}`\n"
            f"📝 စာသား: {message.text}"
        )
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        
        if message.chat.id not in notified_users:
            bot.reply_to(message, "✅ လူကြီးမင်း၏စာကို Admin ထံ ပေးပို့လိုက်ပါပြီ။")
            notified_users.add(message.chat.id)
            
    elif message.reply_to_message and message.chat.id == ADMIN_ID:
        try:
            reply_text = message.reply_to_message.text
            # စာသားထဲမှ ID ကို Backtick များကြားမှ အတိအကျ ဆွဲထုတ်ခြင်း
            if "🆔 ID: `" in reply_text:
                target_id = int(reply_text.split("🆔 ID: `")[1].split("`")[0])
                bot.send_message(target_id, f"👨‍💻 **Admin မှ ပြန်ကြားစာ:**\n\n{message.text}")
                bot.send_message(ADMIN_ID, "✅ ပြန်စာပို့ပြီးပါပြီ။")
            else:
                bot.send_message(ADMIN_ID, "❌ ID ရှာမတွေ့ပါ။ ID ပါသော Bot စာကို Reply ထောက်ပေးပါ။")
        except Exception as e:
            bot.send_message(ADMIN_ID, f"❌ Error: {e}")

# --- Render Webhook Setup ---

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Forbidden", 403

@app.route("/")
def webhook():
    bot.remove_webhook()
    host_url = request.url_root.replace("http://", "https://")
    bot.set_webhook(url=host_url + TOKEN)
    return "✅ Ren Digital Bot is Ready!"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
    
