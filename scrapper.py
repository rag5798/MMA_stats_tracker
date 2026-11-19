from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import random
import time
import datetime
import os


class page_scrapper:
    ufc_stats="http://ufcstats.com/statistics/events/completed?page=all"

    def __init__(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(2)
        self.results = []
        self.url = ""

    def fetch_links(self):
        try:
            #Gets Event links
            self.browser.get(f"{self.ufc_stats}")
            links = self.browser.find_elements(by=By.CLASS_NAME, value="b-link")
            dates = self.browser.find_elements(by=By.CLASS_NAME, value="b-statistics__date")
            events = []
            for link, date in zip(links, dates):
                if datetime.datetime.strptime(date.text.strip(), "%B %d, %Y").date() < datetime.date.today():
                    events.append(link.get_attribute("href"))


            #Gets Fight links
            check_set_events = set([])
            check_set_fights = set([])
            if os.path.exists("events_done.txt"):
                with open("events_done.txt") as file:
                    check_set_events = {n for n in file.read().splitlines()}
            if os.path.exists("fight_urls.txt"):
                        with open("fight_urls.txt") as file:
                            check_set_fights = {n for n in file.read().splitlines()}
            
            for link in events:
                if link in check_set_events:
                    continue
                time.sleep(random.uniform(1,4))
                self.browser.get(link)
                fight_links = self.browser.find_elements(by=By.CSS_SELECTOR, value="tbody > tr.b-fight-details__table-row")
                for n in fight_links:
                    try:
                        fight_urls = n.get_attribute("data-link")
                    except Exception as e:
                        with open("log.txt", "a") as file:
                            file.write(str(e) + ": " + n.get_attribute("outerHTML"))
                            continue
                    if fight_urls is None:
                        with open("log.txt", "a") as file:
                            file.write(n.get_attribute("outerHTML") + "\n")
                        continue
                    if fight_urls not in check_set_fights:
                        with open("fight_urls.txt", "a") as file:
                            file.write(fight_urls + "\n")
                        check_set_fights.add(fight_urls)
                with open("events_done.txt", "a") as file:
                    file.write(link + "\n")
        finally:
            self.browser.quit()

    def fetch_raw(self, url):
        time.sleep(random.uniform(1, 4))
        self.browser.get(url)

        self.browser.quit()


scrape = page_scrapper()
scrape.fetch_links()