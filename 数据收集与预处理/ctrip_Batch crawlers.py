"""
@FileName：ctrip_Batch crawlers.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 01 - 2025/1/27\n
"""
import requests
from bs4 import BeautifulSoup
import json
import csv
import re

# 模拟浏览器
headers = {
    'cookie': 'GUID=09031116215023025465; nfes_isSupportWebP=1; UBT_VID=1737782107875.b5c4RKpvwiq3; MKT_CKID=1737782108470.sg5tk.o53x; _RF1=42.56.135.1; _RSG=peaXFI8L380oO_9..cceWA; _RDG=286d43e1517b43201638547ad8a7c03815; _RGUID=02035484-8f86-4a33-a828-9a6fbe27f632; _jzqco=%7C%7C%7C%7C1737782108639%7C1.1793697365.1737782108473.1737782108473.1737782108473.1737782108473.1737782108473.0.0.0.1.1; MKT_Pagesource=H5; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1737782119&Expires=1738386919279; _resDomain=https%3A%2F%2Fws-s.tripcdn.cn; _pd=%7B%22_o%22%3A1%2C%22s%22%3A4%2C%22_s%22%3A1%7D; _bfa=1.1737782107875.b5c4RKpvwiq3.1.1737782155448.1737782236622.1.4.214070',  # 真实cookie
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

# 北京前10个景点的 businessId 列表
business_ids = [
    229,       # 故宫博物院
    2045497,   # 北京环球度假区
    5208,   # 圆明园
    233,   # 天坛公园
    231,   # 颐和园
    230,       # 八达岭长城
    5173,   # 北京动物园
    5174,      # 恭王府
    243,       # 慕田峪长城
]

# 批量爬取每个景点的评论
def fetch_comments(business_id):
    url = f'https://m.ctrip.com/webapp/you/commentWeb/commentList?businessId={business_id}&businessType=11&noJumpApp=yes&from=https%3A%2F%2Fgs.ctrip.com%2Fhtml5%2Fyou%2Fsight%2Fbeijing1%2F{business_id}.html%3FrenderPlatform%3D%26seo%3D1'

    # 发送请求获取页面内容
    response = requests.get(url, headers=headers)

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找包含 JSON 数据的 <script> 标签
    script_tag = soup.find('script', {'id': '__NEXT_DATA__'})

    # 获取 JSON 字符串
    if script_tag:
        json_str = script_tag.string  # 获取 <script> 标签中的内容，即 JSON 字符串
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
with open('comments_beijing.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['business_id', 'content'])  # 写入 CSV 文件的表头（字段名）

    # 批量爬取前10个景点的评论
    for business_id in business_ids:
        comments = fetch_comments(business_id)
        for comment in comments:
            content = comment.get('content', '')  # 获取评论内容
            if content:  # 如果评论内容不为空
                # 去除内容中的换行符，并清理多余空格
                clean_content = content.replace('\n', ' ').replace('\r', '').strip()

                # 使用正则表达式去除表情符号和非文字字符
                clean_content = re.sub(r'[^\w\s,.:;?!\'"-]', '', clean_content)  # 去掉表情符号

                # 去除多余空格
                clean_content = re.sub(r'\s+', ' ', clean_content)  # 将多个空格替换为一个空格

                # 将评论内容和景点 business_id 写入 CSV 文件
                writer.writerow([business_id, clean_content])

print("所有评论已成功保存到 'comments_beijing.csv' 文件中！")
