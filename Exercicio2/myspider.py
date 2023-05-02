import scrapy

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
        "https://peapi.servimed.com.br/api/Pedido"
    ]

    def start_requests(self):
        yield scrapy.Request(
            url=self.start_urls[0],
            headers=self.header,
            callback=self.parse_page1
        )

    def parse_page1(self, response):
        form_data = {
            'usuario': "juliano@farmaprevonline.com.br",
            'senha': "a007299A"
        }
       
        yield scrapy.FormRequest(
            url=self.start_urls[1],
            headers=self.header,
            formdata=form_data,
            callback=self.parse_page2
        )

    def parse_page2(self, response):
        print(response.headers)
        session_cookie = response.headers
        print(response.headers)
        
        form_data = {
            "dataInicio":"",
            "dataFim":"",
            "filtro":"",
            "pagina":"1",
            "registrosPorPagina":"10",
            "codigoExterno":"267511",
            "codigoUsuario":"22850",
            "kindSeller":"0",
            "users":["267511","518565"]
        }
        
        yield scrapy.Request(
            url=self.start_urls[2],
            # formdata=form_data,
            headers=self.header,
            cookies={
                'session': session_cookie,
            },
            callback=self.parse_page3
        )
    
    def parse_page3(self, response):
        print("status: ", response.status)
        # parse the response from the first URL
        print("response: ", response.text)
        ...

    # def after_login(self, response):
    #     # click a button to access the dashboard
    #     yield scrapy.FormRequest(
    #         url=""
    #         formdata = {
    #         'usuario': "juliano@farmaprevonline.com.br",
    #         'senha': "a007299A"
    #         },
    #         callback=self.after_dashboard
    #     )

    # def after_dashboard(self, response):
    #     # do something after accessing the dashboard, such as extract data
    #     data = response.xpath('//title/text()').get()
    #     print(data)
