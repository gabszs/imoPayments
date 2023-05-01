from Person import Person


class HouseRenter(Person):
    def __init__(self, credentials: dict, income: float, job: str, juridic_person=False, cnpj=None) -> None:
        super().__init__(credentials)
        self.income = income
        self.job = job
        self.payment_history = []
        if juridic_person:
            if cnpj != None:
                self.cnpj = cnpj
            else:
                raise Exception("O cnpj esta vazio")

    def add_payment_history(self, request):
        self.payment_history.append(request)
