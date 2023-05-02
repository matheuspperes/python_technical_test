from robot.robot import JKRowling
from pathlib import Path
import logging
import json

base_path = str(Path(__file__).parent.parent)
log_path = Path(base_path, "Exercicio6", "app6.log")

logging.basicConfig(filename="app6.log", level=logging.INFO,
                    format='%(asctime)s | [%(levelname)s]: %(message)s')

class StartBot:
    def __init__(self):
        self.driver = None
        self.bot = JKRowling()
        self.final_data = {}
        
    def start(self):
        driver = self.bot.open_browser()
        if driver["error"]:
            logging.error(driver["type"])
            raise Exception(driver["type"])
        self.driver = driver['driver']
        
        author_info = self.bot.author_extraction(self.driver)
        if author_info['error']:
            logging.error(author_info["type"])
            raise Exception(author_info["type"])
        self.final_data["author"] = author_info['data']
        
        logging.info("Author information extracted")
        
        self.final_data["quotes"] = []
        for counter in range(1, 11):
            self.driver.get(f"https://quotes.toscrape.com/page/{counter}")
            
            quotes = self.bot.find_quotes(self.driver)
            if quotes['error']:
                logging.error(quotes["type"])
                raise Exception(quotes["type"])
            
            for quote in quotes['data']:
                self.final_data["quotes"].append(quote)
                            
        logging.info("All information extracted successfully")
        
        self.driver.quit()
        
        path = str(Path(base_path, "Exercicio4", "final_json.json"))
        with open(path, "w") as f:
            f.write(str(json.dumps(self.final_data)))
        
if __name__ == "__main__":
    bot = StartBot()
    bot.start()
        
        
        
        