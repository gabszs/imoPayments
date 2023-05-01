from gerencianet import Gerencianet
from requests import get
from base64 import b64decode
import json


class Billet:
    def __init__(self, api_credentials: dict, email_config: dict) -> None:
        self.credentials = api_credentials
        self.email = email_config['email']
        self.email_key = email_config['email_key']
        self.email_addressee = email_config['email_addressee']
        self.gn = Gerencianet(self.credentials)

    def create_charge(self, request_body: dict) -> dict:
        gn = Gerencianet(self.credentials)
        self.request_body = request_body
        self.request_response = self.gn.create_charge_onestep(
            params=None, body=self.request_body)  # ->

        self.pix_code = self.request_response['data']['pix']['qrcode']
        self.boleto_file = get(
            self.request_response['data']['pdf']['charge']).content
        self.qr_code = b64decode(self.request_response['data']['pix']['qrcode_image'].split(
            "data:image/svg+xml;base64,")[1])

    def cancel_charge(self, params: dict):
        """
        Args:
            params (dict): json as {'id':1}
        """
        return self.gn.cancel_charge(params=params)

    def paymentById(self, params: dict):
        """
        Args:
            params (dict): json as {'id':1}
        """
        return self.gn.detail_charge(params=params)

    def update_charge_metadata(self, id: dict, metadata: json):
        """
        Args:
            id (dict): exemple: {'id':2}
            metadata (json): _description_

        Returns:
            _type_: _description_
        """
        return gn.update_charge_metadata(params=dict, body=metadata)


if __name__ == "__main__":

    with open("config.json", encoding="utf-8") as config:
        api_config = json.load(config)
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
                "expire_at": "2023-05-15",
                "configurations": {
                    "fine": 100,
                    "interest": 33
                },
                "message": "Pague pelo código de barras ou pelo QR Code"
            }
        }
    }
    email_config = {"email": "gabrielizaac2020@gmail.com",
                    'email_key': 'lcgnjccvbyleffmd',
                    'email_addressee': ('gabrielizaac2020@gmail.com',
                                        'bonitaosp2017@gmail.com')}
    boleto = Billet(api_credentials=api_config,
                    email_config=email_config)

    boleto.create_charge(request_body=body)

    pagamento = boleto.request_response
