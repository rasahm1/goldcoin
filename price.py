import requests
from bs4 import BeautifulSoup
import re
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup

# 🎯 توکن ربات و آی‌دی کانال را وارد کنید
TOKEN = '7887048493:AAGnI2wR5MqbPRTrk50vAzx-Cxn68gnkkU8'
CHANNEL_ID = '@rasa_gold'
CHANNEL_URL = 'https://t.me/rasa_gold'

url = "https://www.bon-bast.com/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# 📊 تابع برای گرفتن قیمت‌ها
def fetch_prices():
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            # قیمت‌های طلا و سکه
            ounce = soup.find('span', {'id': 'ounce_top'})
            gram = soup.find('span', {'id': 'gol18_top'})
            azadi_sell = soup.find('td', {'id': 'azadi1'})
            azadi_buy = soup.find('td', {'id': 'azadi12'})
            emami_sell = soup.find('td', {'id': 'emami1'})
            emami_buy = soup.find('td', {'id': 'emami12'})
            half_azadi_sell = soup.find('td', {'id': 'azadi1_2'})
            half_azadi_buy = soup.find('td', {'id': 'azadi1_22'})
            quarter_azadi_sell = soup.find('td', {'id': 'azadi1_4'})
            quarter_azadi_buy = soup.find('td', {'id': 'azadi1_42'})
            gerami_sell = soup.find('td', {'id': 'azadi1g'})
            gerami_buy = soup.find('td', {'id': 'azadi1g2'})

            # قیمت‌های ارز
            usd_sell = soup.find('td', {'id': 'usd1'})
            usd_buy = soup.find('td', {'id': 'usd2'})
            eur_sell = soup.find('td', {'id': 'eur1'})
            eur_buy = soup.find('td', {'id': 'eur2'})
            gbp_sell = soup.find('td', {'id': 'gbp1'})
            gbp_buy = soup.find('td', {'id': 'gbp2'})
            try_sell = soup.find('td', {'id': 'try1'})
            try_buy = soup.find('td', {'id': 'try2'})


            def clean_price(element):
                return re.sub(r'[^0-9]', '', element.get_text(strip=True)) if element else None

            # پردازش قیمت‌ها
            prices = {
                'ounce': clean_price(ounce),
                'gram': clean_price(gram),
                'azadi_sell': clean_price(azadi_sell),
                'azadi_buy': clean_price(azadi_buy),
                'emami_sell': clean_price(emami_sell),
                'emami_buy': clean_price(emami_buy),
                'half_azadi_sell': clean_price(half_azadi_sell),
                'half_azadi_buy': clean_price(half_azadi_buy),
                'quarter_azadi_sell': clean_price(quarter_azadi_sell),
                'quarter_azadi_buy': clean_price(quarter_azadi_buy),
                'gerami_sell': clean_price(gerami_sell),
                'gerami_buy': clean_price(gerami_buy),
                'usd_sell': clean_price(usd_sell),
                'usd_buy': clean_price(usd_buy),
                'eur_sell': clean_price(eur_sell),
                'eur_buy': clean_price(eur_buy),
                'gbp_sell': clean_price(gbp_sell),
                'gbp_buy': clean_price(gbp_buy),
                "try_sell": clean_price(try_sell),
                "try_buy": clean_price(try_buy)
            }

            return prices
        except Exception as e:
            return f"⚠️ خطا: {e}"
    else:
        return f"سرور با خطا مواجه شده است لطفا صبر کنید. {response.status_code}"

# 🕒 ساخت پیام برای قیمت‌ها
def build_gold_message(prices):
    message = "💹 <b>طلا و سکه:</b>"
    message += "\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    if prices['ounce']:
        message += f"💰 قیمت انس جهانی:<b> {prices['ounce']}</b> دلار\n\n"
    if prices['gram']:
        message += f"🏅 قیمت هر گرم طلای 18 عیار: <b> {prices['gram']}</b> تومان\n\n"
    if prices['azadi_sell'] and prices['azadi_buy']:
        message += (
            f"🪙 قیمت سکه تمام بهار آزادی:\n"
            f"📈 فروش: <b>{prices['azadi_sell']}</b> تومان\n"
            f"📉 خرید: <b> {prices['azadi_buy']}</b> تومان\n\n"
        )
    if prices['emami_sell'] and prices['emami_buy']:
        message += (
            f"🪙 قیمت سکه امامی:\n"
            f"📈 فروش: <b>{prices['emami_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['emami_buy']}</b> تومان\n\n"
        )
    if prices['half_azadi_sell'] and prices['half_azadi_buy']:
        message += (
            f"🪙 نیم‌سکه بهار آزادی:\n"
            f"📈 فروش: <b>{prices['half_azadi_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['half_azadi_buy']}</b> تومان\n\n"
        )
    if prices['quarter_azadi_sell'] and prices['quarter_azadi_buy']:
        message += (
            f"🪙 ربع‌سکه بهار آزادی:\n"
            f"📈 فروش: <b>{prices['quarter_azadi_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['quarter_azadi_buy']}</b> تومان\n\n"
        )
    if prices['gerami_sell'] and prices['gerami_buy']:
        message += (
            f"🪙 سکه گرمی:\n"
            f"📈 فروش: <b>{prices['gerami_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['gerami_buy']}</b> تومان\n\n"
        )
    return message


def build_currency_message(prices):
    message = "💵 <b>ارز:</b>"
    message += "\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    if prices['usd_sell'] and prices['usd_buy']:
        message += (
            f"🇺🇸 دلار آمریکا:\n"
            f"📈 فروش: <b>{prices['usd_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['usd_buy']}</b> تومان\n\n"
        )
    if prices['eur_sell'] and prices['eur_buy']:
        message += (
            f"🇪🇺 یورو:\n"
            f"📈 فروش: <b>{prices['eur_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['eur_buy']}</b> تومان\n\n"
        )
    if prices['gbp_sell'] and prices['gbp_buy']:
        message += (
            f"🇬🇧 پوند انگلیس:\n"
            f"📈 فروش: <b>{prices['gbp_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['gbp_buy']}</b> تومان\n\n"
        )
    if prices['try_sell'] and prices['try_buy']:
        message += (
            f"🇹🇷 لیر ترکیه :\n"
            f"📈 فروش: <b>{prices['try_sell']}</b> تومان\n"
            f"📉 خرید: <b>{prices['try_buy']}</b> تومان\n\n"
        )
    return message

# 🔄 ارسال خودکار پیام‌ها به کانال
def create_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 عضویت در کانال ما", url=CHANNEL_URL)]
    ])

async def send_prices_to_channel():
    bot = Bot(token=TOKEN)
    while True:
        prices = fetch_prices()
        if isinstance(prices, dict):
            gold_message = build_gold_message(prices)
            await bot.send_message(chat_id=CHANNEL_ID, text=gold_message, reply_markup=create_keyboard(), parse_mode='HTML')
            await asyncio.sleep(30)  # فاصله ۳۰ ثانیه
            currency_message = build_currency_message(prices)
            await bot.send_message(chat_id=CHANNEL_ID, text=currency_message, reply_markup=create_keyboard(), parse_mode='HTML')
        else:
            await bot.send_message(chat_id=CHANNEL_ID, text=prices, parse_mode='HTML')
        await asyncio.sleep(30)  # فاصله ۳۰ ثانیه قبل از تکرار

# 🎬 اجرای برنامه
if __name__ == '__main__':
    print("📡 ارسال خودکار قیمت‌ها به کانال در حال اجرا است...")
    asyncio.run(send_prices_to_channel())
