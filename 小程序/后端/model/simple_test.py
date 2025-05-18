import os
import torch
from predict import load_model, predict_sentiment

def main():
    # 模型路径
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    
    # 加载模型
    print("正在加载模型...")
    model, tokenizer, device = load_model(model_path)
    print(f"模型已加载，使用设备: {device}")
    
    # 用户输入测试
    print("\n请输入旅游景点评论，模型将判断是好评还是差评")
    user_input = input(">>> ")
    
    if user_input.strip():
        result = predict_sentiment(user_input, model, tokenizer, device=device)
        print(f"\n您的评论: {result['text']}")
        print(f"情感分析结果: {result['sentiment']} (置信度: {result['confidence']:.4f})")
        print("各类别概率:")
        for label, prob in result['probabilities'].items():
            print(f"  {label}: {prob:.4f}")

if __name__ == "__main__":
    main() 