import pandas as pd
import re
import os
import sys
import unicodedata

def clean_text(text):
    if not isinstance(text, str):
        return ""
    
    # 第一步：标准化Unicode字符（将组合字符分解）
    text = unicodedata.normalize('NFKD', text)
    
    # 第二步：移除所有控制字符
    text = re.sub(r'[\x00-\x1F\x7F-\x9F]', '', text)
    
    # 第三步：移除所有表情符号（更全面的范围）
    # 基本表情符号和符号
    emoji_pattern = re.compile(
        "["
        "\U0001F100-\U0001F1FF"  # 国旗和符号
        "\U0001F300-\U0001F5FF"  # 符号和象形文字
        "\U0001F600-\U0001F64F"  # 表情符号
        "\U0001F680-\U0001F6FF"  # 交通和地图符号
        "\U0001F700-\U0001F77F"  # 符号
        "\U0001F780-\U0001F7FF"  # 几何符号
        "\U0001F800-\U0001F8FF"  # 杂项符号
        "\U0001F900-\U0001F9FF"  # 补充符号和象形文字
        "\U0001FA00-\U0001FA6F"  # 扩展符号和象形文字
        "\U0001FA70-\U0001FAFF"  # 扩展符号
        "\U00002702-\U000027B0"  # 装饰符号
        "\U000024C2-\U0001F251"  # 装饰字符
        "\U0001F004"             # 麻将牌
        "\U0001F0CF"             # 扑克牌
        "]+", flags=re.UNICODE
    )
    text = emoji_pattern.sub('', text)
    
    # 移除所有非ASCII符号和所有标点符号（包括中文标点）
    # 保留字母、数字和中文字符
    text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s]', '', text)
    
    # 移除多余空格（包括全角空格）
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\u3000', ' ', text)  # 全角空格
    text = text.strip()
    
    return text

def main():
    input_path = os.path.join(os.path.dirname(__file__), 'All_attraction.csv')
    output_path = os.path.join(os.path.dirname(__file__), '../processed/cleaned_attraction.csv')
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    print(f"正在读取CSV文件: {input_path}")
    
    # 尝试不同的编码格式
    encodings = ['utf-8', 'gb18030', 'gbk', 'gb2312']
    df = None
    
    for encoding in encodings:
        try:
            print(f"尝试使用 {encoding} 编码读取...")
            df = pd.read_csv(input_path, encoding=encoding)
            print(f"成功使用 {encoding} 编码读取文件")
            break
        except Exception as e:
            print(f"{encoding} 编码读取失败: {str(e)}")
    
    if df is None:
        print("所有编码尝试均失败，无法读取文件")
        sys.exit(1)
    
    # 检查是否存在content_wrap列
    if 'content_wrap' not in df.columns:
        print(f"CSV文件中不存在'content_wrap'列。可用列: {df.columns.tolist()}")
        sys.exit(1)
    
    print(f"开始清洗数据，总共 {len(df)} 条评论...")
    
    # 清洗数据
    df['cleaned_content'] = df['content_wrap'].apply(clean_text)
    
    # 移除清洗后为空的行
    df_filtered = df[df['cleaned_content'].str.strip().str.len() > 0].copy()
    print(f"过滤后的评论数: {len(df_filtered)}")
    
    # 打印几个样本进行检查
    print("\n清洗前后对比样本（前5条）:")
    for i, (orig, cleaned) in enumerate(zip(df['content_wrap'].head(5), df['cleaned_content'].head(5))):
        print(f"样本 {i+1}:")
        print(f"原始: {orig}")
        print(f"清洗后: {cleaned}")
        print("-" * 50)
    
    # 保存清洗后的数据
    print(f"正在保存清洗后的数据到: {output_path}")
    df.to_csv(output_path, index=False, encoding='utf-8')
    
    print(f"数据清洗完成！清洗后的数据保存在: {output_path}")
    print(f"原始评论数: {len(df)}")
    print(f"清洗后非空评论数: {df['cleaned_content'].str.strip().str.len().gt(0).sum()}")

if __name__ == "__main__":
    main()
