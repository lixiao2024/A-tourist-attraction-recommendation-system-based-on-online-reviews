"""
@FileName：Scrip1.py\n
@Description：TripAdvisor网站数据爬取第一试\n
@Author：Surely\n
@Time： 2025 - 01 - 2025/1/30\n
"""

# ./chromedriver.exe
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By  # 导入 By
from selenium.webdriver.common.keys import Keys  # 导入 Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import csv
import os
import sys
sys.stdout.reconfigure(encoding='gbk')
def save_data(name, score, user, detail, data):
    filename = f"{name}.csv"
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Score", "User", "Detail", "Date", "IP Location"])
        date = data[:10]
        ip_location = data[10:]
        writer.writerow([score, user, detail, date, ip_location])

def changW():
    all_windows = driver.window_handles

    for window in all_windows:
        if window != driver.current_window_handle:
            driver.switch_to.window(window)
            break

service = Service(r"./chromedriver.exe")

driver = webdriver.Chrome(service=service)

driver.get("https://you.ctrip.com/globalsearch/?keyword=%E5%B1%B1%E8%A5%BF%E5%8F%A4%E5%BB%BA")
print(driver.title)
time.sleep(2)

gslmore = driver.find_element(By.ID, "home-page-travel-list").find_element(By.CLASS_NAME, "gsl-more")
time.sleep(2)
actions1 = ActionChains(driver)
actions1.click(gslmore)
actions1.perform()

time.sleep(3)

for pachange in range(1,11):
    time.sleep(2)
    page = driver.find_element(By.XPATH, '//input[@aria-label="页"]')
    page.send_keys(f'{pachange}')
    page.send_keys(Keys.RETURN)
    time.sleep(1)
    view = driver.find_element(By.ID, "home-page-travel-list").find_elements(By.CLASS_NAME, "gsl-common-card")
    for vichange in view[(6 if pachange == 1 else 0):]:
        actions2 = ActionChains(driver)
        actions2.click(vichange)
        actions2.perform()
        time.sleep(2)
        windows = driver.window_handles
        driver.switch_to.window(windows[1])
        previous_first_user = None
        for chatN in range(2,400):
            time.sleep(8)
            html_source = driver.page_source
            soup = BeautifulSoup(html_source, 'lxml')
            name = soup.find("div", {"class": "title"}).find("h1").text
            chats = soup.find_all("div", {"class": "commentItem"})
            if not chats:
                print("没有更多评论，结束爬取。")
                driver.close()
                break
            current_first_user = chats[0].find("div", {"class": "userName"}).text
            if previous_first_user is not None and current_first_user == previous_first_user:
                print("到达最后一页，结束爬取。")
                driver.close()
                break
            for chat in chats:
                user = chat.find("div", {"class": "userName"}).text
                detail = chat.find("div", {"class": "commentDetail"}).text
                score = chat.find("span", {"class": "averageScore"}).text
                data = chat.find("div", {"class": "commentTime"}).text
                print(score)
                print(user)
                print(detail)
                print(data)
                save_data(name, score, user, detail, data)
            previous_first_user = current_first_user
            chatNUM = driver.find_element(By.CSS_SELECTOR, "li.ant-pagination-options input[type='text']")
            chatNUM.send_keys(chatN)
            chatNUM.send_keys(Keys.RETURN)
            time.sleep(2)

        windows = driver.window_handles
        driver.switch_to.window(windows[0])
