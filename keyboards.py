import telebot


def keyboard_reg_main():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Вернуться в главное меню')
    return keyboard


def keyboard_stage_0():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Регистрация в общежитие')
    keyboard.row('Как добраться?')
    return keyboard


def keyboard_stage_5():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Да', 'Нет')
    return keyboard


def keyboard_service_0():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('Выслать идентификационный ключ')
    keyboard.row('Статистика по зарегистрировавшимся')
    keyboard.row('Статистика по заселённым')
    return keyboard


def inline_keyboard_for_template():
    keyboard = telebot.types.InlineKeyboardMarkup()
    button0 = telebot.types.InlineKeyboardButton(text='подтвердить',
                                                 callback_data='approved')
    button1 = telebot.types.InlineKeyboardButton(text='отклонить',
                                                 callback_data='rejected')
    keyboard.add(button0)
    keyboard.add(button1)
    return keyboard
