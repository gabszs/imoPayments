

class Person:
    def __init__(self, credentials: dict) -> None:
        Person.check_json(credentials)

        self.name = credentials['name']
        self.cpf = credentials['cpf']
        self.address = credentials['address']
        self.rg = credentials['rg']
        self.orgao_emissor = credentials['orgao_emissor']
        self.age = credentials['age']
        self.email = credentials['email']
        self.cel_number = credentials['cel_number']
        self.nationality = credentials['nationality']
        self.civil_status = credentials['civil_status']
        self.cep = credentials['cep']
        self.bank_account = credentials["bank_account"]

    def __str__(self) -> str:
        return f"Name: {self.name}, Class: {__class__.__name__}"

    def get_attr(self) -> dict:
        return vars(self)

    @classmethod
    def check_json(cls, dict):
        keys_lst = ["name", "cpf", "address", "rg", "orgao_emissor",
                    "age", "email", "cel_number", "nationality",
                    "civil_status", "cep", "bank_account"]

        try:
            if len(keys_lst) == len(dict):
                for count, keys in enumerate(dict.keys()):
                    if keys not in keys_lst:
                        raise Exception(
                            "As chaves do json nao estao propriamente escritas, cheque novamente os valores")
            else:
                raise Exception(
                    "Ha chaves faltantes, cheque novamente as chaves")
        except:
            raise Exception("Houve um erro")


class Test:
    def __init__(self, number) -> None:
        self.number = number

    def double(self):
        return self.number * 2


class Test2:
    def __init__(self, number) -> None:
        self.number = number
        self.double = Test.double()


if __name__ == "__main__":
    json_p = {'name': 'gabriel',
              'cpf': 1234123,
              'address': '3',
              'rg': '4',
              'orgao_emissor': '5',
              'age': '6',
              'email': '7',
              'cel_number': '8',
              'nationality': '9',
              'civil_status': '11',
              'cep': '13',
              "bank_account": 'itau'}

    p1 = Person(json_p)

    test1 = Test(2)
    print(test1.double())
    Test2(4)
