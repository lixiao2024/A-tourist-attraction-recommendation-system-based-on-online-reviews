import os
import torch
from predict import load_model, predict_sentiment

def test_model():
    # 模型路径
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    # 加载模型
    print("正在加载模型...")
    model, tokenizer, device = load_model(model_path)
    print(f"模型已加载，使用设备: {device}")
    
    # 测试文本列表
    test_texts = [
        "这个景点非常美丽，风景如画，服务也很周到，强烈推荐！",
        "整体来说不错，但是人太多了，排队时间长。",
        "景点很差，环境脏乱，价格还贵，完全不值得。",
        "虽然交通不是很方便，但是景色确实令人惊叹，值得一去。",
        "门票太贵了，里面没什么特别的，就是个普通公园。"
    ]
    
    # 逐个进行预测
    print("\n===== 测试结果 =====")
    for text in test_texts:
        result = predict_sentiment(text, model, tokenizer, device=device)
        print(f"\n文本: {result['text']}")
        print(f"情感: {result['sentiment']} (置信度: {result['confidence']:.4f})")
        print("各类别概率:")
        for label, prob in result['probabilities'].items():
            print(f"  {label}: {prob:.4f}")
    
    # 用户自定义输入测试
    while True:
        user_input = input("\n请输入要测试的文本 (输入'退出'结束): ")
        if user_input.lower() in ['退出', 'exit', 'quit', 'q']:
            break
        
        if user_input.strip():
            result = predict_sentiment(user_input, model, tokenizer, device=device)
            print(f"\n文本: {result['text']}")
            print(f"情感: {result['sentiment']} (置信度: {result['confidence']:.4f})")
            print("各类别概率:")
            for label, prob in result['probabilities'].items():
                print(f"  {label}: {prob:.4f}")

if __name__ == "__main__":
    test_model() 