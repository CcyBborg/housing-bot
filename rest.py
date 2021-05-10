import threading

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Schema, Field

from backend import check_user_enroll, add_series,\
    add_number, add_issued_by, add_date_of_issue, add_place_of_registration


temp_user_id = 0

class UserInfo(object):
    def __init__(self, id):
        self.id = id


class Message(object):
    def __init__(self, text, id):
        self.text = text
        self.from_user = UserInfo(id)


app = FastAPI(title="CampusAPI", version="0.1")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

lock = threading.RLock()


class StudentRegistrationPrompt(BaseModel):
    user_id: int = Field(0, title='user system identifier')
    pass_series: int = Field(0, title='pass_series')
    pass_num: int = Field(0, title='pass_num')
    pass_date_of_issue: str = Field(..., max_length=3000, title='pass date of issue')
    pass_issued_by: str = Field(..., max_length=3000, title='pass issued by')
    pass_place_of_registration: str = Field(..., max_length=3000, title='pass place of registration')


class StudentExistsPrompt(BaseModel):
    identifier: str = Field(..., max_length=3000, title='StudentID & Last Name')


class CompleteRegistration(BaseModel):
    token: int = Field(0, title='secret code')


def add_student_pass_to_db(user_id, pass_series, pass_num,
                         pass_date_of_issue, pass_issued_by,
                         pass_place_of_registration):

    message = Message(text=pass_series, id=user_id)
    rc = add_series(message)
    if rc != 0:
        return -1

    message = Message(text=pass_num, id=user_id)
    rc = add_number(message)
    if rc != 0:
        return -1

    message = Message(text=pass_date_of_issue, id=user_id)
    rc = add_date_of_issue(message)
    if rc != 0:
        return -1

    message = Message(text=pass_issued_by, id=user_id)
    rc = add_issued_by(message)
    if rc != 0:
        return -1

    message = Message(text=pass_place_of_registration, id=user_id)
    rc = add_place_of_registration(message)
    if rc != 0:
        return -1

    return 0


@app.post("/studentExists/")
def student_exists(prompt: StudentExistsPrompt):
    """
    Метод проверки студента в списках на заселение
    :param prompt:
    prompt.identifier — идентификатор на основе номера студенческого и фамилии студента
    """
    with lock:
        message = Message(text=prompt.identifier, id=temp_user_id)
        rc = check_user_enroll(message)

        if rc == 0:
            return {"status_code": 200, "message": 'Студент существует в списках на заселение'}

        elif rc == -1:
            return {"status_code": 400, "message": 'Неверно передан аргумент'}

        elif rc == -2:
            return {"status_code": 404, "message": 'Студент не найден'}


@app.post("/studentRegistration/")
def student_registration_req(prompt: StudentRegistrationPrompt):
    """
    Метод добавления студента в БД
    :param prompt:
    prompt.pass_series - серия паспорта
    prompt.pass_num — номер паспорта
    prompt.pass_date_of_issue — дата выдачи паспорта
    prompt.pass_issued_by – кем выдан паспорт
    prompt.pass_place_of_registration — место регистрации по паспорту
    """
    with lock:
        rc = add_student_pass_to_db(prompt.user_id, prompt.pass_series, prompt.pass_num,
                                  prompt.pass_date_of_issue, prompt.pass_issued_by,
                                  prompt.pass_place_of_registration)

        if rc == 0:
            return {"status_code": 200, "message": 'Студент успешно добавлен в БД'}

        else:
            return {"status_code": 400, "message": 'Не удалось обработать данные'}


@app.post("/completeRegistration/")
def complete_reg(prompt: StudentRegistrationPrompt):
    """
    Метод завершения регистрации студента
    :param prompt:
    prompt.token — секретный ключ, позволяющий студенту заврешить регистрацию
    """
    with lock:
        return 0


@app.get("/howToGet")
def how_to_get():
    return {"status_code": 200, "message": "Координаты общежития: 55.788641, 37.791508"}
