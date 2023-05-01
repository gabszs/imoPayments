from Client import Client
from boletosEmail import Billet
from HouseOwner import HouseOwner
from HouseRenter import HouseRenter
from Property import Property
import json
import smtplib
from email.message import EmailMessage
import jinja2
from gerencianet import Gerencianet
import json
from requests import get
from base64 import b64decode
import ssl
import smtplib
from email.message import EmailMessage

st = "Listar, Adicionar, Remover, Entrada, Saida, Sair".split(", ")
for item in st:
    print(f"case Menu.{item}:\n    break;")


class Rents:
    def __init__(self, Client: Client, HouseOwner: HouseOwner, HouseRenter: HouseRenter,
                 Property: Property, bank_api_credential=dict, email_config=dict,
                 data_start=str, security_deposit=0,) -> None:
        self.Client = Client
        self.HouseOwner = HouseOwner
        self.HouseRenter = HouseRenter
        self.Property = Property
        self.bank_api_credential = bank_api_credential
        self.email_config = email_config
        # self.Billet = Billet(
        #     api_credentials=bank_api_credential, email_config=email_config)
        self.bank_api_credential = bank_api_credential
        self.email_config = email_config
        self.data_start = data_start
        self.security_deposit = security_deposit
        self.payments_history = []
        self.charges_history = []
        self.htmlContent = Billet.htmlContent
        self.email = email_config['email']
        self.email_key = email_config['email_key']
        self.email_addressee = Client.email

    def __str__(self) -> str:
        return f"Client: {self.Client}, HouseOwner: {self.HouseOwner}, Class: {__class__.__name__}"

    def re_config_Billet(self, bank_api_credential=dict, email_config=dict):
        self.Billet = Billet(
            api_credentials=bank_api_credential, email_config=email_config)

    def create_charge(self, body, send_email=False, email_context=dict) -> dict:
        payment = Billet(api_credentials=self.bank_api_credential,
                         email_config=self.email_config)
        payment.create_charge(request_body=body)
        if send_email:
            if email_context:
                body_text = self.htmlContent(context=email_context)
            else:
                body_text = {
                    "name": self.HouseRenter.name,
                    "address": self.Property.address,
                    "rent_value": self.Property.rent_value,
                    "date_expire": self.data_start
                }
            payment.send_email()

        # self.Billet.create_charge(request_body=body)
        # print(self.Billet.pix_code, self.Billet.qr_code)
        # print(vars(self.Billet))

        # self.charges_history.append({
        #     "paymentObject": payment.request_response,
        #     'pix_code': (payment.pix_code if type(payment.pix_code) != None else ""),
        #     'boleto_file': payment.boleto_file,
        #     'qr_code': payment.qr_code
        # })

        # if send_email:
        #     if email_context:
        #         body_text = self.htmlContent(context=email_context)
        #     else:
        #         body_text = {
        #             "name": self.HouseRenter.name,
        #             "address": self.Property.address,
        #             "rent_value": self.Property.rent_value,
        #             "date_expire": self.data_start
        #         }

        #     self.send_email(body_text, payment.boleto_file)
        # return payment.request_response

    def send_email(self, body_text, billet_code) -> Exception:

        expire_date = self.data_start
        subject = f'IMOBILIARIA NORBERTO - Envio de Boleto/PIX Vencimento em {expire_date}'
        with open("email_bodyContent.html", "r", encoding='utf-8') as html_file:
            body_text = html_file.read()
        message = EmailMessage()
        message["From"] = self.email
        message["To"] = self.email_addressee
        message["Subject"] = subject

        message.set_content(body_text, subtype="html")
        safe = ssl.create_default_context()

        billet_name = f"boleto/PIX com vencimento em {expire_date}"
        mime_type, mime_subtype = 'application', 'pdf'

        message.add_attachment(billet_code, maintype=mime_type,
                               subtype=mime_subtype,
                               filename=billet_name)

        with smtplib.SMTP_SSL('smtp.gmail.com',
                              465, context=safe) as smtp:
            smtp.login(self.email, self.email_key)
            smtp.sendmail(self.email, self.email_addressee,
                          message.as_string())
        # try:
        #     # expire_date = '2023-04-15'.split('-')
        #     # expire_date = f"{expire_date[2]}-{expire_date[1]}-{expire_date[0]}"

        #     expire_date = self.data_start
        #     subject = f'IMOBILIARIA NORBERTO - Envio de Boleto/PIX Vencimento em {expire_date}'

        #     message = EmailMessage()
        #     message["From"] = self.email
        #     message["To"] = self.email_addressee
        #     message["Subject"] = subject

        #     message.set_content(body_text, subtype="html")
        #     safe = ssl.create_default_context()

        #     billet_name = f"boleto/PIX com vencimento em {expire_date}"
        #     mime_type, mime_subtype = 'application', 'pdf'

        #     message.add_attachment(billet_code, maintype=mime_type,
        #                            subtype=mime_subtype,
        #                            filename=billet_name)

        #     with smtplib.SMTP_SSL('smtp.gmail.com',
        #                           465, context=safe) as smtp:
        #         smtp.login(self.email, self.email_key)
        #         smtp.sendmail(self.email, self.email_addressee,
        #                       message.as_string())
        # except (AttributeError):
        #     raise Exception(
        #         "The charge doesnt exist, please first create a charge")
        # except (Exception) as error:
        #     raise Exception(
        #         f"A error happend during the executatio: {error}, {error.with_traceback}")


if __name__ == "__main__":
    with open("config.json", encoding="utf-8") as config:
        api_config = json.load(config)

    email_config = {"email": "gabrielizaac2020@gmail.com",
                    'email_key': 'lcgnjccvbyleffmd',
                    'email_addressee': ('gabrielizaac2020@gmail.com',
                                        'bonitaosp2017@gmail.com')}

    body = {
        "items": [
            {
                "name": "Meu Produto",
                "value": 5990,
                "amount": 1
            }
        ],
        "payment": {
            "banking_billet": {
                "customer": {
                    "name": "Gabriel Izaac Norberto de Carvalho",
                    "cpf": "03680056230",
                    "email": "gabrielizaac2020@gmail.com",
                    "phone_number": "11947047830",
                    "address": {
                            "street": "Avenida Juscelino Kubitschek",
                            "number": "909",
                            "neighborhood": "Bauxita",
                            "zipcode": "35400000",
                            "city": "Ouro Preto",
                            "complement": "",
                            "state": "MG"
                    }
                },
                "expire_at": "2023-04-15",
                "configurations": {
                    "fine": 100,
                    "interest": 33
                },
                "message": "Pague pelo código de barras ou pelo QR Code"
            }
        }
    }

    json_HouseOwner = {'name': 'nameTestHouseOwner',
                       'cpf': 'cpfTestHouseOwner',
                       'address': 'addressTestHouseOwner',
                       'rg': 'rgTestHouseOwner',
                       'orgao_emissor': 'orgao_emissorTestHouseOwner',
                       'age': 'ageTestHouseOwner',
                       'email': 'emailTestHouseOwner',
                       'cel_number': 'cel_numberTestHouseOwner',
                       'nationality': 'nationalityTestHouseOwner',
                       'civil_status': 'civil_statusTestHouseOwner',
                       'cep': 'cepTestHouseOwner',
                       'bank_account': 'bank_accountTestHouseOwner', }
    json_HouseRenter = {
        'name': 'nameTestHouseRenter',
        'cpf': 'cpfTestHouseRenter',
        'address': 'addressTestHouseRenter',
        'rg': 'rgTestHouseRenter',
        'orgao_emissor': 'orgao_emissorTestHouseRenter',
        'age': 'ageTestHouseRenter',
        'email': 'emailTestHouseRenter',
        'cel_number': 'cel_numberTestHouseRenter',
        'nationality': 'nationalityTestHouseRenter',
        'civil_status': 'civil_statusTestHouseRenter',
        'cep': 'cepTestHouseRenter',
        'bank_account': 'bank_accountTestHouseRenter',
    }
    json_Client = {'name': 'nameTestHouseClient',
                   'cpf': 'cpfTestHouseClient',
                   'address': 'addressTestHouseClient',
                   'rg': 'rgTestHouseClient',
                   'orgao_emissor': 'orgao_emissorTestHouseClient',
                   'age': 'ageTestHouseClient',
                   'email': 'emailTestHouseClient',
                   'cel_number': 'cel_numberTestHouseClient',
                   'nationality': 'nationalityTestHouseClient',
                   'civil_status': 'civil_statusTestHouseClient',
                   'cep': 'cepTestHouseClient',
                   'bank_account': 'bank_accountTestHouseClient', }
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

    inquilino = HouseRenter(json_HouseRenter, 1200.23, "marceneiro")
    locador = HouseOwner(json_HouseOwner)
    casa = Property(json_property)
    dono_imo = Client(json_Client, "23412341234", {
                      "banco": "itau", "conta": "21344213"})

    aluguel = Rents(dono_imo, locador, inquilino, casa,
                    api_config, email_config, "22222", 2)
    email_mess = {
        "name"
    }

    test = aluguel.create_charge(body, send_email=True, email_context={})
    print(aluguel.charges_history)
