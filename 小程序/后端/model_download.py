from  transformers import BertTokenizer,BertForSequenceClassification
 
model_name="google-bert/bert-base-chinese"
cache_dir="model/bert-base-chinese"
 
#下载模型
BertForSequenceClassification.from_pretrained(model_name,cache_dir=cache_dir)
#下载分词工具
BertTokenizer.from_pretrained(model_name,cache_dir=cache_dir)
 
print(f"模型分词器已下载到：{cache_dir}")