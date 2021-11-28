from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Parsing:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.status = ""
        self.expire_time = ""
        self.FIO = ""

    def parse(self, s):
        self.driver.get(s)
        el = self.driver.find_element(By.XPATH, "/html/body/div/div[2]/div[1]/div[4]/div/span[2]")
        # print(el.te)
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        self.status = soup.find('span', class_='status-value cert-name').text
        self.expire_time = soup.find('div', class_='small-text gray').text
        self.FIO = soup.find('div', class_='attrValue title-h6 bold text-center').text

    def status_getter(self):
        return self.status

    def expire_time_getter(self):
        return self.expire_time

    def FIO_getter(self):
        return self.FIO.replace('*', '').replace(' ', '.')
