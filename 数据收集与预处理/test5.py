import requests

url = "https://secrob.ctrip.com/comment/api/getCommentList"
params = {
    "business_id" : 229,  # 替换为实际景点ID
    "page": 1,
    "pageSize": 10,
    "score": 0  # 尝试筛选低分评论（参数需根据实际接口调整）
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...",
    "Referer": "https://you.ctrip.com/",
    "Cookie": "携带登录后的Cookie（如需）"
}

response = requests.get(url, params=params, headers=headers)
data = response.json()  # 解析JSON数据
comments = data['data']['list']
for comment in comments:
    if comment['score'] < 3:  # 假设3分以下为差评
        print(comment['content'])