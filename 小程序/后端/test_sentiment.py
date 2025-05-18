import sys
import os
import logging

# 设置日志
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])

# 确保能够导入app模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入情感分析功能
from app.utils.sentiment_analysis import analyze_sentiment

def main():
    """测试情感分析功能"""
    print("开始测试情感分析功能...")
    
    # 测试正面评价
    positive_text = "这次旅行真的太棒了！景色优美，服务一流，我非常喜欢这里！"
    print(f"正面文本: {positive_text}")
    positive_result = analyze_sentiment(positive_text)
    print(f"分析结果: {positive_result}")
    
    # 测试负面评价
    negative_text = "这个景点特别差，环境脏乱，价格还贵，千万不要来！"
    print(f"负面文本: {negative_text}")
    negative_result = analyze_sentiment(negative_text)
    print(f"分析结果: {negative_result}")
    
    print("情感分析测试完成。")

if __name__ == "__main__":
    main() 