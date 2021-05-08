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

