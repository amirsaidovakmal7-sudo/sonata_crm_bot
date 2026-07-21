from telebot import types



def button_language():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    rus = types.KeyboardButton('🇷🇺 Русский')
    uzb = types.KeyboardButton("🇺🇿 O'zbekcha")
    kb.add(rus, uzb)
    return kb


def contact_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone = types.KeyboardButton('Поделиться контактом ☎️', request_contact=True)
    kb.add(phone)
    return kb

def contact_button_uzb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    phone = types.KeyboardButton('Kontaktni ulashish ☎️', request_contact=True)
    kb.add(phone)
    return kb


def direct_button():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    guitar = types.KeyboardButton('🎸 Гитара')
    piano = types.KeyboardButton('🎹 Фортепиано')
    baraban = types.KeyboardButton('🥁 Барабаны')
    vokal = types.KeyboardButton('🎤 Вокал')
    skripka = types.KeyboardButton('🎻 Скрипка')
    kb.add(guitar, piano, baraban, vokal, skripka)
    return kb

def direct_button_uzb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    guitar = types.KeyboardButton('🎸 Gitara')
    piano = types.KeyboardButton('🎹 Fortepiano')
    baraban = types.KeyboardButton('🥁 Baraban')
    vokal = types.KeyboardButton('🎤 Vokal')
    skripka = types.KeyboardButton('🎻 Skripka')
    kb.add(guitar, piano, baraban, vokal, skripka)
    return kb

