import datetime
import json

from bson import json_util
from pymongo import MongoClient
from framework.webapp import webapp

from tests.model.Vacancy import Vacancy


class Home:
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = Home()
        return cls.instance

    def __init__(self):
        self.driver = webapp.get_driver()
        self.client = MongoClient('127.0.0.1', 27017)

    def capture_vacancies(self, city):
        print("Capturando vagas", city)
        city_input = self.driver.find_elements_by_xpath('//*[@id="text-input-where"]')[0]
        city_input.clear()
        # city_input.send_keys(city)
        button = self.driver.find_elements_by_xpath('//*[@id="whatWhere"]/form/div[3]/button')[0]
        button.click()
        self.register_all_vacancies(city)

    def register_all_vacancies(self, city):
        array_vacancies = []
        vacancies = self.driver.find_elements_by_xpath("//*[contains(@class,'jobsearch-SerpJobCard')]")

        for i in range(100):
            if len(self.driver.find_elements_by_xpath('//*[@id="popover-x"]/a')):
                self.driver.find_elements_by_xpath('//*[@id="popover-x"]/a')[0].click()

            next = self.driver.find_elements_by_xpath('//*[@id="resultsCol"]/div[29]/a[{}]'.format(i + 1))
            date = datetime.datetime.now()
            for vancancy in vacancies:
                try:
                    self.driver.implicitly_wait(1)
                    vancancy.click()
                    title = self.driver.find_elements_by_xpath('//*[@id="vjs-jobtitle"]')[0].text
                    city = self.driver.find_elements_by_xpath('//*[@id="vjs-loc"]')[0].text
                    company = self.driver.find_elements_by_xpath('//*[@id="vjs-cn"]')[0].text

                    if len(self.driver.find_elements_by_xpath('//*[@id="apply-button-container"]/div[1]/a')) > 0:
                        link = self.driver.find_elements_by_xpath('//*[@id="apply-button-container"]/div[1]/a')[0] \
                            .get_attribute('href')
                    else:
                        link = self.driver.find_elements_by_xpath('//*[@id="apply-button-container"]/div[1]/span[1]')[0] \
                            .get_attribute('data-indeed-apply-joburl')

                    description = self.driver.find_elements_by_xpath('//*[@id="vjs-desc"]')[0].text
                    info = ""

                    if len(self.driver.find_elements_by_xpath('//*[@id="vjs-jobinfo"]/div[3]/span')) > 0:
                        info = self.driver.find_elements_by_xpath('//*[@id="vjs-jobinfo"]/div[3]/span')[0].text

                    array_vacancies.append(Vacancy(title, city, company, link, description, info, date).__dict__)

                except:
                    print("Error")

            if len(next) == 0:
                next = self.driver.find_elements_by_xpath('//*[@id="resultsCol"]/div[28]/a[{}]'.format(i + 1))

            if len(next) == 0:
                next = self.driver.find_elements_by_xpath('//*[@id="resultsCol"]/div[28]/a[6]')

            self.save_vacancies(array_vacancies)
            array_vacancies = []

            webapp.goto_page(next[0].get_attribute('href'))

            vacancies = self.driver.find_elements_by_xpath("//*[contains(@class,'jobsearch-SerpJobCard')]")

    def save_vacancies(self, array):
        db = self.client.bigdata
        db.vacancies.insert_many(array)


home = Home.get_instance()
