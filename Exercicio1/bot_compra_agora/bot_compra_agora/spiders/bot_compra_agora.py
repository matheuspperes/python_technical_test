from scrapy.crawler import CrawlerProcess
from scrapy_splash import SplashRequest
from pathlib import Path
import logging
import scrapy
import json
import jwt
import re

base_path = Path(__file__).parent.parent
log_path = Path(base_path, "app1.log")

# Configuração do registro
logging.basicConfig(filename=log_path, level=logging.INFO,
                    format='%(asctime)s| [%(levelname)s]: %(message)s')

class MySpider(scrapy.Spider):
    name = "bot_compra_agora"
    final_data = {}
    index = None
    number_page = 0
        
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
        "https://www.compra-agora.com/cliente/logar",
        "https://www.compra-agora.com"
    ]
    
    def start_requests(self):
        logging.info("Starting process...")
        
        form_data = {
            "data": "4c573807190709e2cb78e1abbde3fa754d72b7984e905824463909e871dd833fa010f47e2aaa73b67f2e194e24103b4462e5e3e3d330ebd3a565b0d82b7a38e7812ec2d8894358732bca27ff866ab74ef2cf1a7e4ad3f1ca01b564c931a1282bfde3f84b5da246ff6275e246b3d608fad4a948d8af8a58e876e67e47103eaf8212db801cbdbf193ca3af1b4a3059bc3c5a3f4b24d812eb7739c9d499e9929f8af0dec003b07d4e7cc28438265fd2d9270df96dde9ad94a02f1cca667d898d3fc9197e662c5e1af174864310732e8261fc7aa7038ecdcfa781ec6b8d3af9fe4b9b22a315669a11557435b5f46eed8a28a20cecb1981953b615884f89434f6cd9cae6725cf67782fb71c6da3efad05591a67539a2c698969b375e5d7c325ec833694a973a63f9ee7079e4e43c7168dc7762583a89277928371b95ca5a233beca0f480b5c588385d2b5282fef4ce9e2576605656c0f0f530bf2ea9c7985a40e7f222ea337bfcf4cf01e1b9bf8f54cb7ffbdf8b73cfe88cb72e570a513c6fa0ef73b92d56cf8f2934d63ad455305f59713625ad594eebc82b8eea062ae1dd09fad3024b7c5d0afa0e45d41bbd33ddf27b6c8a2044ae040c72203d3740a0a37f1ef9f10377655c59a0a5724b00d35a413794ff2091fa4f44cd300f491b0960742fc7c765a65a0cd9011ed821bf2574ce54417f57158b8f76ca5fa3a1f6da3484be06fc2972e8e51c66c510dadcd81977e2ca5620ec7132240e1f3bb5f48700a1e439328ef1e0caad7a62a13a2b5e9eda6e081d503b05454bd0bce8fcb897cd33d1e053618816c8ae8ae9c68c4ef8af035602405ae5ab906cab1c0b6476f09f5ecc77467c9d6ab28cabd5e6474051bb8bca379cc3815331aadc73801090568c6dd21c19ee0a06131e0b7f9a2a12b39153764bc55d375f71fe1ca8dc282ea73e37e2110e1a753f513825ab495c85eccd81238ec5dd0127564d7ffb402a8927f0386199d979997571a123bbc59ad56572bc099f71881917588fd70a64363d6d3c096678540"
        }
        yield scrapy.FormRequest(
            url=self.start_urls[0],
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
        
        yield scrapy.Request(
            url=self.start_urls[1],
            callback=self.count_categories
        )
        
    def count_categories(self, response):
        if response.status != 200:
            error = f"Site error | status: {response.status}"
            logging.error(error)
            raise Exception(error)
        
        
        all_href = response.css("li[class='lista-menu-itens'] a::attr(href)").getall()
        if self.index is None:
            self.index = 0
        
        category = all_href[self.index].split("/")[4]
        print(category)
        
        all_href[self.index] = all_href[self.index] + f"?ordenacao=0&filtro_principal=p&limit=24&p={self.number_page}"
        
        yield scrapy.Request(
            url=all_href[self.index],
            callback=self.extract_data
        )
        
        # for url in all_href:
        #     self.stop = False
        #     category = url.split("/")[4]
        #     print(category)
        #     # counter = 0
            
        #     url = url + f"?ordenacao=0&filtro_principal=p&limit=24&p="
        #     for counter in range(1, 20):
        #         if self.stop:
        #             break
        #         # counter += 1     
        #         url_category = f"{url}{counter}"           
                
        #         request = SplashRequest (
        #             url=url_category,
        #             callback=self.extract_data,
        #             # endpoint='render.html',
        #             # args={"wait": 5}
        #         )
                
    
    def extract_data(self, response):
        if response.status != 200:
            error = f"category error | status: {response.status}"
            logging.error(error)
            # self.stop = True
            raise Exception(error)
        
        products = response.css("div[class='box-produto box-catalago box-catalago-vitrine  ']").getall()
        if len(products) == 0:
            # self.stop = True
            print("0")
            return
        print(len(products))
        
        # print(len(products))
        
        


def start():
    process = CrawlerProcess()
    process.crawl(MySpider)
    process.start()
    return

start()
        
