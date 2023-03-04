from datetime import datetime

from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from database import KijijiData, Session
from decouple import config


class KijijiScraper:
    def __init__(self, url, driver_path):
        self.url = url
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        # Headless режим запускает парсинг без графического интерфейса. Сделано
        # для большей производительности
        self.service = Service(driver_path)
        self.driver = webdriver.Chrome(service=self.service, options=options)
        self.session = Session()

    def scrape(self):
        self.driver.get(self.url)
        while True:
            print(f'Parser started. Loading...')
            cards = self.driver.find_elements(By.CLASS_NAME, 'search-item')
            for card in cards:
                title_element = card.find_element(By.CLASS_NAME, "title")
                title_text = title_element.text.strip()

                price = card.find_element(By.CLASS_NAME, 'price').text
                if '$' in price:
                    currency = price[0]
                    total_price = price[1:]
                else:
                    currency = '-'
                    total_price = price

                image = card.find_element(By.CLASS_NAME, 'image').find_element(
                    By.TAG_NAME, 'img').get_attribute('data-src')
                if not image:
                    image = 'No such elements'
                location = card.find_element(By.CLASS_NAME, "location")
                location_text = location.find_element(By.TAG_NAME, 'span').text

                location_div = card.find_element(By.CLASS_NAME, 'location')
                date_posted_span = location_div.find_element(
                    By.CSS_SELECTOR, 'span.date-posted').text
                result_date = ''
                if '/' in date_posted_span:
                    result_date = date_posted_span.replace('/', '-')
                else:
                    result_date = datetime.now().strftime('%d-%m-%Y')

                description = card.find_element(By.CLASS_NAME, "description")
                description_text = description.text

                parsed_data = KijijiData(
                    title=title_text,
                    description=description_text,
                    price=total_price,
                    currency=currency,
                    location=location_text,
                    date=result_date,
                    image=image
                )
                self.session.add(parsed_data)
            self.session.commit()

            try:
                next_button = self.driver.find_elements(
                    By.XPATH, "//a[@title='Next']")
                next_url = next_button[0].get_attribute('href')
                self.url = next_url
                next_button[0].click()
                print(self.url)
            except IndexError:
                print('There are no more pages!')
                break
        self.session.close()
        self.driver.quit()


if __name__ == "__main__":
    url = 'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-1/c37l1700273?ad=offering'
    scraper = KijijiScraper(url, driver_path=config('DRIVER_PATH'))
    scraper.scrape()
