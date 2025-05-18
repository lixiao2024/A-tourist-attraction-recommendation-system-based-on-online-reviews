import pandas as pd
import re
import os

# 定义文件路径
good_comments_path = "ctrip_comment_shanghai/东方明珠/东方明珠好评.csv"
bad_comments_path = "ctrip_comment_shanghai/东方明珠/东方明珠差评.csv"
output_path = "ctrip_comment_shanghai/merged_dongfangmingzhu.csv"

# 读取CSV文件
print("正在读取CSV文件...")
try:
    good_comments = pd.read_csv(good_comments_path, encoding='GBK')
    bad_comments = pd.read_csv(bad_comments_path, encoding='GBK')
except UnicodeDecodeError:
    print("尝试使用GB18030编码...")
    good_comments = pd.read_csv(good_comments_path, encoding='GB18030')
    bad_comments = pd.read_csv(bad_comments_path, encoding='GB18030')

# 添加评论类型列
good_comments['comment_type'] = '好评'
bad_comments['comment_type'] = '差评'

# 合并数据
print("正在合并数据...")
merged_comments = pd.concat([good_comments, bad_comments], ignore_index=True)

# 定义文本清洗函数
def clean_text(text):
    if pd.isna(text):
        return ""
    
    # 转为字符串类型
    text = str(text)
    
    # 去除HTML标签
    text = re.sub(r'<.*?>', '', text)
    
    # 去除URL
    text = re.sub(r'http[s]?://\S+', '', text)
    
    # 只保留中文字符、英文字母和数字，去除所有标点符号和特殊字符
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9]', '', text)
    
    # 去除多余空格
    text = re.sub(r'\s+', ' ', text)
    
    # 去除换行符
    text = text.replace('\n', '').replace('\r', '')
    
    return text.strip()

# 处理content_wrap列（评论内容）
print("正在清洗评论文本...")
merged_comments['cleaned_content'] = merged_comments['content_wrap'].apply(clean_text)

# 保存处理后的数据到新的CSV文件
print("正在保存合并后的数据...")
merged_comments.to_csv(output_path, index=False, encoding='utf-8')

print(f"数据处理完成，合并后的文件已保存到: {output_path}")
print(f"共处理 {len(merged_comments)} 条评论，其中好评 {len(good_comments)} 条，差评 {len(bad_comments)} 条")

# 显示处理后数据样例
print("\n数据样例:")
print(merged_comments[['user_detail_name', 'comment_type', 'cleaned_content']].head())
