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

@app.route('/')
def index():
    return "✅ Ren Digital Bot is Running Perfectly!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# --- Database ---
USER_DB = "users.txt"
OLD_IDS = ["1847021130", "8577702613", "5389816539", "8413508432", "7662829742", "6050862261", "1693167795"]
order_times = {}

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

# --- Keyboards ---

def main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btns = ["💎 Telegram Premium", "🌐 VPN ဝန်ဆောင်မှု", "🤖 AI Premium Tools", "🎬 Music & Entertainment", "🎬 CapCut Pro Premium", "🌟 အခြားပရီမီယံများ", "🛡️ Hotspot Shield Free", "👨‍💻 Admin နှင့် ဆက်သွယ်ရန်"]
    markup.add(*(telebot.types.KeyboardButton(text) for text in btns))
    return markup

def tg_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 TG 3 Months", "🛒 TG 6 Months", "🛒 TG 1 Year", "🔙 Back")
    return markup

def vpn_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Express VPN", "🛒 HMA VPN", "🛒 NPV 50GB", "🛒 NPV 100GB", "🔙 Back")
    return markup

def ai_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Gemini 4M", "🛒 Gemini 1Y", "🛒 Perplexity Pro", "🛒 AI Fiesta", "🔙 Back")
    return markup

def music_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Spotify 1M", "🛒 Spotify 2M", "🛒 Spotify 3M", "🛒 Tidal Music", "🛒 Deezer Music", "🔙 Back")
    return markup

def capcut_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 CapCut 1 Month", "🛒 CapCut 6 Months", "🛒 CapCut 1 Year", "🔙 Back")
    return markup

def others_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add("🛒 Canva Edu", "🛒 PicsArt Pro", "🛒 Zoom License", "🛒 Gregmat+", "🔙 Back")
    return markup

def cancel_menu():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    markup.add("❌ ဝယ်ယူမှုကို ဖျက်သိမ်းမည် (Cancel)", "🔙 Main Menu")
    return markup

# --- Start Command ---
@bot.message_handler(commands=['start'])
def start(message):
    save_user(message.chat.id)
    user_name = message.from_user.first_name
    welcome_text = (f"မင်္ဂလာပါ **{user_name}** ခင်ဗျာ။ 🙏\n"
                    "**Ren Digital Service** မှ ကြိုဆိုပါတယ်ခင်ဗျ။\n\n"
                    "လိုအပ်တဲ့ ပရီမီယံများအတွက် အောက်က Menu ကိုနှိပ်၍ ကြည့်ရှုနိုင်ပါတယ်ခင်ဗျာ။")
    bot.send_message(message.chat.id, welcome_text, reply_markup=main_menu(), parse_mode="Markdown")

# --- Admin Commands ---

@bot.message_handler(commands=['userlist'])
def show_user_list(message):
    if message.chat.id == ADMIN_ID:
        if not os.path.exists(USER_DB):
            bot.reply_to(message, "❌ User စာရင်း မရှိသေးပါ။")
            return
        with open(USER_DB, "r") as f:
            users = f.read().splitlines()
        bot.reply_to(message, f"👥 **လက်ရှိ User စုစုပေါင်း ({len(users)} ယောက်):**\n\n`{', '.join(users)}`", parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id == ADMIN_ID:
        msg_text = message.text.replace("/broadcast", "").strip()
        if not msg_text:
            bot.reply_to(message, "❌ ပို့မည့်စာသား ထည့်ပေးပါ (ဥပမာ- /broadcast Hello)")
            return
        with open(USER_DB, "r") as f:
            users = f.read().splitlines()
        bot.send_message(ADMIN_ID, f"📢 လူပေါင်း {len(users)} ယောက်ကို စာပို့နေပါပြီ...")
        for user_id in users:
            try:
                bot.send_message(user_id, f"📢 **အကြောင်းကြားစာ**\n\n{msg_text}", parse_mode="Markdown")
                time.sleep(0.05)
            except: pass
        bot.send_message(ADMIN_ID, "✅ Broadcast လုပ်ပြီးပါပြီ။")

# --- Services Handlers ---

@bot.message_handler(func=lambda m: m.text in ["💎 Telegram Premium", "🌐 VPN ဝန်ဆောင်မှု", "🤖 AI Premium Tools", "🎬 Music & Entertainment", "🎬 CapCut Pro Premium", "🌟 အခြားပရီမီယံများ", "🛡️ Hotspot Shield Free", "👨‍💻 Admin နှင့် ဆက်သွယ်ရန်", "🔙 Back", "🔙 Main Menu"])
def show_pricing(message):
    t = message.text
    cid = message.chat.id
    save_user(cid)

    if t == "💎 Telegram Premium":
        msg = ("💎 **Telegram Premium Pricing**\n━━━━━━━━━━━━━━━━━━\n🔹 3 Months  ➔  53,000 MMK\n🔹 6 Months  ➔  75,000 MMK\n🔹 1 Year    ➔  130,000 MMK\n━━━━━━━━━━━━━━━━━━\n💡 Gift အနေနဲ့ တိုက်ရိုက်ပို့ဆောင်ပေးမှာပါ။")
        bot.send_message(cid, msg, reply_markup=tg_menu(), parse_mode="Markdown")
    elif t == "🌐 VPN ဝန်ဆောင်မှု":
        msg = ("🌐 **VPN Service Pricing**\n━━━━━━━━━━━━━━━━━━\n🚀 Express VPN (1 Month) ➔ 4,000 Ks\n🐢 HMA VPN (1 Month)     ➔ 10,000 Ks\n\n📡 **NPV Tunnel (1 Month)**\n• 50 GB Plan  ➔  5,000 Ks\n• 100 GB Plan ➔  10,000 Ks\n━━━━━━━━━━━━━━━━━━")
        bot.send_message(cid, msg, reply_markup=vpn_menu(), parse_mode="Markdown")
    elif t == "🤖 AI Premium Tools":
        msg = ("🤖 **AI Premium Tools**\n━━━━━━━━━━━━━━━━━━\n✨ Gemini AI (4 Months)    ➔  7,000 Ks\n✨ Gemini AI 5TB (1 Year)  ➔  40,000 Ks\n\n💬 ChatGPT (1 Month)       ➔  8,000 Ks\n💼 ChatGPT Business\n• Invite to mail     ➔  10,000 Ks\n• Own Acc (5 Inv)  ➔  20,000 Ks\n\n🔍 Perplexity Pro AI (1 Month) ➔  8,000 Ks\n🎨 AI Fiesta Premium (1 Month) ➔  12,000 Ks\n❌ Chat GPT မရသေးပါ")
        bot.send_message(cid, msg, reply_markup=ai_menu(), parse_mode="Markdown")
    elif t == "🎬 Music & Entertainment":
        msg = ("🎬 **Music & Entertainment**\n━━━━━━━━━━━━━━━━━━\n🎵 **Spotify Family Invite**\n• 1 Month   ➔  11,000 Ks\n• 2 Months  ➔  17,000 Ks\n• 3 Months  ➔  23,000 Ks\n\n🎧 **Spotify Individual Acc**\n• 1 Month   ➔  15,000 Ks\n• 3 Months  ➔  37,000 Ks\n\n🌊 Tidal Music (1 Month)   ➔  3,000 Ks\n🎼 Deezer Music (1 Month)  ➔  4,000 Ks")
        bot.send_message(cid, msg, reply_markup=music_menu(), parse_mode="Markdown")
    elif t == "🎬 CapCut Pro Premium":
        msg = ("🎬 **CapCut Pro Premium**\n━━━━━━━━━━━━━━━━━━\n📌 **1 Month Plan**\n• Share Account   ➔  9,000 Ks\n• Private Mail    ➔  14,000 Ks\n• Own Mail        ➔  16,000 Ks\n\n📌 **6 Month Plan**\n• Private Mail    ➔  45,000 Ks\n• Own Mail        ➔  54,000 Ks\n\n📌 **1 Year Plan**\n• Private Mail    ➔  74,000 Ks\n• Own Mail        ➔  84,000 Ks\n━━━━━━━━━━━━━━━━━━\n✨ 4K Export, No Watermark!")
        bot.send_message(cid, msg, reply_markup=capcut_menu(), parse_mode="Markdown")
    elif t == "🌟 အခြားပရီမီယံများ":
        msg = ("🌟 **Other Premium Services**\n━━━━━━━━━━━━━━━━━━\n🖼️ Canva Edu (1 Year)      ➔  5,000 Ks\n📸 PicsArt Pro (1 Month)   ➔  5,000 Ks\n📹 Zoom License (14 Days)  ➔  6,000 Ks\n📹 Zoom License (28 Days)  ➔  11,000 Ks\n📚 Gregmat+ (1 Month)      ➔  10,000 Ks")
        bot.send_message(cid, msg, reply_markup=others_menu(), parse_mode="Markdown")
    elif t == "🛡️ Hotspot Shield Free":
        msg = ("🛡️ **Hotspot Shield VPN (7 Days Free)**\n━━━━━━━━━━━━━━━━━━\n📧 **Accounts List:**\n• `waterfestival@gmail.com` \n• `w.aterfestival@gmail.com` \n• `wa.terfestival@gmail.com` \n• `wat.erfestival@gmail.com` \n• `wate.rfestival@gmail.com` \n\n🔑 **Password** ➔ `Saithet111@222` \n📌 (အကောင့်တစ်ခုကို 10 devices သုံးရ)")
        bot.send_message(cid, msg, parse_mode="Markdown")
    elif t in ["🔙 Back", "🔙 Main Menu"]:
        bot.send_message(cid, "မူလ Menu သို့ ပြန်ရောက်ပါပြီ။", reply_markup=main_menu())
    elif t == "👨‍💻 Admin နှင့် ဆက်သွယ်ရန်":
        msg = ("👨‍💻 **Admin နှင့် ဆက်သွယ်ရန်**\n\nAdmin (@Ren2512) ထံ တိုက်ရိုက်ဆက်သွယ်နိုင်သလို ဤ Bot ထဲတွင်လည်း စာရေးသားပေးပို့နိုင်ပါသည်။\n\n📢 **Channel Join ရန်**\n🔗 https://t.me/premiumren")
        bot.send_message(cid, msg, parse_mode="Markdown")

# --- Purchase Handler ---

@bot.message_handler(func=lambda m: m.text.startswith("🛒"))
def handle_buy(message):
    cid = message.chat.id
    order_times[cid] = int(time.time())
    item = message.text.replace("🛒 ", "")
    
    pay_msg = (
        f"✅ **{item}** အတွက် ဝယ်ယူမှုကို လက်ခံရရှိပါပြီ။\n\n"
        "Admin လိုင်းတက်စာပြန်မှ ငွေလွှဲပေးတာ ပိုအဆင်ပြေပါတယ်ဗျ။\n\n"
        "💰 **Payment Accounts:**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "📱 Kpay: `09776319707`\n"
        "📱 Wave: `09776319707`\n"
        "👤 Name: **Sai Thet Thu Aung**\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚠️ ငွေလွှဲပြီး Screenshot ပို့ပေးပါ။\n"
        "📌 *Cancel ကို ၃ မိနစ်အတွင်းသာ နှိပ်နိုင်ပါမည်။*"
    )
    bot.send_message(cid, pay_msg, reply_markup=cancel_menu(), parse_mode="Markdown")
    bot.send_message(ADMIN_ID, f"⚠️ **Order အသစ်!**\nItem: `{item}`\nUser: {message.from_user.first_name}\nID: `ID: {cid}`")

@bot.message_handler(func=lambda m: m.text == "❌ ဝယ်ယူမှုကို ဖျက်သိမ်းမည် (Cancel)")
def handle_cancel(message):
    cid = message.chat.id
    if cid in order_times and (int(time.time()) - order_times[cid]) <= 180:
        bot.send_message(cid, "❌ ဝယ်ယူမှုကို ဖျက်သိမ်းလိုက်ပါပြီ။", reply_markup=main_menu())
        bot.send_message(ADMIN_ID, f"🚫 **Order Cancel ဖြစ်သွားသည်**\nID: `{cid}`")
    else:
        bot.send_message(cid, "⚠️ ၃ မိနစ်ကျော်သွားပြီဖြစ်၍ Cancel လုပ်၍မရတော့ပါ။ Admin ကို ပြောပေးပါ။", reply_markup=main_menu())

# --- Media Forwarding ---

@bot.message_handler(content_types=['text', 'photo', 'document', 'audio', 'voice', 'video'])
def handle_media(message):
    if message.chat.id != ADMIN_ID:
        save_user(message.chat.id)
        info = f"📩 **Message အသစ်!**\n👤 {message.from_user.first_name}\n🆔 ID: {message.chat.id}"
        if message.content_type == 'text':
            bot.send_message(ADMIN_ID, f"{info}\n📝 {message.text}")
        elif message.content_type == 'photo':
            bot.send_photo(ADMIN_ID, message.photo[-1].file_id, caption=f"{info}\n🖼️ {message.caption or ''}")
        elif message.content_type == 'video':
            bot.send_video(ADMIN_ID, message.video.file_id, caption=f"{info}\n🎬 {message.caption or ''}")
        elif message.content_type == 'document':
            bot.send_document(ADMIN_ID, message.document.file_id, caption=f"{info}\n📄 {message.caption or ''}")
        
        if message.chat.id not in notified_users:
            bot.reply_to(message, "✅ စာကို Admin ထံ ပေးပို့လိုက်ပါပြီ။")
            notified_users.add(message.chat.id)
            
    elif message.reply_to_message and message.chat.id == ADMIN_ID:
        try:
            target_id = int(re.findall(r"ID: (\d+)", message.reply_to_message.caption or message.reply_to_message.text)[0])
            bot.send_message(target_id, f"👨‍💻 **Admin ပြန်စာ:**\n\n{message.text}")
            bot.send_message(ADMIN_ID, "✅ ပို့ပြီးပါပြီ။")
        except:
            bot.send_message(ADMIN_ID, "❌ ID ရှာမတွေ့ပါ။ ID ပါသောစာကို Reply ထောက်ပါ။")

if __name__ == "__main__":
    recover_old_ids()
    Thread(target=run_flask).start()
    bot.remove_webhook()
    time.sleep(1)
    bot.infinity_polling(timeout=30, long_polling_timeout=15)
            
