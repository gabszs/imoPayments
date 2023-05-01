from Person import Person


class HouseOwner(Person):
    def __init__(self, credentials: dict) -> None:
        super().__init__(credentials)
