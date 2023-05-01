from Person import Person


class Client(Person):
    def __init__(self, credentials: dict, cnpj: str, bank_account: dict) -> None:
        super().__init__(credentials)
        self.cnpj = cnpj
        self.bank_account = bank_account
