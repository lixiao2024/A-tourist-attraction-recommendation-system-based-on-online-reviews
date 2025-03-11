"""
@FileName：ctrip.comment.py\n
@Description：爬虫\n
@Author：Surely\n
@Time： 2025 - 01 - 2025/1/24\n
"""
#导入请求模块
import requests
from bs4 import BeautifulSoup
import json
# 模拟浏览器
headers = {
    # cookie 用户信息， 常用于检测是否有登陆账号
    'cookie' : 'GUID=09031116215023025465; nfes_isSupportWebP=1; UBT_VID=1737782107875.b5c4RKpvwiq3; MKT_CKID=1737782108470.sg5tk.o53x; _RF1=42.56.135.1; _RSG=peaXFI8L380oO_9..cceWA; _RDG=286d43e1517b43201638547ad8a7c03815; _RGUID=02035484-8f86-4a33-a828-9a6fbe27f632; _jzqco=%7C%7C%7C%7C1737782108639%7C1.1793697365.1737782108473.1737782108473.1737782108473.1737782108473.1737782108473.0.0.0.1.1; MKT_Pagesource=H5; Union=OUID=&AllianceID=66672&SID=1693366&SourceID=&AppID=&OpenID=&exmktID=&createtime=1737782119&Expires=1738386919279; _resDomain=https%3A%2F%2Fws-s.tripcdn.cn; _pd=%7B%22_o%22%3A1%2C%22s%22%3A4%2C%22_s%22%3A1%7D; _bfa=1.1737782107875.b5c4RKpvwiq3.1.1737782155448.1737782236622.1.4.214070',
    # user-agent 用户代理，表示浏览器/设备基本身份信息
    'user-agent' : 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36'

}
# 请求网址
url = 'https://m.ctrip.com/webapp/you/commentWeb/commentList?businessId=229&businessType=11&noJumpApp=yes&from=https%3A%2F%2Fgs.ctrip.com%2Fhtml5%2Fyou%2Fsight%2Fbeijing1%2F229.html%3FrenderPlatform%3D%26seo%3D1'




# 发送请求 使用第三方模块request
response = requests.get(url = url,headers = headers)

# 获取响应的json数据
# json_data = response.json()
# print(json_data)

#print(response.text)  # 打印返回的HTML内容
# 使用 BeautifulSoup 解析 HTML
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

        # 打印 JSON 数据（你可以根据需要进行进一步处理）
        #print(json_data)

        # 假设评论数据在 json_data 中的一个特定字段，例如评论列表可能在 'props' -> 'pageProps' -> 'comments' 里
        comments = json_data.get('props', {}).get('pageProps', {}).get('initialState', {}).get('commentList', [])

        for comment in comments:
            print(comment.get('content', 'No Content'))  # 打印每条评论内容

    except json.JSONDecodeError:
        print("JSON 解码失败")
else:
    print("没有找到包含评论的 <script> 标签")
