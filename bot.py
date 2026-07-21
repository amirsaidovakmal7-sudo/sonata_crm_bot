import telebot
from telebot.types import ReplyKeyboardRemove

from buttons import button_language, contact_button
from database.user_service import *
import time
from buttons import *
from config import TOKEN
from database import Base, engine
from init_amo import add_complex_lead

group_id = -1003798480119

Base.metadata.create_all(engine)

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_language = get_user_language_bd(user_id)
    if user_language:
        if user_language == '🇷🇺 Русский':
            bot.send_message(user_id, 'Здравствуйте, рады видеть вас снова!')
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'Для того что бы связаться с вами, отправьте свой контакт по кнопке:',
                             reply_markup=contact_button())
            bot.register_next_step_handler(message, get_user_number, user_language)
        else:
            bot.send_message(user_id, 'Salom, sizni yana ko‘rganimizdan xursandmiz!')
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'Siz bilan bog‘lanishimiz uchun, iltimos, quyidagi tugma yordamida aloqa ma’lumotlaringizni taqdim eting:',
                             reply_markup=contact_button_uzb())
            bot.register_next_step_handler(message, get_user_number, user_language)
    elif not user_language:
        bot.send_message(user_id, 'Выберите язык:', reply_markup=button_language())
        bot.register_next_step_handler(message, get_user_language)



def get_user_language(message):
    user_id = message.from_user.id
    user_language = message.text
    if user_language == '🇷🇺 Русский' or user_language == "🇺🇿 O'zbekcha":
        if user_language == '🇷🇺 Русский':
            create_user(user_id, user_language)
            bot.send_message(user_id, 'Спасибо! Для того что бы связаться с вами, отправьте свой контакт по кнопке:',
                             reply_markup=contact_button())
            bot.register_next_step_handler(message, get_user_number, user_language)
        else:
            create_user(user_id, user_language)
            bot.send_message(user_id, 'Rahmat! Siz bilan bog‘lanishimiz uchun, iltimos, quyidagi tugma yordamida aloqa ma’lumotlaringizni yuboring:',
                             reply_markup=contact_button_uzb())
            bot.register_next_step_handler(message, get_user_number, user_language)
    else:
        bot.send_message(user_id, 'Неверные данные! Выберите по кнопке')
        bot.send_message(user_id, 'Noto‘g‘ri ma’lumot! Iltimos, tugma yordamida tanlovni amalga oshiring.')
        bot.register_next_step_handler(message, get_user_language)










def get_user_number(message, user_language):
    user_id = message.from_user.id
    if message.contact:
        user_number = message.contact.phone_number
        if user_language == '🇷🇺 Русский':
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'Выберите интересующее вас направление',
                             reply_markup=direct_button())
            bot.register_next_step_handler(message, get_user_direction, user_language, user_number)
        else:
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'O‘zingizni qiziqtirgan sohani tanlang.',
                             reply_markup=direct_button_uzb())
            bot.register_next_step_handler(message, get_user_direction, user_language, user_number)
    else:
        if user_language == '🇷🇺 Русский':
            bot.send_message(user_id, 'Неверные данные! Отправьте по кнопке')
            bot.register_next_step_handler(message, get_user_number, user_language)
        else:
            bot.send_message(user_id, 'Noto‘g‘ri ma’lumot! Tugma yordamida yuboring.')
            bot.register_next_step_handler(message, get_user_number, user_language)



def get_user_direction(message, user_language, user_number):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_nick = message.from_user.username
    if user_language == '🇷🇺 Русский':
        if message.text == '🎸 Гитара' or message.text == '🎹 Фортепиано' or message.text == '🥁 Барабаны' or message.text == '🎻 Скрипка' or message.text == '🎤 Вокал':
            user_direction = message.text
            text = (f'Новая заявка! (от бота) \n\n'
                    f'Имя клиента: {user_name}\n'
                    f'Юзер нейм в тг: @{user_nick}\n'
                    f'Тг айди: {user_id}\n'
                    f'Выбранный язык: {user_language}\n'
                    f'Направление: {user_direction}\n'
                    f'Номер телефона: {user_number}\n')
            bot.send_message(group_id, text)
            add_complex_lead(user_name, user_number, user_nick, user_id, user_language, user_direction)
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'Спасибо! Заявка принята, в ближайшее время с вами свяжется наш менеджер!',
                         reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(user_id, 'Неверный данные! Отправьет по кнопке')
            bot.register_next_step_handler(message, get_user_direction, user_language, user_number)
    else:
        if message.text == '🎸 Gitara' or message.text == '🎹 Fortepiano' or message.text == '🥁 Baraban' or message.text == '🎻 Skripka' or message.text == '🎤 Vokal':
            user_direction = message.text
            text = (f'Новая заявка! (от бота) \n\n'
                    f'Имя клиента: {user_name}\n'
                    f'Юзер нейм в тг: @{user_nick}\n'
                    f'Тг айди: {user_id}\n'
                    f'Выбранный язык: {user_language}\n'
                    f'Направление: {user_direction}\n'
                    f'Номер телефона: {user_number}\n')
            bot.send_message(group_id, text)
            add_complex_lead(user_name, user_number, user_nick, user_id, user_language, user_direction)
            bot.send_chat_action(user_id, 'typing')
            time.sleep(1)
            bot.send_message(user_id, 'Rahmat! So‘rovingiz qabul qilindi va menejerimiz tez orada siz bilan bog‘lanadi.',
                             reply_markup=ReplyKeyboardRemove())
        else:
            bot.send_message(user_id, 'Noto‘g‘ri ma’lumot! Tugma yordamida yuboring.')
            bot.register_next_step_handler(message, get_user_direction, user_language, user_number)






bot.polling(non_stop=True)

