import requests
import logging
import json
import time
from constants import *


# Configuração do registro
logging.basicConfig(filename="ex3.log", level=logging.INFO,
                    format='%(asctime)s| [%(levelname)s]: %(message)s')

number_timestamp = int(time.time())


def make_get(session, url):
    response = session.post(url)
    return response

def make_post(session, url, payload):
    response = session.post(url, data=json.dumps(payload))
    return response

with requests.Session() as session:
    response = make_get(session, DEFAULT_URL + f"{str(number_timestamp)}")
    assert response.status_code == 200, logging.error(
        f"Default status code: {response.status_code}")

    service_key = response.json()['serviceKey']

    AUTHORIZATION_PAYLOAD["key"] = service_key
    response = make_post(session, AUTHORIZATION_URL, AUTHORIZATION_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Authorization status code: {response.status_code}")

    api_token = response.json()['api_token']
    response = make_post(session, LOGIN_URL + api_token, LOGIN_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Login status code: {response.status_code}")

    customer_id = response.json()["customer"]["customer_id"]
    SEARCH_CREDIT_PAYLOAD["customer_id"] = customer_id

    response = make_get(session, CARRINHO_URL + f"{str(int(time.time()))}")
    assert response.status_code == 200, logging.error(
        f"Carrinho status code: {response.status_code}")

    response = make_post(session, SEARCH_CREDIT_URL + api_token, SEARCH_CREDIT_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Search Credit status code: {response.status_code}")

    logging.info("Login successful")

    response = make_get(session, CARRINHO_URL + f"{str(int(time.time()))}")
    assert response.status_code == 200, logging.error(
        f"Carrinho2 status code: {response.status_code}")

    ADDRESSES_PAYLOAD["customer_id"] = customer_id
    response = make_post(session, ADDRESSES_URL + api_token, ADDRESSES_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Addresses status code: {response.status_code}")
    
    response = make_post(COMMERCIAL_ASSOCIATED_URL + api_token, COMMERCIAL_ASSOCIATED_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Commercial associated status code: {response.status_code}")
    
    response = make_post(PRODUTOS_TARGET_URL + api_token, PRODUTOS_TARGET_PAYLOAD)
    assert response.status_code == 200, logging.error(
        f"Produtos target status code: {response.status_code}")
    

