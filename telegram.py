
from replies import *
from keyboards import *
from backend import *


try:
    db.connect()
    Enrolled.create_table()
    Pass.create_table()
    Registered.create_table()
except InternalError as px:
    print(str(px))


token = ""

bot = telebot.TeleBot(token)


def action_by_stage(stage, message):
    if stage == "stage_1":
        bot.send_message(message.chat.id, reply_stage_1, reply_markup=keyboard_reg_main(), parse_mode="Markdown")
        bot.send_message(message.chat.id, reply_stage_10, parse_mode="Markdown")
        bot.send_message(message.chat.id, reply_stage_11, parse_mode="Markdown")
        bot.send_message(message.chat.id, reply_stage_12, parse_mode="Markdown")
        update_status(message.from_user.id, 'stage_reg_0')
    elif stage == "stage_reg_0":
        rc = check_user_enroll(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_0, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_1')
        elif rc == -2:
            bot.send_message(message.chat.id, reply_stage_reg_00, parse_mode="Markdown")
            bot.send_message(message.chat.id, reply_stage_11, parse_mode="Markdown")
            bot.send_message(message.chat.id, reply_stage_12, parse_mode="Markdown")
        elif rc == -1:
            bot.send_message(message.chat.id, reply_stage_reg_01, parse_mode="Markdown")
            back_to_start(message)
    elif stage == "stage_reg_1":
        rc = add_series(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_1, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_2')
    elif stage == "stage_reg_2":
        rc = add_number(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_2, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_3')
    elif stage == "stage_reg_3":
        rc = add_issued_by(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_3, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_4')
    elif stage == "stage_reg_4":
        rc = add_date_of_issue(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_4, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_5')
    elif stage == "stage_reg_5":
        rc = add_place_of_registration(message)
        if rc == 0:
            bot.send_message(message.chat.id, reply_stage_reg_5, parse_mode="Markdown")
            send_user_info(message)
            bot.send_message(message.chat.id, reply_stage_reg_50, reply_markup=keyboard_stage_5(),
                             parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_6')
    elif stage == "stage_reg_6":
        if message.text == 'Да':
            bot.send_message(message.chat.id, reply_stage_reg_6, reply_markup=keyboard_stage_0(), parse_mode="Markdown")
            update_registered_data_id(message)
            update_status(message.from_user.id, 'stage_reg_fin')
        elif message.text == 'Нет':
            bot.send_message(message.chat.id, reply_stage_reg_60, reply_markup=keyboard_stage_0(),
                             parse_mode="Markdown")
            bot.send_message(message.chat.id, reply_stage_reg_0, parse_mode="Markdown")
            update_status(message.from_user.id, 'stage_reg_1')
        else:
            bot.send_message(message.chat.id, reply_incorrect_input, reply_markup=keyboard_stage_5(),
                             parse_mode="Markdown")
            bot.send_message(message.chat.id, reply_stage_reg_5, reply_markup=keyboard_stage_5(), parse_mode="Markdown")
    elif stage == "stage_reg_fin":
        bot.send_message(message.chat.id, reply_stage_fin, reply_markup=keyboard_stage_0(), parse_mode="Markdown")


def back_to_start(message):
    if update_status(message.from_user.id, 'stage_1') != 0:
        add_user(message.from_user.id)
    bot.send_message(message.chat.id, reply_stage_0, reply_markup=keyboard_stage_0(), parse_mode="Markdown")


def check_how_to_get(message):
    return message.text == "Как добраться?"


def how_to_get(message):
    bot.send_message(message.chat.id, reply_how_to_get, reply_markup=keyboard_stage_0(), parse_mode="Markdown")
    bot.send_location(message.chat.id, 55.788641, 37.791508)


def send_user_info(message):
    series = ''
    number = ''
    issued = ''
    date = ''
    reg_place = ''
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            series = user.series
            number = user.number
            issued = user.issued_by
            date = user.date_of_issue
            reg_place = user.place_of_registration

    text = f'*Серия: {series}\n' \
           f'Номер: {number}\n' \
           f'Выдан: {issued}\n' \
           f'Дата выдачи: {date}\n' \
           f'Место регистрации: {reg_place}*'

    bot.send_message(message.chat.id, text, parse_mode="Markdown")


def send_agreement(message):
    series = ''
    number = ''
    issued = ''
    date = ''
    reg_place = ''
    name = ''
    surname = ''
    patronymic = ''
    query = (Registered.select())
    for user in query:
        if user.tg_id == message.from_user.id:
            pass_query = (Pass.select())
            for p_user in pass_query:
                if user.data_id == p_user.id:
                    series = p_user.series
                    number = p_user.number
                    issued = p_user.issued_by
                    date = p_user.date_of_issue
                    reg_place = p_user.place_of_registration
                    break
            enrolled_query = (Enrolled.select())
            for e_user in enrolled_query:
                if user.enrolled_id == e_user.id:
                    name = e_user.name
                    surname = e_user.surname
                    patronymic = e_user.patronymic

    with open(f"{surname}_{message.from_user.id}.txt", "w") as file:
        file.write(contract_template.format(name, patronymic, surname, series, number, issued, date, reg_place))

    with open(f"{surname}_{message.from_user.id}.txt", "rb") as file:
        bot.send_document(221820979, file, reply_markup=inline_keyboard_for_template(), parse_mode="Markdown")


def get_tg_id_from_file_name(file_name):
    return (file_name.split('.')[0]).split('_')[1]


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    tg_id = int(get_tg_id_from_file_name(call.message.document.file_name))
    if call.data == 'approved':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(tg_id, reply_stage_set, parse_mode="Markdown")
        update_status(tg_id, 'stage_reg_set')
    elif call.data == "rejected":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(tg_id, reply_rejected, reply_markup=keyboard_stage_0(), parse_mode="Markdown")
        (update_status(tg_id, 'stage_1'))


@bot.message_handler(func=check_admin_rights, commands=['admin'])
def handle_start(message):
    bot.send_message(message.chat.id, reply_service_0, reply_markup=keyboard_service_0(), parse_mode="Markdown")


@bot.message_handler(func=check_admin_rights, content_types=['text'])
def handle_text(message):
    if message.text == 'Выслать идентификационный ключ':
        bot.send_message(message.chat.id, f'*{get_ident_key()}*', reply_markup=keyboard_service_0(),
                         parse_mode="Markdown")
    elif message.text == 'Статистика по зарегистрировавшимся':
        bot.send_message(message.chat.id, f'Количество зарегистрировашихся:\n'
                                          f'*{get_reg_count()}*', reply_markup=keyboard_service_0(),
                         parse_mode="Markdown")
    elif message.text == 'Статистика по заселённым':
        bot.send_message(message.chat.id, f'Количество заселённых:\n'
                                          f'*{get_settled_count()}*', reply_markup=keyboard_service_0(),
                         parse_mode="Markdown")
    else:
        bot.send_message(message.chat.id, f'Неверная команда\n', reply_markup=keyboard_service_0(),
                         parse_mode="Markdown")


@bot.message_handler(func=check_how_to_get, content_types=['text'])
def handle_text(message):
    how_to_get(message)


@bot.message_handler(func=check_for_set, content_types=['text'])
def handle_text(message):
    bot.send_message(message.from_user.id, reply_stage_set, parse_mode="Markdown")


@bot.message_handler(commands=['start'])
def handle_start(message):
    back_to_start(message)


@bot.message_handler(func=check_back_to_start, content_types=['text'])
def handle_text(message):
    back_to_start(message)


@bot.message_handler(func=check_for_key)
def handle_text(message):
    if message.text.isdigit():
        if int(message.text) == get_ident_key():
            send_agreement(message)
            bot.send_message(message.chat.id, "Договор успешно сформирован.", reply_markup=keyboard_stage_0(),
                             parse_mode="Markdown")
            return 0
    bot.send_message(message.chat.id, reply_stage_fin, reply_markup=keyboard_stage_0(), parse_mode="Markdown")


@bot.message_handler(content_types=['text'])
def handle_text(message):
    stage = get_status(message.from_user.id)
    action_by_stage(stage, message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
