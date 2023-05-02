import requests
import logging
import json
import time
from constants import *

# Configuração do registro
logging.basicConfig(filename='app3.log', level=logging.INFO,
                    format='%(asctime)s| [%(levelname)s]: %(message)s')

number_timestamp = int(time.time())

with requests.Session() as session:
    response = session.get(DEFAULT_URL + f"{str(number_timestamp)}")
    assert response.status_code == 200, logging.error(
        f"Default status code: {response.status_code}")

    service_key = response.json()['serviceKey']

    AUTHORIZATION_PAYLOAD["key"] = service_key
    response = session.post(
        AUTHORIZATION_URL,
        data=json.dumps(AUTHORIZATION_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Authorization status code: {response.status_code}")

    api_token = response.json()['api_token']
    response = session.post(
        LOGIN_URL + api_token,
        data=json.dumps(LOGIN_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Login status code: {response.status_code}")

    customer_id = response.json()["customer"]["customer_id"]
    SEARCH_CREDIT_PAYLOAD["customer_id"] = customer_id

    response = session.get(CARRINHO_URL + f"{str(int(time.time()))}")
    assert response.status_code == 200, logging.error(
        f"Carrinho status code: {response.status_code}")

    response = session.post(
        SEARCH_CREDIT_URL + api_token,
        data=json.dumps(SEARCH_CREDIT_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Search Credit status code: {response.status_code}")

    logging.info("Login successful")

    response = session.get(CARRINHO_URL + f"{str(int(time.time()))}")
    assert response.status_code == 200, logging.error(
        f"Carrinho2 status code: {response.status_code}")

    ADDRESSES_PAYLOAD["customer_id"] = customer_id
    response = session.post(
        ADDRESSES_URL + api_token,
        data=json.dumps(ADDRESSES_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Addresses status code: {response.status_code}")
    
    ######
    
    response = session.post(
        COMMERCIAL_ASSOCIATED_URL + api_token,
        data=json.dumps(COMMERCIAL_ASSOCIATED_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Commercial associated status code: {response.status_code}")
    
    response = session.post(
        PRODUTOS_TARGET_URL + api_token,
        data=json.dumps(PRODUTOS_TARGET_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Produtos target status code: {response.status_code}")
    
    ######
    
    response = session.post(
        CART_ADD_URL + api_token,
        data=json.dumps(CART_ADD_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Cart add status code: {response.status_code}")
    print(response.status_code)
    
    response = session.post(
        COMMERCIAL_CONDITION_URL + api_token,
        data=json.dumps(COMMERCIAL_CONDITION_PAYLOAD)
    )
    assert response.status_code == 200, logging.error(
        f"Commercial condition status code: {response.status_code}")
    print(response.status_code)
    
    
    # response = session.post(
    #     GET_CART_URL + api_token,
    #     data=json.dumps(GET_CART_PAYLOAD)
    # )
    # assert response.status_code == 200, logging.error(
    #     f"Get cart status code: {response.status_code}")
    
    # response = session.post(
    #     PRODUTOS_TARGET_URL + api_token,
    #     data=json.dumps(PRODUTOS_TARGET_PAYLOAD)
    # )
    # assert response.status_code == 200, logging.error(
    #     f"Produtos target status code: {response.status_code}")
    # print(response.json())
