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
    student_group = CharField()
    qualification = CharField()

    hiring_num = CharField()
    hiring_date = CharField()
    faculty = CharField()

    room_num = CharField(null=True)

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


try:
    db.connect()
    Enrolled.create_table()
    Pass.create_table()
    Registered.create_table()
except InternalError as px:
    print(str(px))


