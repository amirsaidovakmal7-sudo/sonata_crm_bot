from config import *
import requests
import os
from datetime import datetime
import time
from requests.exceptions import JSONDecodeError
import jwt
from database.access_token_service import *
from database.refresh_token_service import *
import json
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

dotenv_path = os.path.join(BASE_DIR, ".env")


TG_USERNAME = 801567
CHOOSED_DIRECTION = 846757
CHOOSED_LANGUAGE = 846755
TG_ID = 846661





secret_code = 'def50200c4cee883019cebabcd188f91432b936ccec2bbfe007f267223c84fd524ca8e9e9f8aff3f816e6ed2c8e1233ed3f1d3657fd8e7ac84c332b7fd3537c8ec6e2191d2abdcc44b1c8fafd5333c8b471639a0d7eda7e87f76cfbaa04689c4a0571ced952c8acf796928d268afb97eef6bba3992a63b8d62887240c1d436910fb4d7996a893f7486f2393ba29fb3d5ffd0ba859d84951eace401ff700c439e3056d234b997467c2e04463d499688866bb0405b99778d39cfffabd678755f310a949be9631adeb2c7a7c8e426e953b80f36918d6a0637e2fe04adbcdc3df67d309ae5ada65523c9801c18e071ec102760fccb93d84354d548e85789ec07e89e5ebc2c0d8460a66532124adff4045db82bf2194e2915ae8756f036c9d52ca29247aa6b4a6c9c72fb7587ba139d6c2297085d1912bad3f9d84bd9c0dc2bbb148e54f5bd130827d8cc0a0cc6b939716f704366ad77b1b2ebbad1c37923e7b169025b350232b13563c2421dd375357ace95b851e35396bb5692f990166133d1ac5ebc0f2dba43f68cbdccebd21364798cc1d18e3db60a0c525179cc97f6de4975c721584bb30a303bcbbb13aa212eb6566c3d4d0cdd1233f3e4aeb9713e6653b1aae925878d2ad17391a5a8d9a1719d73d67f5c43c421ea68d2d6e3ee2f77e51bc89b7f5be62a7dbfd9ac7a'



def _is_expire(token):
    if isinstance(token, str):
        token = token.encode('utf-8')
    token_data = jwt.decode(token, options={"verify_signature": False})
    exp = datetime.utcfromtimestamp(token_data['exp'])
    now = datetime.utcnow()

    return now >= exp


def save_tokens(access_token, refresh_token):
    try:
        create_access_token(access_token)
        create_refresh_token(refresh_token)
        return True
    except Exception as e:
        return e





def get_access_token():
    return get_access_token_bd()


def get_refresh_token():
    return get_refresh_token_bd()


def get_new_tokens():
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'refresh_token',
        'refresh_token': get_refresh_token(),
        'redirect_uri': REDIRECT_URI,

    }
    response = requests.post('https://{}.amocrm.ru/oauth2/access_token'.format(SUBDOMAIN),
                             json=data).json()
    print(response)
    access_token = response['access_token']
    refresh_token = response['refresh_token']

    save_tokens(access_token, refresh_token)


class AmoCRMWrapper:
    def init_oauth2(self):
        data = {
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'grant_type': "authorization_code",
            'code': secret_code,
            'redirect_uri': REDIRECT_URI
        }
        response = requests.post('https://{}.amocrm.ru/oauth2/access_token'.format(SUBDOMAIN),
                                 json=data).json()

        print(response)
        access_token = response['access_token']
        refresh_token = response['refresh_token']

        result = save_tokens(access_token, refresh_token)

        print(f'РЕЗУЛЬТАТ: {result}, {type(result)}')




    def base_request(self, **kwargs):
        if _is_expire(get_access_token()):
            get_new_tokens()
        access_token = f"Bearer {get_access_token()}"

        headers = {
            "Authorization": access_token
        }
        req_type = kwargs.get('type')
        response = ""
        if req_type == "get":
            try:
                response = requests.get("https://{}.amocrm.ru{}".format(
                    SUBDOMAIN, kwargs.get("endpoint")), headers=headers).json()
            except JSONDecodeError as e:
                return e

        elif req_type == "get_param":
            url = "https://{}.amocrm.ru{}?{}".format(
                SUBDOMAIN,
                kwargs.get("endpoint"), kwargs.get("parameters"))
            response = requests.get(str(url), headers=headers).json()
        elif req_type == "post":
            response = requests.post("https://{}.amocrm.ru{}".format(
                SUBDOMAIN,
                kwargs.get("endpoint")), headers=headers, json=kwargs.get("data")).json()
        return response



def add_complex_lead(name, phone_number, username, tg_id, user_language, direction):
    print(user_language)
    print(direction)
    updated_language = re.sub(r'^[\U0001F000-\U0001FFFF\u2600-\u27BF\s]+', '', user_language).strip()
    updated_direction = re.sub(r'^[\U0001F000-\U0001FFFF\u2600-\u27BF\s]+', '', direction).strip()
    data = [
        {
            "source_name": "Тг бот Sonata Заявки",
            "source_uid": "Заявка из тг бота",
            "metadata": {
                "ip": "82.115.50.26",
                "form_id": "new lead",
                "form_sent_at": int(time.time()),
                "form_name": "Заявка в телеграм боте",
                "form_page": "https://sonataschool.uz",
                "referer": "https://sonataschool.uz"
            },
            "_embedded": {
                "leads": [{
                    "pipeline_id": 9124238,
                    "status_id": 73376102,
                }

                          ],
                "contacts": [
                    {
                        "name": name,
                        "custom_fields_values": [
                            {
                                "field_id": TG_USERNAME,
                                "values": [
                                    {
                                        "value": username
                                    }
                                ]
                            },
                            {
                                "field_id": CHOOSED_DIRECTION,
                                "values": [
                                    {
                                        "value": updated_direction
                                    }
                                ]
                            },
                            {
                                "field_id": CHOOSED_LANGUAGE,
                                "values": [
                                    {
                                        "value": updated_language
                                    }
                                ]
                            },
                            {
                                "field_id": TG_ID,
                                "values": [
                                    {
                                        "value": str(tg_id)
                                    }
                                ]
                            },
                            {
                                "field_code": "PHONE",
                                "values": [
                                    {
                                        "enum_code": "WORK",
                                        "value": phone_number
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]
    amocrm_wrapper = AmoCRMWrapper()
    response = amocrm_wrapper.base_request(endpoint='/api/v4/leads/complex', type='post', data=data)
    print(response)
    lead_id = response[0]['id']
    return lead_id



