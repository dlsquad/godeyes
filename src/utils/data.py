
class Data:
    url = str
    code = str
    position = str

class Response:
    isSuccess = str
    msg = str
    data = Data

class Form:
    position = str
    name = str

class FormResponse:
    isSuccess = str
    msg = str
    date = [Form]


