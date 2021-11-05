from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import time

class WebDriver:

    location_data = {}

    def __init__(self):
        self.PATH = "D:\Python\Driver\Chrome\chromedriver.exe"
        self.options = Options()
        # self.options.binary_location = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe"
        self.options.add_argument("--headless")
        self.driver = webdriver.Chrome(self.PATH, options=self.options)

        self.location_data["rating"] = "NA"
        self.location_data["reviews_count"] = "NA"
        self.location_data["location"] = "NA"
        self.location_data["contact"] = "NA"
        self.location_data["website"] = "NA"
        self.location_data["Time"] = {"Monday":"NA", "Tuesday":"NA", "Wednesday":"NA", "Thursday":"NA", "Friday":"NA", "Saturday":"NA", "Sunday":"NA"}
        self.location_data["Reviews"] = []
        self.location_data["Popular Times"] = {"Monday":[], "Tuesday":[], "Wednesday":[], "Thursday":[], "Friday":[], "Saturday":[], "Sunday":[]}

    def scroll_the_page(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "section-layout-root")))

            pause_time = 2
            max_count = 5
            x = 0

            while(x<max_count):
                scrollable_div = self.driver.find_element_by_css_selector('div.section-layout.section-scrollbox.scrollable-y.scrollable-show')
                try:
                    self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', scrollable_div)
                except:
                    pass
                time.sleep(pause_time)
                x=x+1
        except:
            self.driver.quit()

    def expand_all_reviews(self):
        try:
            element = self.driver.find_elements_by_class_name("BgrMEd BgrMEd-text")
            for i in element:
                i.click()
        except:
            pass

    def get_reviews_data(self):
        try:
            review_names = self.driver.find_elements_by_class_name("ODSEW-ShBeI-RWgCYc ODSEW-ShBeI-RWgCYc-SfQLQb-BKD3ld")
            review_text = self.driver.find_elements_by_class_name("ODSEW-ShBeI-ShBeI-content")
            review_dates = self.driver.find_elements_by_css_selector("[class='ODSEW-ShBeI-RgZmSc-date']")
            review_stars = self.driver.find_elements_by_css_selector("[class='ODSEW-ShBeI-H1e3jb']")

            review_stars_final = []

            for i in review_stars:
                review_stars_final.append(i.get_attribute("aria-label"))

            review_names_list = [a.text for a in review_names]
            review_text_list = [a.text for a in review_text]
            review_dates_list = [a.text for a in review_dates]
            review_stars_list = [a for a in review_stars_final]

            for (a,b,c,d) in zip(review_names_list, review_text_list, review_dates_list, review_stars_list):
                self.location_data["Reviews"].append({"name":a, "review":b, "date":c, "rating":d})

        except Exception as e:
            pass

    def scrape(self, url):
        time.sleep(10)
        self.scroll_the_page()
        self.expand_all_reviews()
        self.get_reviews_data()
        self.driver.quit()
        return(self.location_data)
url = "https://www.google.it/maps/place/Anteraja/@-6.224705,106.8278741,17z/data=!3m1!4b1!4m5!3m4!1s0x2e69f302656f37b5:0xe80bb4258dbec662!8m2!3d-6.224705!4d106.8300628"
x = WebDriver()
print(x.scrape(url))