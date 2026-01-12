import telebot
from telebot import types
import json

# Конфигурация
BOT_TOKEN = "8528658688:AAHTvP1HFVOI5lhDmrlIRlIBfv7kGFqfy5A"
MANAGER_CHAT_ID = 100885885
CARD_NUMBER = "1111"  # Замените на реальный номер карты

# URL вашего Mini App (замените после деплоя на Render)
WEBAPP_URL = "https://your-app-name.onrender.com"

bot = telebot.TeleBot(BOT_TOKEN)

def get_main_menu():
    """Главное меню с Web App"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Кнопка открытия Mini App
    webapp_btn = types.KeyboardButton(
        text="🛒 Открыть магазин",
        web_app=types.WebAppInfo(url=WEBAPP_URL)
    )
    markup.add(webapp_btn)
    markup.add(types.KeyboardButton("💰 Цена"))
    markup.add(types.KeyboardButton("📞 Связаться с нами"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    """Приветствие"""
    # Отправляем фото товара
    try:
        with open('product.png', 'rb') as photo:
            bot.send_photo(
                message.chat.id,
                photo,
                caption="""
🌿 *Добро пожаловать в Softy!*

Натуральные эко-грелки из вишнёвых косточек.

✨ *Преимущества:*
• 100% натуральные материалы
• Сохраняет тепло до 2 часов
• Приятный аромат
• Безопасно для здоровья

💰 *Цена:* 250 000 сум

Нажмите кнопку ниже, чтобы оформить заказ 👇
""",
                parse_mode="Markdown",
                reply_markup=get_main_menu()
            )
    except:
        bot.send_message(
            message.chat.id,
            """
🌿 *Добро пожаловать в Softy!*

Натуральные эко-грелки из вишнёвых косточек.

💰 *Цена:* 250 000 сум

Нажмите кнопку ниже, чтобы оформить заказ 👇
""",
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )

@bot.message_handler(func=lambda m: m.text == "💰 Цена")
def show_price(message):
    """Показать цену"""
    bot.send_message(
        message.chat.id,
        """
💰 *Эко-грелка Softy*

*Цена:* 250 000 сум

✅ В стоимость входит:
• Грелка из натуральных материалов
• Красивая упаковка
• Доставка по Ташкенту

Нажмите "🛒 Открыть магазин" чтобы заказать!
""",
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda m: m.text == "📞 Связаться с нами")
def contact_us(message):
    """Контакты"""
    bot.send_message(
        message.chat.id,
        """
📞 *Связаться с нами*

Если у вас есть вопросы, напишите нам!

Мы ответим в ближайшее время 💛
""",
        parse_mode="Markdown"
    )
    
    # Уведомляем менеджера
    bot.send_message(
        MANAGER_CHAT_ID,
        f"📞 Клиент хочет связаться!\n\n👤 @{message.from_user.username or 'Нет username'}\n🆔 {message.chat.id}"
    )

@bot.message_handler(content_types=['web_app_data'])
def handle_webapp_data(message):
    """Обработка данных из Mini App"""
    try:
        data = json.loads(message.web_app_data.data)
        
        # Подтверждение клиенту
        bot.send_message(
            message.chat.id,
            f"""
✅ *Заказ принят!*

📦 *Товар:* {data.get('product', 'Эко-грелка')}
🔢 *Количество:* {data.get('quantity', 1)} шт.
💰 *Сумма:* {data.get('total', 250000):,} сум

📍 *Доставка:* {data.get('address', 'Не указан')}

Спасибо за заказ! Мы свяжемся с вами для подтверждения 💛
""".replace(',', ' '),
            parse_mode="Markdown",
            reply_markup=get_main_menu()
        )
        
        # Отправка менеджеру
        order_text = f"""
🆕 *НОВЫЙ ЗАКАЗ из Mini App!*

👤 *Клиент:* {data.get('name', 'Не указано')}
📱 *Телефон:* {data.get('phone', 'Не указано')}
📍 *Адрес:* {data.get('address', 'Не указано')}

📦 *Товар:* {data.get('product', 'Эко-грелка')}
🔢 *Количество:* {data.get('quantity', 1)} шт.
💰 *Сумма:* {data.get('total', 250000):,} сум

🆔 *Chat ID:* {message.chat.id}
👤 *Username:* @{message.from_user.username or 'Нет'}
""".replace(',', ' ')
        
        bot.send_message(MANAGER_CHAT_ID, order_text, parse_mode="Markdown")
        
    except Exception as e:
        print(f"Ошибка обработки данных: {e}")
        bot.send_message(
            message.chat.id,
            "Произошла ошибка. Пожалуйста, попробуйте ещё раз.",
            reply_markup=get_main_menu()
        )

@bot.message_handler(func=lambda m: True)
def handle_other(message):
    """Обработка прочих сообщений"""
    bot.send_message(
        message.chat.id,
        "Используйте кнопки меню 👇",
        reply_markup=get_main_menu()
    )

if __name__ == "__main__":
    print("🤖 Softy Bot запущен...")
    bot.infinity_polling()
