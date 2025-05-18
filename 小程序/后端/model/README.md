# BERT 评论情感分析模型

本项目使用预训练的中文 BERT 模型对旅游景点评论进行情感分析，将评论分类为积极和消极两种情感。

## 环境要求

- Python 3.7+
- PyTorch 1.7+
- Transformers 4.0+
- pandas
- numpy
- scikit-learn
- tqdm

安装依赖：

```bash
pip install torch transformers pandas numpy scikit-learn tqdm
```

## 文件结构

```
后端/
  ├── data/
  │    ├── raw/              # 原始数据
  │    │    ├── All_attraction.csv   # 原始评论数据
  │    │    └── process.py    # 数据清洗脚本
  │    └── processed/        # 处理后的数据
  │         └── cleaned_attraction.csv  # 清洗后的评论数据
  └── model/
       ├── bert-base-chinese/  # 预训练的中文BERT模型
       ├── output/             # 训练后的模型输出
       │    ├── bert_model/    # 保存的模型
       │    └── training_stats.json  # 训练统计信息
       ├── train_bert.py       # 模型训练脚本
       ├── predict.py          # 模型预测脚本
       ├── training.log        # 训练日志
       └── README.md           # 说明文档
```

## 数据处理

原始数据包含旅游景点的评论，通过`process.py`脚本进行清洗，去除表情符号、标点符号和多余空格，以便于 BERT 模型的训练。

清洗数据：

```bash
cd 后端/data/raw
python process.py
```

## 模型训练

使用`train_bert.py`脚本训练 BERT 模型：

```bash
cd 后端/model
python train_bert.py --data_path ../data/processed/cleaned_attraction.csv --output_dir ./output
```

参数说明：

- `--data_path`: 处理后的 CSV 数据路径
- `--model_path`: 预训练模型路径（默认：./bert-base-chinese）
- `--output_dir`: 输出目录（默认：./output）
- `--max_length`: 最大序列长度（默认：128）
- `--batch_size`: 批次大小（默认：16）
- `--epochs`: 训练轮数（默认：10）
- `--learning_rate`: 学习率（默认：5e-5）
- `--weight_decay`: 权重衰减（默认：0.01）
- `--max_grad_norm`: 梯度裁剪最大范数（默认：1.0）
- `--warmup_proportion`: 学习率预热比例（默认：0.1）
- `--seed`: 随机种子（默认：42）
- `--tensorboard`: 启用 TensorBoard 记录训练和验证指标
- `--visualize_embeddings`: 在 TensorBoard 中可视化词嵌入（需要同时指定 --tensorboard）
- `--gpu_memory_cleanup`: 在训练后清理 GPU 显存缓存，有助于解决 OOM 问题
- `--early_stopping`: 启用早停策略，在验证损失不再显著改善时停止训练
- `--min_improvement`: 早停最小改善阈值（默认：0.001）
- `--class_weights`: 启用类别权重，对不平衡类别自动分配权重
- `--balance_data`: 平衡数据集，确保各类别样本数量相近

### 解决训练问题的建议

如果您在训练过程中遇到问题（如验证准确率不变、学习率下降过快等），可以尝试以下方法：

```bash
# 平衡训练数据，使用权重适应类别不平衡问题
python train_bert.py --balance_data --class_weights --tensorboard

# 使用更慢的学习率衰减和预热
python train_bert.py --learning_rate 2e-5 --warmup_proportion 0.2 --tensorboard

# 启用早停以避免过拟合
python train_bert.py --early_stopping --min_improvement 0.0005 --tensorboard

# 使用更合适的批次大小和训练轮数
python train_bert.py --batch_size 8 --epochs 15 --tensorboard
```

### 在 GPU 环境下的优化

在使用 GPU 训练时，可以考虑以下优化措施：

```bash
# 使用较小的批次大小以减少GPU内存占用
python train_bert.py --batch_size 4 --tensorboard --gpu_memory_cleanup

# 如果仍然遇到内存问题，可以减小最大序列长度
python train_bert.py --batch_size 4 --max_length 64 --tensorboard --gpu_memory_cleanup

# 对于大数据集，关闭嵌入可视化可以节省内存
python train_bert.py --tensorboard --gpu_memory_cleanup
```

### 使用 TensorBoard 监控训练过程

如果启用了 TensorBoard，您可以使用以下命令查看训练过程中的各项指标：

```bash
cd 后端/model
tensorboard --logdir=./output/tensorboard_logs
```

TensorBoard 可以显示以下指标：

- 训练损失（Training Loss）
- 验证损失（Validation Loss）
- 验证准确率（Validation Accuracy）
- 学习率变化（Learning Rate）
- 精确率、召回率和 F1 值（Precision, Recall, F1）
- 混淆矩阵（通过日志查看）
- 词嵌入可视化（如果启用了 --visualize_embeddings）

执行上述命令后，在浏览器中访问 http://localhost:6006 即可查看 TensorBoard 仪表板。

## 模型预测

使用`predict.py`脚本进行评论情感预测：

### 单条文本预测

```bash
cd 后端/model
python predict.py --model_path ./output/bert_model --text "这个景点真的很美，值得一去"
```

### 批量预测

```bash
cd 后端/model
python predict.py --model_path ./output/bert_model --batch_file ./texts.txt --output_file ./predictions.json
```

参数说明：

- `--model_path`: 训练好的模型路径
- `--text`: 要预测的单条文本
- `--batch_file`: 包含多条文本的文件路径（每行一条）
- `--output_file`: 预测结果输出文件路径

## 注意事项

1. 模型训练需要较大内存和计算资源，建议在 GPU 环境下训练
2. 首次运行时会自动下载 BERT 预训练模型（如果不存在）
3. 对于长文本，模型会截断到最大长度 128 个 token
4. 预测结果包含情感标签和置信度，可用于后续分析

## 情感标签映射

- 0: 消极
- 1: 积极
