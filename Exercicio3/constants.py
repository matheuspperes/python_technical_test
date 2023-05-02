# URLs
DEFAULT_URL = "https://carrinho-inusd5bbia-rj.a.run.app/Login/GetServiceKey?_="
AUTHORIZATION_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/authorization"
LOGIN_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/login&api_token="
CARRINHO_URL = "https://carrinho-inusd5bbia-rj.a.run.app/Login/GetConfigSystem/0?_="
SEARCH_CREDIT_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/search_credit&api_token="
ADDRESSES_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/addresses&api_token="
COMMERCIAL_ASSOCIATED_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/commercial_condition_associated&api_token="
# GET_CART_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/get_cart_ui&api_token="
PRODUTOS_TARGET_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/produtos_integracao_target&api_token="
CART_ADD_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/cart_add&api_token="
COMMERCIAL_CONDITION_URL = "https://coopertotal.nc7i.app/index.php?route=api/v2/rest_cooper/commercial_condition&api_token="

# Payloads
AUTHORIZATION_PAYLOAD = {
    "key": "",
    "username": "default",
}

LOGIN_PAYLOAD = {
    "email": "leonardo@coopertotal.com.br",
    "password": "1234",
    "storeid": 0
}

SEARCH_CREDIT_PAYLOAD = {
    "customer_id": ""
}

ADDRESSES_PAYLOAD = {
    "customer_id": ""
}

COMMERCIAL_ASSOCIATED_PAYLOAD = {
    "commercial_condition_id":"103"
}
# GET_CART_PAYLOAD = {
#     "address_id":"535",
#     "commercial_condition_id":"103"
# }

PRODUTOS_TARGET_PAYLOAD = {
    "commercial_condition_id":"344",
    "pay_term_id":"1"
}

CART_ADD_PAYLOAD = {
    "products": [{
        "ean": "7897595901927",
        "discount": 4,
        "price": 62.98,
        "product_id": 34748,
        "quantity": 2,
        "name": "AAS INFANTIL 100MG 120CPR",
        "manufacturer": "HYPERA PP",
        "tax": 1.45,
        "category": "ANALGESICOS E ANTIPIRETICOS",
        "cashback": 0
    },
        {
        "ean": "7896241225547",
        "discount": 5,
        "price": 52.68,
        "product_id": 30,
        "quantity": 1,
        "name": "ABLOK PLUS 100/25MG 30CPR",
        "manufacturer": "BIOLAB SANUS",
        "tax": 1.09,
        "category": "ANTI-HIPERTENSIVOS",
        "cashback": 0
    }]
}

COMMERCIAL_CONDITION_PAYLOAD = {
    "address_id": "535",
    "commercial_condition_id":"103",
    "commercial_condition":"CONDIÇÃO DIAMANTE A PRAZO",
    "pay_term_id":"1",
    "name":"42 DIAS",
    "code":"001",
    "minimum_value":"100",
    "comercial_condition_queue":""
}