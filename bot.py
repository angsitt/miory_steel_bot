import telebot
from utils import *
from telebot import types
from config import TOKEN
from db_connection import add_user_contacts, view_user_contacts

bot = telebot.TeleBot(TOKEN)
surname = ''
name = ''
middle_name = ''
email = ''

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, GREETING_MSG.format(message.from_user))
    menu(message)

@bot.message_handler(commands=['menu'])
def menu(message):
    menu_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    company_info_btn = types.KeyboardButton(text="Информация о компании")
    items_btn = types.KeyboardButton(text="Продукция")
    partners_btn = types.KeyboardButton(text="Наши партнеры")
    contacts_btn = types.KeyboardButton(text="Контакты")
    connect_btn = types.KeyboardButton(text="Связаться с менеджером")
    menu_markup.add(company_info_btn, items_btn, partners_btn, contacts_btn, connect_btn)
    bot.send_message(message.from_user.id,
                     'Пожалуйста, чтобы получить необходимую информацию, выберите запрос ⬇:',
                     reply_markup=menu_markup)

@bot.message_handler(func=lambda msg: 'Меню' == msg.text, content_types=['text'])
def turn_to_menu(message):
    menu(message)

@bot.message_handler(func=lambda msg: msg.text == 'Информация о компании', content_types=['text'])
def company_info(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, COMPANY_INFO_MSG, reply_markup=user_markup)
    bot.send_photo(message.chat.id, 'https://www.google.com/imgres?imgurl=https%3A%2F%2Fmiory.vitebsk-region.gov.by%2Fuploads%2Fimages%2F26-02-2020-04.png&imgrefurl=https%3A%2F%2Fmiory.vitebsk-region.gov.by%2Fru%2Fpromyshlennost%2F&tbnid=k1BuW_-0MqwxEM&vet=12ahUKEwi-wZXWl9X2AhWK2uAKHd3ECbsQMygPegUIARCrAQ..i&docid=yJYVwVvOssI1WM&w=304&h=134&q=miory%20steel&hl=en&ved=2ahUKEwi-wZXWl9X2AhWK2uAKHd3ECbsQMygPegUIARCrAQ')

@bot.message_handler(func=lambda msg: msg.text == 'Продукция', content_types=['text'])
def items_info(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, ITEMS_MSG, reply_markup=user_markup)

@bot.message_handler(func=lambda msg: msg.text == 'Наши партнеры', content_types=['text'])
def partners_info(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, PARTNERS_MSG, reply_markup=user_markup)

@bot.message_handler(func=lambda msg: msg.text == 'Контакты', content_types=['text'])
def contacts(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, CONTACTS_MSG, reply_markup=user_markup)

@bot.message_handler(func=lambda msg: msg.text == 'Связаться с менеджером', content_types=['text'])
def connect(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row('Меню')
    bot.send_message(message.from_user.id, CONNECT_MSG + 'Введите фамилию:', reply_markup=user_markup)
    bot.register_next_step_handler(message, get_surname)

def get_surname(message):
    global surname
    surname = message.text
    if name_validation(surname):
        bot.send_message(message.from_user.id, 'Введите имя:')
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод! Чтобы продолжить нажмите "Меню"')

def get_name(message):
    global name
    name = message.text
    if name_validation(name):
        bot.send_message(message.from_user.id, 'Введите отчество:')
        bot.register_next_step_handler(message, get_middle_name)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод! Чтобы продолжить нажмите "Меню"')

def get_middle_name(message):
    global middle_name
    middle_name = message.text
    bot.send_message(message.from_user.id, 'Введите адрес электронной почты:')
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    global email
    email = message.text
    if email_validation(email):
        keyboard = types.InlineKeyboardMarkup()
        key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
        keyboard.add(key_yes)
        key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
        keyboard.add(key_no)
        bot.send_message(message.from_user.id,
                         VERIFICATION_MSG.format(surname, name, middle_name, email),
                         reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ввод! Чтобы продолжить нажмите "Меню"')

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        response = add_user_contacts(user_surname=surname, user_name=name, user_middle_name=middle_name, user_email=email)
        if response == True:
            bot.send_message(call.message.chat.id, 'Ваши контакты успешно сохранены, наш менеджер свяжется с Вами в рабочее время.')
            view_user_contacts()
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Чтобы продолжить нажмите "Меню"')

if __name__ == '__main__':
    bot.polling(none_stop=True)