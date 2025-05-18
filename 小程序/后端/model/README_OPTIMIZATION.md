# BERT 情感分析模型训练优化

本文档说明了对 BERT 情感分析模型训练流程的优化改进，解决了训练损失波动和收敛慢的问题。

## 优化内容

### 1. 训练稳定性优化

- **损失平滑显示**：使用移动平均方法平滑训练损失显示，减少视觉上的波动
- **梯度累积**：默认设置为 4 步梯度累积，相当于将批次大小扩大 4 倍而不增加内存占用
- **降低学习率**：将学习率从 5e-5 降低到 2e-5，减少参数更新幅度
- **学习率预热**：保持预热比例为 0.15，在训练开始阶段稳定学习过程
- **梯度裁剪**：保持梯度裁剪阈值为 0.5，防止梯度爆炸
- **优化器配置**：微调 AdamW 优化器参数，增加数值稳定性

### 2. 训练效率优化

- **余弦退火调度**：使用余弦退火学习率调度，在后期更平缓地降低学习率
- **早停与耐心**：加入基于验证损失的早停机制，有 3 轮容忍度
- **限制 TensorBoard 记录频率**：降低记录频率，减少磁盘 I/O 和视觉波动

### 3. 模型性能优化

- **保存最佳模型**：根据验证损失保存训练过程中的最佳模型，而不是最后一个 checkpoint
- **类别权重**：使用类别权重处理数据不平衡问题，同时解决了 JSON 序列化错误
- **训练曲线可视化**：添加训练和验证损失、准确率曲线的可视化，帮助分析模型性能

## 如何使用

我们提供了运行优化训练的脚本：

### Windows 系统

直接双击运行`train_sentiment.bat`批处理文件，或在命令行中运行：

```
train_sentiment.bat
```

### Linux/macOS 系统

首先给脚本添加执行权限：

```bash
chmod +x train_sentiment.sh
```

然后运行：

```bash
./train_sentiment.sh
```

### 自定义参数

如果需要使用自定义参数，可以直接使用 Python 命令：

```bash
python train_bert.py \
  --data_path="你的数据路径.csv" \
  --output_dir="./输出目录" \
  --batch_size=16 \
  --gradient_accumulation_steps=4 \
  --learning_rate=2e-5 \
  --epochs=10 \
  --tensorboard \
  --early_stopping \
  --patience=3 \
  --slow_decay \
  --class_weights
```

## 新增参数说明

| 参数                            | 说明                                     | 默认值 |
| ------------------------------- | ---------------------------------------- | ------ |
| `--gradient_accumulation_steps` | 梯度累积步数，用于模拟更大批次           | 4      |
| `--tensorboard_logging_freq`    | TensorBoard 记录频率(每多少批次记录一次) | 10     |
| `--patience`                    | 早停耐心值，验证损失多少轮未改善则停止   | 3      |
| `--slow_decay`                  | 使用余弦退火学习率调度                   | 启用   |

## 训练监控

训练开始后，可以使用 TensorBoard 查看训练进度：

```bash
tensorboard --logdir=./output/optimized/tensorboard_logs
```

然后在浏览器中访问 http://localhost:6006

## 结果对比

优化前：

- 训练损失曲线波动较大
- 验证损失下降较慢
- 提前过拟合

优化后：

- 训练损失曲线平滑
- 验证损失稳定下降
- 收敛速度更快
- 最终模型性能更好

## 注意事项

1. 如果 GPU 内存不足，可以减小`batch_size`并增加`gradient_accumulation_steps`
2. 如果数据集较小，可能需要减少`epochs`数量，增加`early_stopping`的敏感度
3. 类别权重对不平衡数据集特别有用，如果数据集已经平衡，可以移除`--class_weights`选项
