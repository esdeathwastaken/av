import time
import json
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import telebot
from selenium.webdriver.chrome.options import Options


class Parser:
    def __init__(self):
        self.driver = self.Get_driver()
        self.wait = WebDriverWait(self.driver, 5)
        self.url = 'https://www.avito.ru/moskva_i_mo/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&f=ASgBAgECAkSSA8gQ8AeQUgFFxpoMFXsiZnJvbSI6MCwidG8iOjMwMDAwfQ&footWalkingMetro=15&i=1&metro=26-29-55-103-119-2142-2143-2151-2208-2209-2210-2211-2219-2220-2221&s=104'
        self.ids = self.Load_Ids()
        self.bot = telebot.TeleBot('5789852810:AAECNzpqKl7GUXHMP3sifXlcQncelDxYdlg')
        self.bot.config['api_key'] = '5789852810:AAECNzpqKl7GUXHMP3sifXlcQncelDxYdlg'

    def Get_driver(self):
        options = Options()
        options.add_argument('--headless')
        return webdriver.Chrome(ChromeDriverManager().install(), options=options)

    def Send_tg(self, block):
        url = block.find_element(By.XPATH, './div/div/div/a').get_attribute('href')
        res = self.bot.send_message(897888789, url)
        print(res)

    def Load_Ids(self):
        with open('ids.json') as file:
            return json.load(file)

    def Add_Ids(self, id_):
        self.ids.append(id_.get_attribute('data-item-id'))
        with open('ids.json', 'w') as file_w:
            json.dump(self.ids, file_w, indent=4)

    def Parse(self):
        self.driver.get(self.url)
        time.sleep(2)
        blocks = self.wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[@data-marker="item"]')))
        for block in blocks:
            if block.get_attribute('data-item-id') not in self.ids:
                self.Add_Ids(block)
                self.Send_tg(block)

    def main(self):
        while True:
            try:
                self.Parse()
                time.sleep(60)
            except:
                time.sleep(60)


if __name__ == '__main__':
    Worker = Parser()
    Worker.main()