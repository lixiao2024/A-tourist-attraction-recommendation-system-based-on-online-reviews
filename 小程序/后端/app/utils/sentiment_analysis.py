import os
import torch
from transformers import BertForSequenceClassification, BertTokenizer
import logging
import sys

# 设置日志
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置为DEBUG级别
# 确保日志处理器已设置
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# 模型路径
MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "model", "output")
logger.debug(f"模型路径: {MODEL_PATH}")

# 全局变量用于存储加载的模型和分词器
model = None
tokenizer = None

def load_model():
    """
    加载BERT模型和分词器
    """
    global model, tokenizer
    
    try:
        # 如果模型已经加载，则直接返回
        if model is not None and tokenizer is not None:
            logger.debug("模型已加载，直接使用")
            return model, tokenizer
        
        logger.debug(f"开始加载模型，路径: {MODEL_PATH}")
        
        # 检查模型文件是否存在
        if not os.path.exists(MODEL_PATH):
            logger.error(f"模型路径不存在: {MODEL_PATH}")
            raise FileNotFoundError(f"模型路径不存在: {MODEL_PATH}")
        
        files = os.listdir(MODEL_PATH)
        logger.debug(f"模型目录文件列表: {files}")
        
        # 加载分词器
        logger.debug("开始加载分词器")
        tokenizer = BertTokenizer.from_pretrained(MODEL_PATH)
        
        # 加载模型
        logger.debug("开始加载BERT模型")
        model = BertForSequenceClassification.from_pretrained(MODEL_PATH)
        model.eval()  # 设置为评估模式
        
        logger.info("情感分析模型加载成功")
        return model, tokenizer
    
    except Exception as e:
        logger.error(f"加载情感分析模型失败: {str(e)}", exc_info=True)
        raise RuntimeError(f"无法加载情感分析模型: {str(e)}")

def analyze_sentiment(text):
    """
    对输入文本进行情感分析
    
    参数:
        text (str): 要分析的文本内容
    
    返回:
        str: 'positive', 'negative' 或 'neutral'
    """
    try:
        logger.debug(f"开始分析文本情感: {text[:100]}...") 
        
        # 加载模型和分词器
        model, tokenizer = load_model()
        
        # 对文本进行分词和编码
        logger.debug("对文本进行分词和编码")
        inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512, padding=True)
        
        # 进行模型推理
        logger.debug("开始模型推理")
        with torch.no_grad():
            outputs = model(**inputs)
        
        # 获取预测结果
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1).item()
        
        # 根据配置文件，映射类别ID到标签
        # 假设0是negative，1是neutral，2是positive
        sentiment_map = {
            0: "negative",
            1: "neutral",
            2: "positive"
        }
        
        result = sentiment_map.get(predicted_class, "neutral")
        logger.debug(f"情感分析结果: {result}, 预测类别: {predicted_class}")
        return result
    
    except Exception as e:
        logger.error(f"情感分析过程中出错: {str(e)}", exc_info=True)
        # 如果分析失败，返回默认值
        return "neutral" 