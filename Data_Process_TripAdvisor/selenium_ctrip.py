# # �������������·��
# driver_path = "chromedriver.exe"  # �滻Ϊ���Լ��� chromedriver ·��
# driver_service = Service(driver_path)
# driver = webdriver.Chrome(service=driver_service, options=options)
from docker.models.services import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# # �������������·��
driver_path = "chromedriver.exe"  # �滻Ϊ���Լ��� chromedriver ·��
driver_service = Service(driver_path)
driver = webdriver.Chrome(service=driver_service, options=options)

# ��Я�̵ľ���ҳ�棬ȷ��business_id����Ŀ�꾰���ID
business_id = 229  # ʾ��business_id
url = f"https://www.ctrip.com/webapp/tour/attraction/{business_id}.html"
driver.get(url)
