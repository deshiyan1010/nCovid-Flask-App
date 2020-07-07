from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pickle


def message(country_code,number,text):
  chrome_options = Options()
  chrome_options.add_argument("user-data-dir=selenium") 
  #chrome_options.set_headless()
  driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=chrome_options)

  cookies = pickle.load(open("cookies.pkl", "rb"))
  for cookie in cookies:
    driver.add_cookie(cookie)

  num = "+"+str(country_code)+str(number)
  driver.get('https://web.whatsapp.com/send?phone='+str(num))
  
  #input()
  #pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
  
  #name = input('Enter the name of user or group : ')
  msg = text.split("\n")#input('Enter the message : ')
  #Scan the code before proceeding further
  # user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name))
  # user.click()
  flag = 0
  while flag==0:

    try:
      msg_box = driver.find_element_by_class_name('_3FRCZ')
      msg_box = driver.find_element_by_xpath("//div[@class='_3FRCZ copyable-text selectable-text' and @data-tab='1']")

      for ms in msg:
        msg_box.send_keys(ms)
        msg_box.send_keys(Keys.SHIFT+Keys.ENTER)
      
      driver.find_element_by_class_name('_1U1xa').click()

      flag=1

    except:
      pass

  driver.quit()

if __name__ == "__main__":
  
  message(91,9108469502,"sup")