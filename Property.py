

class Property:
    def __init__(self, property_datails: dict) -> None:
        Property.check_json(property_datails)

        self.bathroom = property_datails["bathroom"]
        self.kitchen = property_datails["kitchen"]
        self.garage = property_datails["garage"]
        self.property_description = property_datails["property_description"]
        self.address = property_datails["property_address"]
        self.rent_value = property_datails["rent_value"]
        self.water_code = property_datails["water_code"]
        self.electricity_code = property_datails["electricity_code"]
        self.property_ref = property_datails["property_ref"]
        self.documentation_status = property_datails["documentation_status"]

    def __str__(self) -> str:
        return f"REF: {self.property_ref}, CASA: {self.property_description}"

    @classmethod
    def check_json(cls, dict):
        keys_lst = ["bathroom",
                    "kitchen",
                    "garage",
                    "property_description",
                    "property_address",
                    "rent_value",
                    "water_code",
                    "electricity_code",
                    "property_ref",
                    "documentation_status"]

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

    def get_description(self) -> dict:
        return vars(self)


if __name__ == "__main__":
    json_property = {
        'bathroom': 'bathroomTest',
        'kitchen': 'kitchenTest',
        'garage': 'garageTest',
        'property_description': 'property_descriptionTest',
        'property_address': 'property_addressTest',
        'rent_value': 'rent_valueTest',
        'water_code': 'water_codeTest',
        'electricity_code': 'electricity_codeTest',
        'property_ref': 'property_refTest',
        'documentation_status': 'documentation_statusTest',
    }
    casa = Property(json_property)
