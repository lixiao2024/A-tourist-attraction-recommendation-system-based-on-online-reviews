"""
@FileName：Beijing_Final.py\n
@Description：成功案例北京9个景点100条评论及打分\n
@Author：Surely\n
@Time： 2025 - 02 - 2025/2/1\n
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
}

# 目标景点的 businessId 列表
business_ids = [
    229, 2045497, 5208, 233, 231, 230, 5173, 5174, 243,
]

# 获取评论数据
def fetch_comments(business_id, page=1):
    url = f'https://m.ctrip.com/webapp/you/commentWeb/commentList?businessId={business_id}&businessType=11&noJumpApp=yes&pageIndex={page}&pageSize=10&from=https%3A%2F%2Fgs.ctrip.com%2Fhtml5%2Fyou%2Fsight%2Fbeijing1%2F{business_id}.html%3FrenderPlatform%3D%26seo%3D1'

    # 发送请求获取页面内容
    response = requests.get(url, headers=headers)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找包含 JSON 数据的 <script> 标签
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    if script_tag:
        json_str = script_tag.string
        try:
            # 解析 JSON 数据
            json_data = json.loads(json_str)

            # 获取评论数据
            comments = json_data.get('props', {}).get('pageProps', {}).get('initialState', {}).get('commentList', [])

            return comments  # 返回评论数据
        except json.JSONDecodeError:
            print(f"景点 {business_id} JSON 解码失败")
    else:
        print(f"景点 {business_id} 没有找到包含评论的 <script> 标签")

    return []

# 打开 CSV 文件并准备写入
with open('comments_all_sights_Beijing.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['business_id','content', 'score'])  # 写入 CSV 文件的表头（字段名）

    # 循环遍历每个景点的 business_id
    for business_id in business_ids:
        print(f"正在爬取景点 {business_id} 的评论...")

        # 循环翻页抓取评论（假设每页10条评论，爬取前5页）
        for page in range(1, 11):  # 假设只爬取前5页
            comments = fetch_comments(business_id, page)
            for comment in comments:
                content = comment.get('content', '')
                score = comment.get('score', 0)
                if content:
                    clean_content = content.replace('\n', ' ').replace('\r', '').strip()
                    clean_content = re.sub(r'[^\w\s,.:;?!\'"-]', '', clean_content)  # 去掉表情符号
                    clean_content = re.sub(r'\s+', ' ', clean_content)
                    writer.writerow([business_id, clean_content, score])

print("所有评论已成功保存到 'comments_all_sights_Beijing.csv' 文件中！")