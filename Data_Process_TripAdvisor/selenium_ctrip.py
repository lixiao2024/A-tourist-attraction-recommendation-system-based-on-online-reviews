# # 设置浏览器驱动路径
# driver_path = "chromedriver.exe"  # 替换为你自己的 chromedriver 路径
# driver_service = Service(driver_path)
# driver = webdriver.Chrome(service=driver_service, options=options)
from docker.models.services import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# # 设置浏览器驱动路径
driver_path = "chromedriver.exe"  # 替换为你自己的 chromedriver 路径
driver_service = Service(driver_path)
driver = webdriver.Chrome(service=driver_service, options=options)

# 打开携程的景点页面，确保business_id是你目标景点的ID
business_id = 229  # 示例business_id
url = f"https://www.ctrip.com/webapp/tour/attraction/{business_id}.html"
driver.get(url)
