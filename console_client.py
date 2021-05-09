from replies import *
from backend import *

try:
    db.connect()
    Enrolled.create_table()
    Pass.create_table()
    Registered.create_table()
except InternalError as px:
    print(str(px))


def how_to_get():
    print('-------------------------------------------')
    print("Координаты общежития: 55.788641, 37.791508")
    print('-------------------------------------------')


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

    print(text)


def back_to_start(message):
    if update_status(message.from_user.id, 'stage_1') != 0:
        add_user(message.from_user.id)
    print(reply_stage_0)
    print()
    print('> 1. Регистрация в общежитие')
    print('> 2. Как добраться?')


def action_by_stage(stage, message):
    if stage == "stage_1":
        print()
        print(reply_stage_1)
        print(reply_stage_10)
        print(reply_stage_11)
        print(reply_stage_12)
        print()
        update_status(message.from_user.id, 'stage_reg_0')
    elif stage == "stage_reg_0":
        rc = check_user_enroll(message)
        if rc == 0:
            print()
            print(reply_stage_reg_0)
            print()
            update_status(message.from_user.id, 'stage_reg_1')
        elif rc == -2:
            print()
            print(reply_stage_reg_00)
            print(reply_stage_11)
            print(reply_stage_12)
            print()
        elif rc == -1:
            print()
            print(reply_stage_reg_01)
            print()
            back_to_start(message)
    elif stage == "stage_reg_1":
        rc = add_series(message)
        if rc == 0:
            print()
            print(reply_stage_reg_1)
            print()
            update_status(message.from_user.id, 'stage_reg_2')
    elif stage == "stage_reg_2":
        rc = add_number(message)
        if rc == 0:
            print()
            print(reply_stage_reg_2)
            print()
            update_status(message.from_user.id, 'stage_reg_3')
    elif stage == "stage_reg_3":
        rc = add_issued_by(message)
        if rc == 0:
            print()
            print(reply_stage_reg_3)
            print()
            update_status(message.from_user.id, 'stage_reg_4')
    elif stage == "stage_reg_4":
        rc = add_date_of_issue(message)
        if rc == 0:
            print()
            print(reply_stage_reg_4)
            print()
            update_status(message.from_user.id, 'stage_reg_5')
    elif stage == "stage_reg_5":
        rc = add_place_of_registration(message)
        if rc == 0:
            print()
            print(reply_stage_reg_5)
            send_user_info(message)
            print(reply_stage_reg_50)
            print()
            print('> 1. Да')
            print('> 2. Нет')
            print()
            update_status(message.from_user.id, 'stage_reg_6')
    elif stage == "stage_reg_6":
        if message.text == 'Да':
            print()
            print(reply_stage_reg_6)
            print('> 1. Регистрация в общежитие')
            print('> 2. Как добраться?')
            print()
            update_registered_data_id(message)
            update_status(message.from_user.id, 'stage_reg_fin')
        elif message.text == 'Нет':
            print()
            print(reply_stage_reg_60)
            print(reply_stage_reg_0)
            print()


            update_status(message.from_user.id, 'stage_reg_1')
        else:
            print()
            print(reply_incorrect_input)
            print(reply_stage_reg_5)
            print()
            print('> 1. Да')
            print('> 2. Нет')
            print()

    elif stage == "stage_reg_fin":
        print()
        print(reply_stage_fin)
        print()
        print('> 1. Регистрация в общежитие')
        print('> 2. Как добраться?')
        print()


user_id = 88127631


class UserInfo(object):
    def __init__(self, id):
        self.id = id


class Message(object):
    def __init__(self, text, id):
        self.text = text
        self.from_user = UserInfo(id)


back_to_start(Message('start', user_id))


while True:

    print()
    text = input('Введите сообщение: ')
    message = Message(text, user_id)

    if text == 'Как добраться?':
        how_to_get()
    else:
        stage = get_status(message.from_user.id)
        action_by_stage(stage, message)
