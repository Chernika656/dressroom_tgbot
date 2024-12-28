import asyncio
import json
from pyexpat.errors import messages

from aiogram import F, Router, types
from aiogram.client import bot
from aiogram.filters import Command


from aiogram.types import Message, WebAppInfo, FSInputFile, URLInputFile, BufferedInputFile, InputMediaPhoto, InputMedia
from aiogram import flags
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
import asyncpg
from aiogram.utils import CallbackData
from django.db.backends import mysql
from pymysql import IntegrityError




import kb
import text
import db
import admin
import states
import img


router = Router()

# СТАРТ
@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(text.greet.format(name=msg.from_user.full_name), reply_markup=kb.to_menu)
    with db.connection.cursor() as cursor:
        cursor.execute(f"INSERT IGNORE INTO profile (id) VALUES ({msg.from_user.id})")
        cursor.execute(f"INSERT IGNORE INTO users_settings (id) VALUES ({msg.from_user.id})")
        cursor.execute(f"INSERT IGNORE INTO photo_user (id) VALUES ({msg.from_user.id})")
        db.connection.commit()



# МЕНЮ
@router.callback_query(F.data == "menu")
async def menu2(clbck: CallbackQuery, state: FSMContext):
    global msg_m
    media = InputMediaPhoto(media=img.menu)
    await clbck.message.edit_media(media=media)
    await clbck.message.edit_reply_markup(reply_markup=kb.menu)







# ТЕХ ПОДДЕРЖКА
@router.callback_query(F.data == "tech_helper")
async def tech_help(clbck: CallbackQuery, state: FSMContext):
    media = InputMediaPhoto(media=img.techi, caption=text.tech)
    await clbck.message.edit_media(media=media)
    await clbck.message.edit_reply_markup(reply_markup=kb.btn_tech)






# ПРОФИЛЬ
@router.callback_query(F.data == "profile")
async def profile_first(clbck: CallbackQuery, state: FSMContext):
    with db.connection.cursor() as cursor:
        cursor.execute(f"SELECT height, weight, shoe_size, 1 FROM profile WHERE id = {clbck.from_user.id}")
        result = cursor.fetchone()
        if result and result['height']:
            prof = f'{clbck.from_user.full_name}, твой профиль.⬇️\n\n ID:{clbck.from_user.id}\n\n Рост: {result['height']} см.\n Вес: {result['weight']} кг.\n Размер обуви: {result['shoe_size']}'
            media = InputMediaPhoto(media=img.profi, caption=prof)
            await clbck.message.edit_media(media=media)
            await clbck.message.edit_reply_markup(reply_markup=kb.profile_edit)
        else:
            media1 = InputMediaPhoto(media=img.profi, caption=text.text_profile)
            await clbck.message.edit_media(media=media1)
            await clbck.message.edit_reply_markup(reply_markup=kb.profile_add)






# ЗАПОЛНИТЬ АНКЕТУ
@router.callback_query(F.data == "profile_h1")
async def profile_1(clbck: CallbackQuery, state: FSMContext):
    global msg
    media1 = InputMediaPhoto(media=img.profi, caption=text.profile_text1)
    msg = await clbck.message.edit_media(media=media1)
    await state.update_data(msg_id1=msg.message_id)
    await state.set_state(states.ProfileStates.height)


# РОСТ
@router.message(states.ProfileStates.height)
async def process_height(msg: types.Message, state: FSMContext):
    global msg2
    height = msg.text
    await state.update_data(height=height)
    msg2 = await msg.answer(text.profile_text2)
    await state.update_data(msg_id2=msg2.message_id)
    await state.set_state(states.ProfileStates.weight)
    await msg.delete()


# ВЕС
@router.message(states.ProfileStates.weight)
async def process_weight(message: types.Message, state: FSMContext):
    global msg3
    weight = message.text
    await state.update_data(weight=weight)
    msg3 = await message.answer(text.profile_text3)
    await state.update_data(msg_id3=msg3.message_id)
    await state.set_state(states.ProfileStates.shoesize)
    await message.delete()


# РАЗМЕР
@router.message(states.ProfileStates.shoesize)
async def process_shoesize(message: types.Message, state: FSMContext):
    global msg
    global msg2
    global msg3
    shoesize = message.text
    await state.update_data(shoesize=shoesize)
    data = await state.get_data()
    await message.delete()
    try:
        with db.connection.cursor() as cursor:
            try:
                cursor.execute("INSERT INTO profile (id, height, weight, shoe_size) VALUES (%s, %s, %s, %s)",
                               (message.from_user.id, data['height'], data['weight'], shoesize))
            except IntegrityError as e:
                cursor.execute("UPDATE profile SET height = %s, weight = %s, shoe_size = %s WHERE id = %s",
                               (data['height'], data['weight'], shoesize, message.from_user.id))
            db.connection.commit()
            await message.answer(f"✅ Данные сохранены:\nРост: {data['height']}\nВес: {data['weight']}\nРазмер обуви: {shoesize}", reply_markup=kb.iexit_kb)

            await msg.delete()
            await msg2.delete()
            await msg3.delete()

            await state.clear()
    except asyncpg.exceptions.PostgresError as e:
        print(f"Ошибка при сохранении данных в базу данных: {e}")
        await state.clear()
        return False
    return True





# АДМИН-КЛЮЧ
@router.message(Command("hg7hf8h8y2rb2", prefix="$"))
async def admin_id(msg: Message):
    admin_id1 = msg.from_user.id
    admin.ADMINS.append(admin_id1)
    await msg.answer(text.admin_text(name=msg.from_user.full_name))
    await msg.delete()




#НАСТРОЙКИ
@router.callback_query(F.data == "settings")
async def setting(clbck: CallbackQuery, state: FSMContext):
    media1 = InputMediaPhoto(media=img.settingsi)
    await clbck.message.edit_media(media=media1)
    await clbck.message.edit_reply_markup(reply_markup=kb.settings_d(clbck.from_user.id))

#УВЕДОМЛЕНИЯ
@router.callback_query(F.data == "mute")
async def mute(clbck: CallbackQuery, state: FSMContext):
    user_id = clbck.from_user.id
    # Получаем текущее состояние уведомлений из базы данных
    with db.connection.cursor() as cursor: #db - ваше подключение к БД
        cursor.execute("SELECT notifications_enabled FROM users_settings WHERE id = %s", (user_id,))
        result = cursor.fetchone()
        if result['notifications_enabled'] == 0:
            notifications_enabled = 1
        else:
            notifications_enabled = 0

    # Обновляем состояние в базе данных
    with db.connection.cursor() as cursor:
        cursor.execute("UPDATE users_settings SET notifications_enabled = %s WHERE id = %s", (notifications_enabled, user_id))
        db.connection.commit()

    await  update_mute_button(clbck, notifications_enabled)



async def update_mute_button(clbck: CallbackQuery, notifications_enabled: int):
    if notifications_enabled == 0:
        emoji = "🔔"
    else:
        emoji = "🔕"
    text = f"{emoji} Уведомления"
    markup = kb.settings_d(clbck.from_user.id) # Передаем ID пользователя для обновления
    await clbck.message.edit_reply_markup(reply_markup=markup)



#ПОМОЩЬ
@router.callback_query(F.data == "help")
async def help_1(clbck: CallbackQuery, state: FSMContext):
    media = InputMediaPhoto(media="https://i.pinimg.com/originals/2d/92/fd/2d92fda1d751ba2a8a4b49e739424958.jpg", caption=text.helper)
    await clbck.message.edit_media(media=media)
    await clbck.message.edit_reply_markup(reply_markup=kb.iexit_kb)





@router.callback_query(F.data == "dress")
async def dress(clbck: CallbackQuery, state: FSMContext):
    global msg_m
    msg_m = 0
    with db.connection.cursor() as cursor:
        cursor.execute(f"SELECT user_photo FROM photo_user WHERE id = {clbck.from_user.id}")
        result = cursor.fetchone()
    if result['user_photo'] == '0':
        media = InputMediaPhoto(media="https://i.pinimg.com/originals/2d/92/fd/2d92fda1d751ba2a8a4b49e739424958.jpg", caption=text.dress_new_text)
        msg_m = await clbck.message.edit_media(media=media)
        await clbck.message.edit_reply_markup(reply_markup=kb.dn)
    else:
        media = InputMediaPhoto(media=result['user_photo'], caption=text.dress_text)
        msg_m = await clbck.message.edit_media(media=media)
        await clbck.message.edit_reply_markup(reply_markup=kb.dl)



@router.callback_query(lambda c: c.data == 'add_photo')
async def process_callback_add_photo(query: types.CallbackQuery, state: FSMContext):
    global msg_m
    await query.answer(text.edit_foto)
    await state.set_state(states.Form.wait_for_photo)
    await msg_m.delete()






@router.message(F.photo, states.Form.wait_for_photo)
async def process_photo_change(message: types.Message, state: FSMContext):
    global msg_m
    if message.photo:
        photo = message.photo[-1]
        file_id = photo.file_id
        await state.update_data(key_img=file_id)
        with db.connection.cursor() as cursor:
            cursor.execute("UPDATE photo_user SET user_photo = %s WHERE id = %s", (file_id, message.from_user.id))
            db.connection.commit()
        await state.clear() #Сбрасываем состояние после успешного изменения


        await asyncio.sleep(3)
        await message.delete()
        msg_m = await message.answer_photo(photo=file_id, caption=text.dress_true, reply_markup=kb.dl)
    else:
        msg5 = await message.reply("Это не фото, попробуйте ещё раз")
        await asyncio.sleep(3)
        await msg5.delete()
        await message.delete()



@router.callback_query(F.data == "add_clothes")
async def add_clothes_photo(clbck: CallbackQuery, state: FSMContext):
    global msg_p
    media = InputMediaPhoto(media=img.profi)
    msg_p = await clbck.message.edit_media(media=media)
    await clbck.message.edit_reply_markup(reply_markup=kb.cph)



@router.callback_query(F.data == "add_photo_from_person")
async def clothes_from_user(clbck: CallbackQuery, state: FSMContext):
    global msg_p
    await clbck.answer(text.clothes_from_ur)
    await state.set_state(states.Form.wait_for_photo1) # Устанавливаем состояние ожидания фото
    await msg_p.delete()



@router.message(F.photo, states.Form.wait_for_photo1)
async def process_user_photo(message: types.Message, state: FSMContext):
    global  user_photo_file_id
    global existing_photo_file_id
    user_photo = message.photo[-1]
    user_photo_file_id = user_photo.file_id
    await message.delete()
    # try:
    with db.connection.cursor() as cursor:
        cursor.execute("SELECT user_photo FROM photo_user WHERE id = %s", (message.from_user.id,))
        result = cursor.fetchone()
        print(result)

    if result is None:
        await message.answer("Фотография пользователя не найдена в базе данных.")
        return

    existing_photo_file_id = result['user_photo']
    if not isinstance(existing_photo_file_id, str):
        await message.answer("Неверный формат данных в базе данных.")
        return


    await message.answer_media_group([
        InputMediaPhoto(media=existing_photo_file_id),
        InputMediaPhoto(media=user_photo_file_id)
    ])
    await message.answer("Альбом для примерки ⬆️", reply_markup=kb.convert) #kb.convert должен генерировать кнопки с callback_data
    await state.clear()


@router.callback_query(F.data == 'convert_AI')
async def convertation(clbck: CallbackQuery, state: FSMContext):
    global user_photo_file_id
    global existing_photo_file_id
    await clbck.answer() # Показывает пользователю, что запрос обработан
    try:
        user_photo_file = await download_file_from_telegram(bot, user_photo_file_id)
        existing_photo_file = await download_file_from_telegram(bot, existing_photo_file_id)

        print(user_photo_file)
        print(existing_photo_file)

    except Exception as e:
            await clbck.message.answer(f"Произошла неизвестная ошибка: {e}")




async def download_file_from_telegram(bot, file_id: str):
    file_info = await bot.get_file(file_id)
    file_url = file_info.file_path
    return await bot.download_file(file_url)
# file = await clbck.get_file(user_photo_file_id)
        # file_path = file.file_path
        # downloaded_file = await clbck.download_file(file_path)
        # filename = "converted_photo_user.jpg" #Или другое имя файла
        # with open(filename, 'wb') as f:
        #     f.write(downloaded_file.read())
        # file1 = await clbck.get_file(existing_photo_file_id)
        # file_path = file1.file_path
        # downloaded_file = await clbck.download_file(file_path)
        # filename = "converted_photo_from_user.jpg"  # Или другое имя файла
        # with open(filename, 'wb') as f2:
        #     f2.write(downloaded_file.read())
        # await clbck.message.answer_document(types.InputFile(filename))