"""
@FileName：ctrip_Batch crawler_plus.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 01 - 2025/1/27\n
这个代码在有得分的基础上再限定了爬取的内容有好有坏，不只有好评，且一共20条
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

# 获取评论数据
def fetch_comments(business_id, page_index=1, page_size=10):
    url = f'https://m.ctrip.com/webapp/you/commentWeb/commentList?businessId={business_id}&businessType=11&noJumpApp=yes&pageIndex={page_index}&pageSize={page_size}&from=https%3A%2F%2Fgs.ctrip.com%2Fhtml5%2Fyou%2Fsight%2Fbeijing1%2F{business_id}.html%3FrenderPlatform%3D%26seo%3D1'

    # 发送请求获取页面内容
    response = requests.get(url, headers=headers)

    # 检查是否请求成功
    if response.status_code != 200:
        print(f"请求失败，HTTP状态码: {response.status_code}")
        return []

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

# 处理获取指定评分范围的评论
def filter_comments_by_score(comments, min_score, max_score):
    filtered_comments = []
    for comment in comments:
        # 获取评分，默认值为0
        score = comment.get('score', 0)

        # 确保评分是有效的（如果评分为None或无效，默认为0）
        if score is None:
            score = 0

        if min_score <= score <= max_score:
            filtered_comments.append(comment)
    return filtered_comments

# 获取每个景点的评论，满足评分要求的评论
def get_comments_for_scenic_spot(business_id, min_comments=20):
    all_comments = []
    pageIndex = 1
    pageSize = 10  # 每次请求 10 条评论
    while len(all_comments) < min_comments:  # 至少爬取 20 条评论
        comments = fetch_comments(business_id, pageIndex, pageSize)
        if not comments:
            break  # 如果没有评论了，则停止爬取

        all_comments.extend(comments)
        pageIndex += 1  # 翻到下一页

    return all_comments

# 去除评论中的换行符、多余空格及表情符号
def clean_comment_content(content):
    clean_content = content.replace('\n', ' ').replace('\r', '').strip()
    clean_content = re.sub(r'[^\w\s,.:;?!\'"-]', '', clean_content)  # 去掉表情符号
    clean_content = re.sub(r'\s+', ' ', clean_content)  # 将多个空格替换为一个空格
    return clean_content

# 打开 CSV 文件并准备写入
with open('comments_beijing_classic.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['business_id', 'content', 'score', 'rating_type'])  # 添加 rating_type 字段

    # 批量爬取前10个景点的评论
    for business_id in business_ids:
        comments = get_comments_for_scenic_spot(business_id)

        # 筛选出评分在 3 到 5 分之间的评论
        high_score_comments = filter_comments_by_score(comments, 3, 5)
        low_score_comments = filter_comments_by_score(comments, 0, 3)

        # 保证每种类型的评论都有10条
        high_score_comments = high_score_comments[:10]
        low_score_comments = low_score_comments[:10]

        # 将评分为 3-5 分的评论保存到 CSV 文件
        for comment in high_score_comments:
            content = comment.get('content', '')
            score = comment.get('score', 0)
            if content:
                clean_content = clean_comment_content(content)
                writer.writerow([business_id, clean_content, score, 'good'])

        # 将评分为 0-3 分的评论保存到 CSV 文件
        for comment in low_score_comments:
            content = comment.get('content', '')
            score = comment.get('score', 0)
            if content:
                clean_content = clean_comment_content(content)
                writer.writerow([business_id, clean_content, score, 'bad'])

print("所有评论已成功保存到 'comments_beijing_classic.csv' 文件中！")