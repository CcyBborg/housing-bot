

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
