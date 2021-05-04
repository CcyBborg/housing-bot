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
