import scrapy
import json
import logging
import jwt
import re
from pathlib import Path
from sys import argv

base_path = Path(__file__).parent.parent

# Configuração do registro
logging.basicConfig(filename="ex2.log", level=logging.INFO,
                    format='%(asctime)s| [%(levelname)s]: %(message)s')

class MySpider(scrapy.Spider):
    name = "myspider"
    custom_settings = {
        'DOWNLOAD_DELAY': 2,
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
            'scrapy_fake_useragent.middleware.RandomUserAgentMiddleware': 400,
            'scrapy_fake_useragent.middleware.RetryUserAgentMiddleware': 401,
        },
        'FAKEUSERAGENT_PROVIDERS': [
                'scrapy_fake_useragent.providers.FakeUserAgentProvider',  
                'scrapy_fake_useragent.providers.FakerProvider',  
                'scrapy_fake_useragent.providers.FixedUserAgentProvider',  
            ]
    }
    
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Cache-Control": "max-age=0"
    }
    
    start_urls = [
        "https://pedidoeletronico.servimed.com.br/",
        "https://peapi.servimed.com.br/api/usuario/login",
        "https://peapi.servimed.com.br/api/Pedido",
        "https://peapi.servimed.com.br/api/Pedido/ObterTodasInformacoesPedidoPendentePorId/511082"
    ]

    def start_requests(self):
        logging.info("Starting process...")
        yield scrapy.Request(
            url=self.start_urls[0],
            headers=self.header,
            callback=self.login_page
        )

    def login_page(self, response):
        if response.status != 200:
            error = f"Error entering site | status: {response.status}"
            logging.error(error)
            raise Exception(error)
        
        form_data = {
            'usuario': "juliano@farmaprevonline.com.br",
            'senha': "a007299A"
        }
       
        yield scrapy.FormRequest(
            url=self.start_urls[1],
            headers=self.header,
            formdata=form_data,
            callback=self.initial_page
        )

    def initial_page(self, response):
        if response.status != 200:
            error = f"Login error | status: {response.status}"
            logging.error(error)
            raise Exception(error)
        
        logging.info("Login successful")
        session_cookie = response.headers.getlist('Set-Cookie')[0].decode('utf-8').replace("sessiontoken=", "")
        session_cookie = re.search(r'[^;]*', session_cookie).group()
        code = jwt.decode(session_cookie, options={"verify_signature": False})
        self.access_token = code["token"]
        
        form_data = {
            "dataInicio":"",
            "dataFim":"",
            "filtro":f"{str(argv[1])}",
            "pagina":"1",
            "registrosPorPagina":"10",
            "codigoExterno":"267511",
            "codigoUsuario":"22850",
            "kindSeller":"0",
            "users":["267511","518565"]
        }
        
        self.header['accesstoken'] = self.access_token, 
        yield scrapy.FormRequest(
            url=self.start_urls[2],
            formdata=form_data,
            headers=self.header,
            callback=self.my_orderedes_page
        )
    
    def my_orderedes_page(self, response):
        if response.status != 200:
            error = f"Error getting 'Meus Pedidos' page | status: {response.status}"
            logging.error(error)
            raise Exception(error)
        
        yield scrapy.Request(
            url=self.start_urls[3],
            headers=self.header,
            callback=self.ordered_details_page
        )
        
    def ordered_details_page(self, response):
        if response.status != 200:
            error = f"Error getting ordered details page | status: {response.status}"
            logging.error(error)
            raise Exception(error)
        
        final_data = {'motivo': '', 'itens':[]}
        body = json.loads(response.body)
        
        final_data['motivo'] = str(body['rejeicao']).strip()
        
        itens = body['itens']
        for index in range(len(itens)):
            product = {}
            product['codigo_produto'] = int(str(itens[index]['produto']['id']).strip())
            product['descricao'] = str(itens[index]['produto']['descricao']).strip()
            product['quantidade_faturada'] = itens[index]['quantidadeFaturada']
            
            final_data["itens"].append(product)
            
        logging.info("Process completed")
            
        with open("final_data_python.json", "w") as f:
            f.write(str(json.dumps(final_data)))
