from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo
import db


menu = [
    [InlineKeyboardButton(text="👕 Каталог🚫",  callback_data="generate_image"),
    InlineKeyboardButton(text="🖼 Примерить🚫", callback_data="dress")],
    [InlineKeyboardButton(text="👤 Профиль✅", callback_data="profile"),
    InlineKeyboardButton(text="💰 Баланс🚫", callback_data="balance")],
    [InlineKeyboardButton(text="⚙️ Настройки✅", callback_data="settings"),
    InlineKeyboardButton(text="🖼 Галерея🚫", callback_data="gallary")],
    [InlineKeyboardButton(text="🔎 Помощь✅", callback_data="help"),
    InlineKeyboardButton(text="🛠 Тех.Поддержка✅", callback_data="tech_helper")],
    [InlineKeyboardButton(text="💳 Купить примерки🚫", callback_data="buy_tokens")],
    [InlineKeyboardButton(text="🎁 Бесплатые примерки🚫", callback_data="free_tokens")]
]



admin_tech_id = 967026526
tech = [
    [InlineKeyboardButton(text="📩 Написать в поддержку✅", url=f"tg://user?id={admin_tech_id}")],
    [InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]
]






profile = [
    [InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu"),
     InlineKeyboardButton(text="✏️ Изменить данные✅", callback_data="menu")]
]





profkb1 = [
    [InlineKeyboardButton(text="Создать профиль✅", callback_data="profile_h1"),
     InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]
]




profkb2 = [
    [InlineKeyboardButton(text="Изменить профиль✅", callback_data="profile_h1"),
     InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]
]



dress_new = [
    [InlineKeyboardButton(text="📸 Добавить фото✅", callback_data="add_photo"),
     InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]
]

dress_last = [
    [InlineKeyboardButton(text="⏩ Продолжить✅", callback_data="add_clothes"),
     InlineKeyboardButton(text="📸 Изменить фото✅", callback_data="add_photo")],
    [InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]
]

clothes_photo = [
    [InlineKeyboardButton(text="Добавить одежду из каталога 🚫", callback_data="add_photo_from_webapp")],
    [InlineKeyboardButton(text="Добавить свою одежду✅", callback_data="add_photo_from_person")]
]




iexit_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]])

to_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Меню✅", callback_data="menu")]])

iexit_kb1 = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="👁‍ Скрыть✅", callback_data="menu_1")]])

convert = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Запустить примерку 🧬", callback_data="convert_AI")]])


cph = InlineKeyboardMarkup(inline_keyboard=clothes_photo)
dn = InlineKeyboardMarkup(inline_keyboard=dress_new)
dl = InlineKeyboardMarkup(inline_keyboard=dress_last)
menu = InlineKeyboardMarkup(inline_keyboard=menu)
btn_tech = InlineKeyboardMarkup(inline_keyboard=tech)
profile = InlineKeyboardMarkup(inline_keyboard=profile)
profile_add = InlineKeyboardMarkup(inline_keyboard=profkb1)
profile_edit = InlineKeyboardMarkup(inline_keyboard=profkb2)







def settings_d(user_id):
    with db.connection.cursor() as cursor: #db - ваше подключение к БД
        cursor.execute("SELECT notifications_enabled FROM users_settings WHERE id = %s", (user_id))
        result = cursor.fetchone()
        if result['notifications_enabled'] == 0:
            notifications_enabled = True
        else:
            notifications_enabled = False

    if notifications_enabled == True:
        emoji = "🔔"
    else:
        emoji = "🔕"
    text = f"{emoji} Уведомления"

    settings_k = [
        [InlineKeyboardButton(text=text, callback_data="mute"),
         InlineKeyboardButton(text="❇️ Отзывы🚫", callback_data="tech_helper")],
        [InlineKeyboardButton(text="◀️ Выйти в меню✅", callback_data="menu")]

    ]
    return InlineKeyboardMarkup(inline_keyboard=settings_k)
# web_app=WebAppInfo('https://<your_domain>')