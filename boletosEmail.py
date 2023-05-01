import jinja2
from gerencianet import Gerencianet
import json
from requests import get
from base64 import b64decode
import ssl
import smtplib
from email.message import EmailMessage


class Billet:
    def __init__(self, api_credentials: dict, email_config: dict) -> None:
        self.credentials = {
            'client_id': api_credentials["client_id"],
            'client_secret': api_credentials["client_secret"],
            'sandbox': api_credentials["sandbox"],
            'certificate': api_credentials["certificate"],
        }

        self.email = email_config['email']
        self.email_key = email_config['email_key']
        self.email_addressee = email_config['email_addressee']

    def htmlContent(self, context: dict) -> str:
        self.text_mold = 'Prezado(a) Sr(a) {{ name }}\n<br>\n<br>\n<br>\nIm&oacute;vel: {{ address }}\n<br>\n<br>\n<br>\nSegue em anexo o boleto de cobran&ccedil;a de aluguel do im&oacute;vel supracitado.\n<br>\n<br>\nValor Boleto: R$ {{ rent_value }}\n<br>\n<br>\nVencimento: {{ date_expire }}\n<br>\n<br>\nCaso j&aacute; tenha recebido este boleto, favor desconsiderar este email.\n<br>\n<br>\nEstamos &agrave; disposi&ccedil;&atilde;o para esclarecer eventuais d&uacute;vidas,\n<br>\n<br>\nAtenciosamente,\n<br>\n<br>\n<br>\nDepto. Administra&ccedil;&atilde;o de Im&oacute;veis\nImobiliaria Norberto, Rua Coronel Fagundes, 114\n<br>\n<br>\n(11) 4811-3981\n<br>\n<br>\n<a href="mailto:gabrielizaac2020@gmail.com" style="text-decoration: none;">gabrielizaac2020@gmail.com</a>'

        environment = jinja2.Environment()
        template = environment.from_string(self.text_mold)
        final_text = template.render(name=context["name"],
                                     address=context["address"],
                                     rent_value=context["rent_value"],
                                     date_expire=context["date_expire"])

        return final_text

    def create_charge(self, request_body: json) -> None:
        self.request_body = request_body
        gn = Gerencianet(self.credentials)
        self.request_response = gn.create_charge_onestep(
            params=None, body=self.request_body)

        self.pix_code = self.request_response['data']['pix']['qrcode']
        self.boleto_file = get(
            self.request_response['data']['pdf']['charge']).content
        self.qr_code = b64decode(self.request_response['data']['pix']['qrcode_image'].split(
            "data:image/svg+xml;base64,")[1])

        return self.request_response

    def send_email(self) -> Exception:
        try:
            expire_date = '2023-04-15'.split('-')
            expire_date = f"{expire_date[2]}-{expire_date[1]}-{expire_date[0]}"

            subject = f'IMOBILIARIA NORBERTO - Envio de Boleto/PIX Vencimento em {expire_date}'
            with open("email_bodyContent.html", "r", encoding='utf-8') as html_file:
                body_text = html_file.read()

            message = EmailMessage()
            message["From"] = self.email
            message["To"] = self.email_addressee
            message["Subject"] = subject

            message.set_content(body_text, subtype="text")
            safe = ssl.create_default_context()

            billet_name = f"boleto/PIX com vencimento em {expire_date}"
            mime_type, mime_subtype = 'application', 'pdf'

            message.add_attachment(self.boleto_file, maintype=mime_type,
                                   subtype=mime_subtype,
                                   filename=billet_name)

            with smtplib.SMTP_SSL('smtp.gmail.com',
                                  465, context=safe) as smtp:
                smtp.login(self.email, self.email_key)
                smtp.sendmail(self.email, self.email_addressee,
                              message.as_string())
        except (AttributeError):
            raise Exception(
                "The charge doesnt exist, please first create a charge")
        except (Exception) as error:
            raise Exception(
                f"A error happend during the executatio: {error}, {error.with_traceback}")

    # def set_credentials(path: str) -> None:


if __name__ == '__main__':
    email_config = {"email": "gabrielizaac2020@gmail.com",
                    'email_key': 'lcgnjccvbyleffmd',
                    'email_addressee': ('gabrielizaac2020@gmail.com',
                                        'bonitaosp2017@gmail.com', 'cesar.scorsi@gmail.com')}

    json_true = {"name": "test1", "cpf": "test1", "cnpj": "test1", "address": "test1",
                 "age": "test1", "contract": "test1", "email": "test1", "cel_number": "test1"}
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

    with open("config.json", encoding="utf-8") as config:
        api_config = json.load(config)

    client = Billet(api_credentials=api_config, email_config=email_config)

    client.create_charge(request_body=body)
    client.send_email()
