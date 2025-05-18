"""
@FileName：chengdu.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 02 - 2025/2/1\n
"""
# 模拟浏览器
import  requests
from bs4 import BeautifulSoup
import json
import csv
import re
headers = {
    'cookie': 'GUID=09031133115752733078; nfes_isSupportWebP=1; _resDomain=https%3A%2F%2Fbd-s.tripcdn.cn; UBT_VID=1738645722047.b71197Ymnpfp; _RF1=42.56.134.103; _RSG=byq46D3Jla8TKiwpRImT.9; _RDG=28e66ff9e6b2d625000fe12191ea0d0b3a; _RGUID=892f4c33-4613-4f25-9f9d-c126f3eac51d; _pd=%7B%22_o%22%3A18%2C%22s%22%3A1399%2C%22_s%22%3A2%7D; _bfa=1.1738645722047.b71197Ymnpfp.1.1738645730987.1738645790069.1.3.10650053721',  # 真实cookie
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

url = "https://www.tripadvisor.cn/Attraction_Review-g297463-d457089-Reviews-Giant_Panda_Breeding_Research_Base_Xiongmao_Jidi-Chengdu_Sichuan.html"
response = requests.get(url = url, headers=headers)
json_data = response.json()
print(json_data)
