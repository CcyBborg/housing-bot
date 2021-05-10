from peewee import *

db = SqliteDatabase('./CAMPUS.db', pragmas={
    'journal_mode': 'wal',
    'cache_size': -1024 * 64})


class Enrolled(Model):
    id = PrimaryKeyField(unique=True, null=False)
    name = CharField()
    surname = CharField()
    patronymic = CharField()
    student_card = CharField()

    class Meta:
        db_table = 'enrolled_stats'
        database = db


class Pass(Model):
    id = PrimaryKeyField(unique=True, null=False)
    series = CharField()
    number = CharField()
    date_of_issue = CharField()
    issued_by = CharField()
    place_of_registration = CharField()

    class Meta:
        db_table = 'pass_data'
        database = db


class Registered(Model):
    tg_id = PrimaryKeyField(null=False)
    enrolled_id = IntegerField()
    data_id = IntegerField()
    status = CharField()

    class Meta:
        db_table = 'registered'
        database = db


def add_user(tg_id):
    Registered.create(
        tg_id=tg_id,
        enrolled_id=-1,
        data_id=-1,
        status='stage_1'
    )
    return 0


def get_status(tg_id):
    query = (Registered.select())
    for user in query:
        if user.tg_id == tg_id:
            return user.status


def update_status(tg_id, status):
    query = (Registered.select())
    for user in query:
        if user.tg_id == tg_id:
            user.status = status
            user.save()
            return 0
    return -1


def get_settled_count():
    query = (Registered.select())
    count = 0
    for user in query:
        if user.status == 'stage_reg_set':
            count += 1
    return count


def get_reg_count():
    query = (Registered.select())
    count = 0
    for user in query:
        if user.status == 'stage_reg_fin':
            count += 1
    return count


def get_ident_key():
    with open("key.txt", "r") as file:
        return int(file.read().strip())


def check_admin_rights(message):
    return message.from_user.id == 221820979


def check_back_to_start(message):
    return message.text == "Вернуться в главное меню"


def update_registered_data_id(message):
    query = (Registered.select())
    for user in query:
        if user.tg_id == message.from_user.id:
            user.data_id = message.from_user.id
            user.save()


def update_enrolled_id(tg_id, enrolled_id):
    query = (Registered.select())
    for user in query:
        if user.tg_id == tg_id:
            user.enrolled_id = enrolled_id
            user.save()


def check_user_enroll(message):
    data = message.text.split(',')
    if len(data) != 2:
        return -2
    data = [i.strip() for i in data]
    query = (Enrolled.select())
    for user in query:
        if (str(user.surname)).lower() == data[0].lower() and (str(user.student_card)).lower() == data[1].lower():
            update_enrolled_id(message.from_user.id, user.id)
            return 0
    return -1


def add_series(message):
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            user.series = message.text
            user.save()
            return 0
    Pass.create(
        id=message.from_user.id,
        series=message.text,
        number=-1,
        date_of_issue='01 января 1990 года',
        issued_by='МВД РОССИИ',
        place_of_registration='Россия'
    )
    return 0


def add_number(message):
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            user.number = message.text
            user.save()
            return 0
    return -1


def add_date_of_issue(message):
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            user.date_of_issue = message.text
            user.save()
            return 0
    return -1


def add_issued_by(message):
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            user.issued_by = message.text
            user.save()
            return 0
    return -1


def add_place_of_registration(message):
    query = (Pass.select())
    for user in query:
        if user.id == message.from_user.id:
            user.place_of_registration = message.text
            user.save()
            return 0
    return -1


def check_for_key(message):
    query = (Registered.select())
    for user in query:
        if user.tg_id == message.from_user.id:
            if user.status == "stage_reg_fin":
                return True
    return False


def check_for_set(message):
    query = (Registered.select())
    for user in query:
        if user.tg_id == message.from_user.id:
            if user.status == "stage_reg_set":
                return True
    return False
