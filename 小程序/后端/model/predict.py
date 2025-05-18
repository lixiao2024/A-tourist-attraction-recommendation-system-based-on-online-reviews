import os
import torch
import argparse
import numpy as np
from transformers import BertTokenizer, BertForSequenceClassification

def predict_sentiment(text, model, tokenizer, max_length=128, device=None):
    """使用训练好的模型预测文本情感"""
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 转为模型输入格式
    encoding = tokenizer(
        text,
        add_special_tokens=True,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    
    # 移到设备上
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    
    # 设置模型为评估模式
    model.eval()
    
    # 不计算梯度
    with torch.no_grad():
        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask
        )
    
    # 获取预测结果
    logits = outputs.logits
    probs = torch.nn.functional.softmax(logits, dim=1)
    predicted_class = torch.argmax(probs, dim=1).item()
    
    # 获取每个类别的概率
    probs = probs.cpu().numpy()[0]
    
    # 映射类别到情感标签
    sentiment_labels = {0: "消极", 1: "积极"}
    predicted_sentiment = sentiment_labels.get(predicted_class, "未知")
    
    result = {
        'text': text,
        'sentiment': predicted_sentiment,
        'sentiment_id': predicted_class,
        'confidence': float(probs[predicted_class]),
        'probabilities': {sentiment_labels.get(i, f"类别 {i}"): float(prob) for i, prob in enumerate(probs)}
    }
    
    return result

def load_model(model_path):
    """加载预训练模型和分词器"""
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 加载分词器和模型
    tokenizer = BertTokenizer.from_pretrained(model_path)
    model = BertForSequenceClassification.from_pretrained(model_path)
    
    # 将模型移到设备上
    model.to(device)
    
    return model, tokenizer, device

def batch_predict(texts, model, tokenizer, max_length=128, batch_size=32, device=None):
    """批量预测多个文本的情感"""
    if device is None:
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    results = []
    
    # 分批处理
    for i in range(0, len(texts), batch_size):
        batch_texts = texts[i:i+batch_size]
        
        # 为整个批次编码
        encodings = tokenizer(
            batch_texts,
            add_special_tokens=True,
            max_length=max_length,
            padding='max_length',
            truncation=True,
            return_tensors='pt'
        )
        
        # 移到设备上
        input_ids = encodings['input_ids'].to(device)
        attention_mask = encodings['attention_mask'].to(device)
        
        # 设置模型为评估模式
        model.eval()
        
        # 不计算梯度
        with torch.no_grad():
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )
        
        # 获取预测结果
        logits = outputs.logits
        probs = torch.nn.functional.softmax(logits, dim=1)
        predicted_classes = torch.argmax(probs, dim=1).cpu().numpy()
        
        # 获取每个类别的概率
        probs = probs.cpu().numpy()
        
        # 映射类别到情感标签
        sentiment_labels = {0: "消极", 1: "积极"}
        
        # 构建结果
        for j, text in enumerate(batch_texts):
            predicted_class = predicted_classes[j]
            predicted_sentiment = sentiment_labels.get(predicted_class, "未知")
            
            result = {
                'text': text,
                'sentiment': predicted_sentiment,
                'sentiment_id': int(predicted_class),
                'confidence': float(probs[j][predicted_class]),
                'probabilities': {sentiment_labels.get(i, f"类别 {i}"): float(prob) for i, prob in enumerate(probs[j])}
            }
            
            results.append(result)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="使用BERT模型进行评论情感分析预测")
    parser.add_argument("--model_path", type=str, default="./output/bert_model", help="训练好的模型路径")
    parser.add_argument("--text", type=str, help="要预测的文本")
    parser.add_argument("--batch_file", type=str, help="包含多个文本的文件路径，每行一个文本")
    parser.add_argument("--output_file", type=str, help="输出预测结果的文件路径")
    
    args = parser.parse_args()
    
    # 加载模型
    model_path = args.model_path
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.model_path)
    
    model, tokenizer, device = load_model(model_path)
    print(f"模型已加载，使用设备: {device}")
    
    # 单个文本预测
    if args.text:
        result = predict_sentiment(args.text, model, tokenizer, device=device)
        print(f"文本: {result['text']}")
        print(f"情感: {result['sentiment']} (置信度: {result['confidence']:.4f})")
        print("各类别概率:")
        for label, prob in result['probabilities'].items():
            print(f"  {label}: {prob:.4f}")
    
    # 批量预测
    if args.batch_file:
        if os.path.exists(args.batch_file):
            with open(args.batch_file, 'r', encoding='utf-8') as f:
                texts = [line.strip() for line in f if line.strip()]
            
            if texts:
                print(f"开始批量预测 {len(texts)} 条文本...")
                results = batch_predict(texts, model, tokenizer, device=device)
                
                # 显示前5个结果
                for i, result in enumerate(results[:5]):
                    print(f"\n[{i+1}] 文本: {result['text'][:50]}..." if len(result['text']) > 50 else result['text'])
                    print(f"情感: {result['sentiment']} (置信度: {result['confidence']:.4f})")
                
                # 保存结果
                if args.output_file:
                    import json
                    with open(args.output_file, 'w', encoding='utf-8') as f:
                        json.dump(results, f, ensure_ascii=False, indent=2)
                    print(f"预测结果已保存到 {args.output_file}")
            else:
                print("文件为空或没有有效文本")
        else:
            print(f"文件不存在: {args.batch_file}")

if __name__ == "__main__":
    main() 