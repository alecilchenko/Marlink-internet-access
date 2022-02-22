from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from playsound import playsound
import time
import requests
import json



class Manager:
	def __init__(self):
		#открываем файл с паролем и задаём их
		with open('login.json', 'r') as f:
			data = f.readline()
			login_data = json.loads(data)
		self.user_name = login_data['user']
		self.password = login_data['password']
		
#переход с первой страницы, где нужно залогиниться
	def first_page(self):
		self.driver = webdriver.Chrome()
		url = 'https://m.xchange-box.com'
		self.driver.get(url)
		self.driver.find_element_by_id('login_username').send_keys(self.user_name)
		password = self.driver.find_element_by_id('login_password')
		password.send_keys(self.password)
		password.send_keys(Keys.RETURN)
		self.driver.implicitly_wait(100)
		
#переход со второй страницы по кнопке "Соединение"
	def second_page(self):
		self.driver.find_element_by_id('connection_link_open_popup').click()
		self.driver.implicitly_wait(100)
		
#проверяем цены в трейтьем окне
	def price_check(self):
		Manager.first_page(self)
		Manager.second_page(self)
		price_unit = self.driver.find_element_by_xpath('//*[@id="dialog_connection_content"]/table/tbody/tr[5]/td[2]')
		price = price_unit.text.replace('$/MiB', '').strip()
		print(price)
		self.driver.close()
		
#мониторим цену, если она нам не подходит, обновляем страницу и ждём
	def price_monitor(self):
		print('price monitor был вызван')
		Manager.first_page(self)
		Manager.second_page(self)
		price = Manager.price_check(self)
		while True:
			url_page = self.driver.current_url
			#проверка, если закончилась сессия длступа 
			if url_page == 'https://m.xchange-box.com/index.php?logout&error=unknown_user#/home.php&ui-state=dialog':
				Manager.first_page(self)
				Manager.second_page(self)
				price = Manager.price_check(self)
				print(price)
			#проверка подходяцей цены
			if float(price) == 0.45:
				print('You can connect')
				self.driver.find_element_by_xpath('//*[@id="dialog_connection_content"]/form/ul/li[2]/div/div/input').click()
				playsound('TVORCHI-Feeling OK.mp3')
			#в других случаях обновляем страницу
			else:
				time.sleep(5)
				driver.refresh()
				driver.implicitly_wait(100)
				feed_page = self.driver.current_url
				if feed_page == 'https://m.xchange-box.com/home.php':
					manager.second_page
				price = Manager.price_check(self)
				print(price)
				
#задать нового пользователя, может быть только один пользователь
	def set_user(self, user):
		with open('login.json', 'r') as f:
			data = f.readline()
			data = json.loads(data)
		data['user'] = user
		json_data = json.dumps(data)
		with open('login.json', 'w') as f:
			f.write(json_data)
			
#задать новый пароль
	def set_password(self, password):
		with open('login.json', 'r') as f:
			data = f.readline()
			data = json.loads(data)
		data['password'] = password
		json_data = json.dumps(data)
		with open('login.json', 'w') as f:
			f.write(json_data)
		

#Метод должен давать сигнал, когда пропадает интернет
	def connection_monitor(self):
		while True:
			if self.check_connection() == False:
				print('You lost connection')
				playsound('TVORCHI-Feeling OK.mp3')
				break
			else:
				print('You have connection')
	
#Метод подключает к интернету
	def connect(self):
		Manager.first_page(self)
		Manager.second_page(self)
		self.driver.find_element_by_xpath('//*[@id="dialog_connection_content"]/form/ul/li[2]/div/div/input').click()
		self.driver.close()
		
#Метод отключает интрнет
	def disconnect(self):
		Manager.first_page(self)
		Manager.second_page(self)
		self.driver.find_element_by_xpath('//*[@id="dialog_connection_content"]/form/ul/li/div/div/input').click()
		self.driver.implicitly_wait(10)
		self.driver.close()
	
#метод проверяет сколько осталось времени для интренета
	def check_remaining(self):
		Manager.first_page(self)
		Manager.second_page(self)
		time = self.driver.find_element_by_xpath('//*[@id="remainingTime"]')
		time = time.text
		print(f'У тебя осталось времени - {time}')
		
			
if __name__ == '__main__':
	pass
