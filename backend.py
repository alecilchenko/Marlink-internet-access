from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playsound import playsound
import time
import json


class Manager:
    def __init__(self):
        self.driver = None
        with open("login.json", "r") as f:
            data = f.readline()
            login_data = json.loads(data)
        self.user_name = login_data["user"]
        self.password = login_data["password"]

    def first_page(self):
        self.driver = webdriver.Chrome()
        url = "https://m.xchange-box.com"
        self.driver.get(url)
        self.driver.find_element_by_id(
            "login_username"
        ).send_keys(self.user_name)
        password = self.driver.find_element_by_id("login_password")
        password.send_keys(self.password)
        password.send_keys(Keys.RETURN)
        self.driver.implicitly_wait(100)

    def second_page(self):
        self.driver.find_element_by_id("connection_link_open_popup").click()
        self.driver.implicitly_wait(100)

    def price_check(self):
        Manager.first_page(self)
        Manager.second_page(self)
        price_unit = self.driver.find_element_by_xpath(
            '//*[@id="dialog_connection_content"]/table/tbody/tr[5]/td[2]'
        )
        price = price_unit.text.replace("$/MiB", "").strip()
        return price

    def price_monitor(self):
        price = Manager.price_check(self)
        while True:
            url_page = self.driver.current_url
            if (
                url_page
                == "https://m.xchange-box.com/index.php?"
                   "logout&error=unknown_user#/home.php&ui-state=dialog"
            ):
                self.driver.close()
                price = Manager.price_check(self)
            if float(price) == 0.45:
                print("You can connect")
                self.driver.close()
                playsound("TVORCHI-Feeling OK.mp3")
                break
            else:
                time.sleep(5)
                self.driver.refresh()
                self.driver.implicitly_wait(100)
                feed_page = self.driver.current_url
                if (
                    feed_page
                    == "https://m.xchange-box.com/home.php#/"
                       "home.php&ui-state=dialog"
                ):
                    Manager.second_page(self)
                price_unit = self.driver.find_element_by_xpath(
                    '//*[@id="dialog_connection_content"'
                    ']/table/tbody/tr[5]/td[2]'
                )
                price = price_unit.text.replace("$/MiB", "").strip()

    @staticmethod
    def set_user(user):
        with open("login.json", "r") as f:
            data = f.readline()
            data = json.loads(data)
        data["user"] = user
        json_data = json.dumps(data)
        with open("login.json", "w") as f:
            f.write(json_data)

    @staticmethod
    def set_password(password):
        with open("login.json", "r") as f:
            data = f.readline()
            data = json.loads(data)
        data["password"] = password
        json_data = json.dumps(data)
        with open("login.json", "w") as f:
            f.write(json_data)

    def connect(self):
        Manager.first_page(self)
        Manager.second_page(self)
        self.driver.find_element_by_xpath(
            '//*[@id="dialog_connection_content"]/form/ul/li[2]/div/div/input'
        ).click()
        self.driver.close()

    def disconnect(self):
        Manager.first_page(self)
        Manager.second_page(self)
        self.driver.find_element_by_xpath(
            '//*[@id="dialog_connection_content"]/form/ul/li/div/div/input'
        ).click()
        self.driver.implicitly_wait(10)
        self.driver.close()

    def check_remaining(self):
        Manager.first_page(self)
        Manager.second_page(self)
        time_limit = self.driver.find_element_by_xpath(
            '//*[@id="remainingTime"]'
        )
        time_limit = time_limit.text
        print(f"У тебя осталось времени - {time_limit}")
        self.driver.close()
