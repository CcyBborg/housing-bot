from replies import *
from backend import *

try:
    db.connect()
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
    pass


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
