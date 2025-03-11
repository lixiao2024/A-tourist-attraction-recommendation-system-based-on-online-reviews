"""
@FileName：Batch_test.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 01 - 2025/1/27\n
"""
import re

import requests
from bs4 import BeautifulSoup

# 模拟浏览器
headers = {
    'cookie': 'GUID=09031116215023025465; nfes_isSupportWebP=1; nfes_isSupportWebP=1; UBT_VID=1737782107875.b5c4RKpvwiq3; MKT_CKID=1737782108470.sg5tk.o53x; _RSG=peaXFI8L380oO_9..cceWA; _RDG=286d43e1517b43201638547ad8a7c03815; _RGUID=02035484-8f86-4a33-a828-9a6fbe27f632; Hm_lvt_a8d6737197d542432f4ff4abc6e06384=1737964247; Hm_lpvt_a8d6737197d542432f4ff4abc6e06384=1737964247; HMACCOUNT=3235764F344DD52B; Union=OUID=&AllianceID=4902&SID=22921635&SourceID=&createtime=1737964247&Expires=1738569047372; MKT_OrderClick=ASID=490222921635&AID=4902&CSID=22921635&OUID=&CT=1737964247375&CURL=https%3A%2F%2Fwww.ctrip.com%2F%3Fallianceid%3D4902%26sid%3D22921635%26msclkid%3D10b184c73589182588dbe3500f5bcfcf%26keywordid%3D82327063055689&VAL={"pc_vid":"1737782107875.b5c4RKpvwiq3"}; Hm_lvt_e4211314613fcf074540918eb10eeecb=1737782108,1737964251; ASP.NET_SessionSvc=MTAuNjEuMjIuMjQ0fDkwOTB8amlucWlhb3xkZWZhdWx0fDE2NjYzNDk2NTM2OTM; _bfaStatusPVSend=1; _bfaStatus=send; MKT_Pagesource=H5; _RF1=42.56.134.103; Hm_lpvt_e4211314613fcf074540918eb10eeecb=1737967385; _jzqco=%7C%7C%7C%7C1737964247597%7C1.1793697365.1737782108473.1737967279372.1737967385234.1737967279372.1737967385234.undefined.0.0.13.13; _ubtstatus=%7B%22vid%22%3A%221737782107875.b5c4RKpvwiq3%22%2C%22sid%22%3A3%2C%22pvid%22%3A46%2C%22pid%22%3A%22214070%22%7D; _bfa=1.1737782107875.b5c4RKpvwiq3.1.1737967395479.1737967395793.3.47.10650064020; _pd=%7B%22_o%22%3A64%2C%22s%22%3A984%2C%22_s%22%3A9%7D',  # 需要填写真实的cookie
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Mobile Safari/537.36',
}

# 假设这是包含多个景点的城市页面
url = 'https://gs.ctrip.com/html5/you/sight/beijing1/'

# 发送请求获取页面内容
response = requests.get(url, headers=headers)

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 假设每个景点的链接包含在 <a> 标签中，并且有 businessId 参数
# 你可以根据页面的实际结构调整这个选择器
links = soup.find_all('a', href=True)

# 提取每个景点的 businessId（假设 businessId 是 URL 中的一部分）
business_ids = []
for link in links:
    href = link['href']
    if 'businessId' in href:
        # 提取 businessId
        # 假设 URL 中的 businessId 格式为 ?businessId=数字，例如 ?businessId=229
        match = re.search(r'businessId=(\d+)', href)
        if match:
            business_ids.append(match.group(1))

# 打印提取出的 businessId 列表
print(business_ids)