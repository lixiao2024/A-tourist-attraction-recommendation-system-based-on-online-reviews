"""
@FileName：chengdu.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 02 - 2025/2/2\n

爬取businessid
"""
import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# 模拟浏览器
headers = {
    'cookie': 'GUID=09031116215023025465; nfes_isSupportWebP=1; UBT_VID=1737782107875.b5c4RKpvwiq3; MKT_CKID=1737782108470.sg5tk.o53x; _RF1=42.56.135.1; _RSG=peaXFI8L380oO_9..cceWA; _RDG=286d43e1517b43201638547ad8a7c03815; _RGUID=02035484-8f86-4a33-a828-9a6fbe27f632; _jzqco=%7C%7C%7C%7C1737782108639%7C1.1793697365.1737782108473.1737782108473.1737782108473.1737782108473.1737782108473.0.0.0.1.1; MKT_Pagesource=H5; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1737782119&Expires=1738386919279; _resDomain=https%3A%2F%2Fws-s.tripcdn.cn; _pd=%7B%22_o%22%3A1%2C%22s%22%3A4%2C%22_s%22%3A1%7D; _bfa=1.1737782107875.b5c4RKpvwiq3.1.1737782155448.1737782236622.1.4.214070',  # 请替换为你自己的cookie
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
    'Content-Type': 'application/json'  # 新增必要请求头
}

# 从CSV读取business_id
business_ids = []
with open('business_ids.csv', 'r', encoding='gbk') as csvfile:  # 确保文件名和路径正确
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            business_ids.append(int(row['business_id']))  # 转换为整数类型
        except KeyError:
            print("CSV文件中缺少'business_id'列")
            exit()
        except ValueError:
            print(f"无效的business_id值: {row['business_id']}")

# 获取评论数据
def fetch_comments(business_id, page=1):
    url = 'https://m.ctrip.com/webapp/you/commentWeb/commentList'  # 请求的URL
    # 定义请求体的JSON数据
    payload = {
        "poiId": None,
        "resourceId": business_id,
        "resourceType": 11,
        "pageIndex": page,  # 页码
        "pageSize": 10,  # 每页的评论数量
        "sortType": 3,
        "commentTagId": 0,
        "collapseType": 1,
        "channelType": 7,
        "videoImageSize": "700_392",
        "starType": 0,
        "sourceType": 1
    }

    # 发送 POST 请求获取页面内容
    response = requests.post(url, headers=headers, json=payload)

    # 打印返回的内容，调试用
    print(f"请求 URL: {url}")
    print(f"请求体: {json.dumps(payload, ensure_ascii=False)}")
    print(f"响应状态码: {response.status_code}")
    print(f"响应内容: {response.text[:500]}")  # 仅打印前500个字符，避免过长

    # 确保响应状态码为200
    if response.status_code == 200:
        try:
            # 解析 JSON 数据
            json_data = response.json()
            comments = json_data.get('data', {}).get('commentList', [])  # 获取评论列表
            return comments  # 返回评论数据
        except json.JSONDecodeError:
            print(f"景点 {business_id} JSON 解码失败")
    else:
        print(f"景点 {business_id} 请求失败，状态码: {response.status_code}")

    return []

# 打开 CSV 文件并准备写入
with open('comments_all_sights_Beijing.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['business_id', 'poiName', 'content', 'score'])  # 写入 CSV 文件的表头（字段名）

    # 循环遍历每个景点的 business_id
    for business_id in business_ids:
        print(f"正在爬取景点 {business_id} 的评论...")

        # 根据 business_id 获取 poiName
        poi_name = None  # 你可以通过其他方式来获取 poiName

        # 循环翻页抓取评论（假设每页10条评论，爬取前10页）
        for page in range(1, 11):  # 假设爬取前10页
            comments = fetch_comments(business_id, page)
            for comment in comments:
                content = comment.get('content', '')
                score = comment.get('score', 0)
                if content:
                    clean_content = content.replace('\n', ' ').replace('\r', '').strip()
                    clean_content = re.sub(r'[^\w\s,.:;?!\'"-]', '', clean_content)  # 去掉表情符号
                    clean_content = re.sub(r'\s+', ' ', clean_content)
                    writer.writerow([business_id, poi_name, clean_content, score])

print("所有评论已成功保存到 'comments_all_sights_Beijing.csv' 文件中！")