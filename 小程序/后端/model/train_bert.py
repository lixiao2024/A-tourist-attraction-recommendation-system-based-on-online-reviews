import os
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from torch.optim import AdamW
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import get_linear_schedule_with_warmup, get_cosine_schedule_with_warmup
from sklearn.model_selection import train_test_split
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import precision_recall_fscore_support, confusion_matrix
from collections import Counter
import argparse
import logging
import gc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from tqdm import tqdm
import json
import re
from torch.utils.tensorboard import SummaryWriter
import datetime

# 确保日志目录存在
os.makedirs("./logs", exist_ok=True)

# 设置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("./logs/training.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 使用纯英文配置，确保在各环境都能正常显示
plt.rcParams['font.family'] = 'DejaVu Sans'
# 不使用特定中文字体，防止字体缺失警告
# 可选的设置是使用系统的默认字体
# plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

class CommentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length
    
    def __len__(self):
        return len(self.texts)
    
    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]
        
        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def load_data(csv_path):
    """加载CSV数据并准备训练数据"""
    try:
        # 尝试不同的编码方式读取CSV
        encodings = ['utf-8', 'gb18030', 'gbk', 'gb2312']
        for encoding in encodings:
            try:
                df = pd.read_csv(csv_path, encoding=encoding)
                logger.info(f"成功使用{encoding}编码读取CSV")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError(f"无法以支持的编码读取CSV文件: {csv_path}")
        
        logger.info(f"加载了 {len(df)} 条数据")
        logger.info(f"数据列: {df.columns.tolist()}")
        
        # 确保列名小写，避免大小写问题
        df.columns = [col.lower() for col in df.columns]
        
        # 检查是否有评论内容列
        content_column = None
        for col in ['cleaned_content', 'content', 'review', 'comment', '评论', '内容']:
            if col in df.columns:
                content_column = col
                break
        
        if content_column is None:
            # 如果找不到内容列，假设最后一列是内容
            content_column = df.columns[-1]
            logger.warning(f"找不到明确的内容列，使用最后一列 '{content_column}' 作为内容")
        
        # 检查是否有标签列
        label_column = None
        for col in ['text', 'label', 'star', 'rating', 'score', '评分', '标签']:
            if col in df.columns:
                label_column = col
                break
        
        if label_column is None:
            # 如果找不到标签列，假设第一列是标签
            label_column = df.columns[0]
            logger.warning(f"找不到明确的标签列，使用第一列 '{label_column}' 作为标签")
        
        logger.info(f"使用 '{content_column}' 作为内容列，'{label_column}' 作为标签列")
        
        # 提取标签
        df['label_numeric'] = 0  # 默认为消极
        
        # 处理标签列
        def extract_score(text):
            if not isinstance(text, str):
                # 如果不是字符串，尝试直接作为数字解析
                try:
                    num = float(text)
                    if num >= 3:
                        return 1  # 积极
                    else:
                        return 0  # 消极
                except:
                    return 1  # 默认积极
            
            # 尝试从文本中提取数字评分
            patterns = [
                r'([1-5])(?:星|分|级)',  # 中文评分格式：3星、4分、5级
                r'([1-5])(?:\.0)?\/5',   # 英文格式：4/5、3.0/5
                r'([1-5])(?:\.0)?'       # 纯数字格式：4、4.0
            ]
            
            for pattern in patterns:
                match = re.search(pattern, text)
                if match:
                    score = int(match.group(1))
                    if score >= 3:
                        return 1  # 积极
                    else:
                        return 0  # 消极
            
            # 用情感关键词判断
            positive_words = ['好', '棒', '赞', '喜欢', '推荐', '满意', '优秀', '美', '舒适', '精彩']
            negative_words = ['差', '烂', '糟', '失望', '不推荐', '不满', '遗憾', '后悔', '不好', '不行']
            
            text_lower = text.lower()
            if any(word in text_lower for word in positive_words):
                return 1  # 积极
            elif any(word in text_lower for word in negative_words):
                return 0  # 消极
            
            # 最后默认为积极
            return 1
        
        df['label_numeric'] = df[label_column].apply(extract_score)
        
        # 输出标签分布
        logger.info(f"标签分布: {df['label_numeric'].value_counts().to_dict()}")
        
        # 移除空评论
        df = df[df[content_column].notna() & (df[content_column].astype(str) != '')]
        logger.info(f"处理后剩余 {len(df)} 条有效数据")
        
        texts = df[content_column].astype(str).tolist()
        labels = df['label_numeric'].tolist()
        
        # 确保有足够的两类样本
        if len(set(labels)) < 2:
            logger.warning(f"标签类别少于2类，当前只有{len(set(labels))}类")
        
        # 输出一些样例以便检查
        logger.info("数据样例:")
        for i in range(min(3, len(texts))):
            logger.info(f"内容: {texts[i][:50]}...，标签: {labels[i]}")
        
        return texts, labels
    
    except Exception as e:
        logger.error(f"加载数据时出错: {str(e)}")
        raise

def train_model(model, train_dataloader, val_dataloader, args):
    """训练BERT模型"""
    # 初始化TensorBoard（如果启用）
    writer = None
    if args.tensorboard:
        # 创建更明确的日志目录
        timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        log_dir = os.path.join(args.output_dir, 'tensorboard_logs', f"run_{timestamp}")
        os.makedirs(log_dir, exist_ok=True)
        writer = SummaryWriter(log_dir=log_dir)
        logger.info(f"TensorBoard日志保存到: {log_dir}")
        
        # 记录基本训练信息到TensorBoard
        writer.add_text('Training/Info', f"批量大小: {args.batch_size}", 0)
        writer.add_text('Training/Info', f"学习率: {args.learning_rate}", 0)
        writer.add_text('Training/Info', f"训练轮数: {args.epochs}", 0)
        writer.add_text('Training/Info', f"预热比例: {args.warmup_proportion}", 0)
        writer.add_text('Training/Hyperparams', str(vars(args)), 0)
        
        try:
            # 尝试将超参数保存为文件
            param_file = os.path.join(log_dir, 'hyperparameters.txt')
            with open(param_file, 'w') as f:
                for key, value in vars(args).items():
                    f.write(f"{key}: {value}\n")
        except Exception as e:
            logger.warning(f"保存超参数时出错: {str(e)}")
        
        # 记录模型结构 - 使用try-except避免训练中断
        try:
            # 在GPU环境下跳过添加模型图，因为这会导致设备不一致问题
            if torch.cuda.is_available():
                logger.info("GPU环境下跳过添加模型图，以避免设备不一致问题")
            else:
                dummy_input = torch.zeros((1, args.max_length), dtype=torch.long)
                dummy_mask = torch.ones_like(dummy_input)
                writer.add_graph(model, [dummy_input, dummy_mask])
                logger.info("成功添加模型图到TensorBoard")
        except Exception as e:
            logger.warning(f"添加模型图到TensorBoard时出错，但训练将继续: {str(e)}")
    
    # 优化器 - 调整优化器配置
    no_decay = ['bias', 'LayerNorm.weight']
    optimizer_grouped_parameters = [
        {'params': [p for n, p in model.named_parameters() if not any(nd in n for nd in no_decay)],
         'weight_decay': args.weight_decay},
        {'params': [p for n, p in model.named_parameters() if any(nd in n for nd in no_decay)],
         'weight_decay': 0.0}
    ]
    
    # 使用AdamW优化器，添加eps参数防止数值不稳定
    optimizer = AdamW(optimizer_grouped_parameters, lr=args.learning_rate, eps=1e-8, betas=(0.9, 0.999))
    
    # 训练步数（考虑梯度累积）
    total_steps = len(train_dataloader) * args.epochs // args.gradient_accumulation_steps
    
    # 学习率调度器 - 使用更平缓的学习率调度
    warmup_steps = int(total_steps * args.warmup_proportion)
    
    # 如果启用了慢衰减，使用余弦退火调度
    if args.slow_decay:
        scheduler = get_cosine_schedule_with_warmup(
            optimizer,
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )
        logger.info(f"使用余弦退火学习率调度: 总步数: {total_steps}，预热步数: {warmup_steps}")
    else:
        scheduler = get_linear_schedule_with_warmup(
            optimizer, 
            num_warmup_steps=warmup_steps,
            num_training_steps=total_steps
        )
        logger.info(f"使用线性学习率调度: 总步数: {total_steps}，预热步数: {warmup_steps}")
    
    # 训练统计
    training_stats = []
    
    # 设置设备
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model.to(device)
    
    # 如果提供了类别权重，创建加权损失函数
    class_weights = None
    if hasattr(model, '_class_weights'):
        class_weights = model._class_weights
        logger.info(f"使用类别权重进行训练: {class_weights}")
    
    logger.info(f"开始训练，使用设备: {device}")
    
    # 用于记录全局训练步数
    global_step = 0
    best_accuracy = 0.0
    best_model_state = None
    patience_counter = 0
    best_val_loss = float('inf')
    
    # 用于平滑化损失显示的移动平均
    train_loss_moving_avg = None
    smoothing_factor = 0.9  # 平滑因子，值越高平滑效果越强
    
    # 记录训练指标的历史
    train_losses = []
    val_losses = []
    accuracies = []

    # 训练循环
    for epoch in range(args.epochs):
        logger.info(f"Epoch {epoch+1}/{args.epochs}")
        
        # 训练模式
        model.train()
        
        # 进度条
        progress_bar = tqdm(train_dataloader, desc=f"Epoch {epoch+1}")
        
        total_train_loss = 0
        epoch_steps = 0
        
        # 在每个epoch开始时重置梯度
        optimizer.zero_grad()
        
        # 用于抽样记录TensorBoard的计数器
        tb_logging_counter = 0
        
        for step, batch in enumerate(progress_bar):
            # 准备数据
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # 前向传播
            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )
            
            loss = outputs.loss
            
            # 如果使用类别权重，手动计算加权损失
            if class_weights is not None:
                # 获取logits并计算损失
                logits = outputs.logits
                log_probs = torch.nn.functional.log_softmax(logits, dim=-1)
                # 使用类别权重进行加权
                per_example_loss = -torch.sum(class_weights.unsqueeze(0) * log_probs * torch.nn.functional.one_hot(labels, num_classes=log_probs.size(-1)), dim=-1)
                loss = per_example_loss.mean()
            
            # 梯度累积: 将损失除以累积步数
            loss = loss / args.gradient_accumulation_steps
            
            # 反向传播
            loss.backward()
            
            # 记录未缩放的损失值用于显示
            display_loss = loss.item() * args.gradient_accumulation_steps
            total_train_loss += display_loss
            epoch_steps += 1
            
            # 应用移动平均平滑化损失显示
            if train_loss_moving_avg is None:
                train_loss_moving_avg = display_loss
            else:
                train_loss_moving_avg = smoothing_factor * train_loss_moving_avg + (1 - smoothing_factor) * display_loss
            
            # 仅在累积梯度到指定步数后才更新参数
            if (step + 1) % args.gradient_accumulation_steps == 0:
                # 梯度裁剪 - 使用更小的最大梯度范数
                torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)
                
                # 更新参数
                optimizer.step()
                
                # 更新学习率
                scheduler.step()
                
                # 清零梯度
                optimizer.zero_grad()
                
                # 更新步数
                global_step += 1
                
                # 限制TensorBoard记录频率，减少波动显示
                tb_logging_counter += 1
                if writer is not None and tb_logging_counter % args.tensorboard_logging_freq == 0:
                    writer.add_scalar('Training/Loss', train_loss_moving_avg, global_step)
                    writer.add_scalar('Training/LearningRate', scheduler.get_last_lr()[0], global_step)
                    # 每500步刷新一次TensorBoard
                    if global_step % 500 == 0:
                        writer.flush()
            
            # 更新进度条 - 显示平滑后的损失值
            progress_bar.set_postfix({'loss': f"{train_loss_moving_avg:.4f}", 'lr': f"{scheduler.get_last_lr()[0]:.2e}"})
        
        # 计算平均训练损失
        avg_train_loss = total_train_loss / epoch_steps if epoch_steps > 0 else 0
        train_losses.append(avg_train_loss)
        logger.info(f"平均训练损失: {avg_train_loss:.4f}")
        
        # 验证模式
        model.eval()
        
        total_val_loss = 0
        total_correct = 0
        total_examples = 0
        
        # 保存每个类别的统计信息
        class_correct = {}
        class_total = {}
        
        # 保存每个类别的预测结果用于计算精确率、召回率和F1值
        all_predictions = []
        all_labels = []
        
        for batch in tqdm(val_dataloader, desc="验证中"):
            # 准备数据
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # 不计算梯度
            with torch.no_grad():
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )
            
            loss = outputs.loss
            total_val_loss += loss.item()
            
            # 计算准确率
            logits = outputs.logits
            predictions = torch.argmax(logits, dim=1)
            correct = (predictions == labels).sum().item()
            
            # 记录每个类别的准确率
            for i in range(len(labels)):
                label = labels[i].item()
                pred = predictions[i].item()
                if label not in class_correct:
                    class_correct[label] = 0
                    class_total[label] = 0
                if label not in class_total:
                    class_total[label] = 0
                
                class_total[label] += 1
                if label == pred:
                    class_correct[label] = class_correct.get(label, 0) + 1
            
            all_predictions.extend(predictions.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())
            
            total_correct += correct
            total_examples += len(labels)
        
        # 计算平均验证损失和准确率
        avg_val_loss = total_val_loss / len(val_dataloader) if len(val_dataloader) > 0 else 0
        val_losses.append(avg_val_loss)
        accuracy = total_correct / total_examples if total_examples > 0 else 0
        accuracies.append(accuracy)
        
        # 记录每个类别的准确率
        class_accuracies = {}
        for label in class_total:
            if class_total[label] > 0:
                class_accuracies[label] = class_correct.get(label, 0) / class_total[label]
            else:
                class_accuracies[label] = 0
        
        logger.info(f"验证损失: {avg_val_loss:.4f}")
        logger.info(f"验证准确率: {accuracy:.4f}")
        logger.info(f"类别准确率: {class_accuracies}")
        
        # 是否有提升
        accuracy_improved = accuracy > best_accuracy
        val_loss_improved = avg_val_loss < best_val_loss
        
        if accuracy_improved:
            best_accuracy = accuracy
            logger.info(f"新的最佳准确率: {best_accuracy:.4f}")
        
        if val_loss_improved:
            best_val_loss = avg_val_loss
            # 保存最佳模型状态
            best_model_state = model.state_dict().copy()
            patience_counter = 0
            logger.info(f"新的最佳验证损失: {best_val_loss:.4f}")
        else:
            patience_counter += 1
            logger.info(f"验证损失未改善，耐心计数: {patience_counter}/{args.patience}")
        
        # 计算精确率、召回率和F1值（如果可能）
        if len(set(all_labels)) > 1:
            precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_predictions, average='weighted')
            logger.info(f"加权精确率: {precision:.4f}")
            logger.info(f"加权召回率: {recall:.4f}")
            logger.info(f"加权F1分数: {f1:.4f}")
            
            # 计算混淆矩阵
            cm = confusion_matrix(all_labels, all_predictions)
            logger.info(f"混淆矩阵:\n{cm}")
            
            # 记录到TensorBoard
            if writer is not None:
                writer.add_scalar('Validation/Loss', avg_val_loss, epoch)
                writer.add_scalar('Validation/Accuracy', accuracy, epoch)
                writer.add_scalar('Validation/Precision', precision, epoch)
                writer.add_scalar('Validation/Recall', recall, epoch)
                writer.add_scalar('Validation/F1', f1, epoch)
                
                # 记录每个类别的准确率
                for label, acc in class_accuracies.items():
                    writer.add_scalar(f'Validation/Class_{label}_Accuracy', acc, epoch)
                
                # 可视化混淆矩阵
                try:
                    fig = plt.figure(figsize=(8, 8))
                    canvas = FigureCanvas(fig)
                    ax = fig.add_subplot(111)
                    cax = ax.matshow(cm, cmap=plt.cm.Blues)
                    fig.colorbar(cax)
                    
                    # 设置坐标轴
                    ax.set_title('Confusion Matrix')
                    ax.set_xlabel('Predicted Label')
                    ax.set_ylabel('True Label')
                    
                    # 添加数值标签
                    for i in range(cm.shape[0]):
                        for j in range(cm.shape[1]):
                            ax.text(j, i, str(cm[i, j]), va='center', ha='center')
                    
                    # 保存为图像
                    canvas.draw()
                    img_array = np.array(canvas.renderer.buffer_rgba())
                    img_array = np.transpose(img_array[:, :, :3], (2, 0, 1))  # HWC -> CHW
                    
                    writer.add_image('Validation/ConfusionMatrix', img_array, epoch)
                    plt.close(fig)
                except Exception as e:
                    logger.warning(f"绘制混淆矩阵时出错: {str(e)}")
                
                # 确保刷新数据到磁盘
                writer.flush()
        else:
            precision, recall, f1 = 0, 0, 0
            if writer is not None:
                writer.add_scalar('Validation/Loss', avg_val_loss, epoch)
                writer.add_scalar('Validation/Accuracy', accuracy, epoch)
        
        # 记录统计信息
        training_stats.append({
            'epoch': epoch + 1,
            'train_loss': avg_train_loss,
            'val_loss': avg_val_loss,
            'val_accuracy': accuracy,
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'class_accuracies': {str(k): v for k, v in class_accuracies.items()}  # 转换键为字符串以便JSON序列化
        })
        
        # 早停策略 - 基于验证损失和耐心参数
        if args.early_stopping and patience_counter >= args.patience:
            logger.info(f"早停触发: 验证损失 {args.patience} 轮未改善，停止训练")
            break
    
    # 绘制训练曲线
    if len(train_losses) > 1:
        try:
            plt.figure(figsize=(12, 8))
            
            # 损失曲线
            plt.subplot(2, 1, 1)
            plt.plot(range(1, len(train_losses) + 1), train_losses, label='Training Loss')
            plt.plot(range(1, len(val_losses) + 1), val_losses, label='Validation Loss')
            plt.title('Training and Validation Loss')
            plt.xlabel('Epoch')
            plt.ylabel('Loss')
            plt.legend()
            plt.grid(True)
            
            # 准确率曲线
            plt.subplot(2, 1, 2)
            plt.plot(range(1, len(accuracies) + 1), accuracies, label='Validation Accuracy')
            plt.axhline(y=best_accuracy, color='r', linestyle='--', label=f'Best Accuracy: {best_accuracy:.4f}')
            plt.title('Validation Accuracy')
            plt.xlabel('Epoch')
            plt.ylabel('Accuracy')
            plt.legend()
            plt.grid(True)
            
            plt.tight_layout()
            
            # 保存图表
            curves_path = os.path.join(args.output_dir, 'training_curves.png')
            plt.savefig(curves_path)
            logger.info(f"训练曲线已保存到: {curves_path}")
            
            # 添加图表到TensorBoard
            if writer is not None:
                try:
                    canvas = FigureCanvas(plt.gcf())
                    canvas.draw()
                    img_array = np.array(canvas.renderer.buffer_rgba())
                    img_array = np.transpose(img_array[:, :, :3], (2, 0, 1))  # HWC -> CHW
                    writer.add_image('Training/Curves', img_array, 0)
                except Exception as e:
                    logger.warning(f"添加训练曲线到TensorBoard时出错: {str(e)}")
            
            plt.close()
        except Exception as e:
            logger.warning(f"绘制训练曲线时出错: {str(e)}")
    
    # 保存训练统计信息
    with open(os.path.join(args.output_dir, 'training_stats.json'), 'w') as f:
        json.dump(training_stats, f, ensure_ascii=False, indent=2)
    
    # 加载最佳模型状态（如果有）
    if best_model_state is not None:
        model.load_state_dict(best_model_state)
        logger.info(f"已加载最佳模型状态（验证损失: {best_val_loss:.4f}，准确率: {best_accuracy:.4f}）")
    
    # 关闭TensorBoard writer
    if writer is not None:
        # 确保数据刷新到磁盘
        writer.flush()
        writer.close()
        logger.info(f"TensorBoard日志已关闭并刷新到磁盘")
    
    return model

def main():
    parser = argparse.ArgumentParser(description="训练BERT模型进行评论情感分析")
    parser.add_argument("--data_path", type=str, default="1_cleaned_All_attraction.csv", help="清洗后的CSV数据路径")
    parser.add_argument("--model_path", type=str, default="./bert-base-chinese/models--google-bert--bert-base-chinese/snapshots/c30a6ed22ab4564dc1e3b2ecbf6e766b0611a33f", help="预训练模型路径")
    parser.add_argument("--output_dir", type=str, default="./output", help="输出目录")
    parser.add_argument("--max_length", type=int, default=128, help="最大序列长度")
    parser.add_argument("--batch_size", type=int, default=16, help="批次大小")
    parser.add_argument("--gradient_accumulation_steps", type=int, default=4, help="梯度累积步数，可用于模拟更大批次")
    parser.add_argument("--epochs", type=int, default=10, help="训练轮数")
    parser.add_argument("--learning_rate", type=float, default=2e-5, help="学习率")
    parser.add_argument("--weight_decay", type=float, default=0.01, help="权重衰减")
    parser.add_argument("--max_grad_norm", type=float, default=0.5, help="梯度裁剪最大范数")
    parser.add_argument("--warmup_proportion", type=float, default=0.15, help="学习率预热比例")
    parser.add_argument("--seed", type=int, default=42, help="随机种子")
    parser.add_argument("--tensorboard", action="store_true", help="是否启用TensorBoard记录")
    parser.add_argument("--tensorboard_logging_freq", type=int, default=10, help="TensorBoard记录频率（每多少批次记录一次）")
    parser.add_argument("--visualize_embeddings", action="store_true", help="是否在TensorBoard中可视化词嵌入")
    parser.add_argument("--gpu_memory_cleanup", action="store_true", help="是否在训练后清理GPU显存缓存")
    parser.add_argument("--early_stopping", action="store_true", help="是否启用早停")
    parser.add_argument("--min_improvement", type=float, default=0.0005, help="早停最小改善阈值")
    parser.add_argument("--patience", type=int, default=3, help="早停耐心值（验证损失多少轮未改善则停止）")
    parser.add_argument("--class_weights", action="store_true", help="是否使用类别权重")
    parser.add_argument("--balance_data", action="store_true", help="是否平衡数据集")
    parser.add_argument("--slow_decay", action="store_true", help="是否使用缓慢的学习率衰减")
    
    args = parser.parse_args()
    
    # 打印当前工作目录和参数信息
    logger.info(f"当前工作目录: {os.getcwd()}")
    logger.info(f"训练参数: {vars(args)}")
    
    # 确保TensorBoard日志目录存在
    if args.tensorboard:
        tensorboard_dir = os.path.join(args.output_dir, 'tensorboard_logs')
        os.makedirs(tensorboard_dir, exist_ok=True)
        logger.info(f"TensorBoard日志目录: {os.path.abspath(tensorboard_dir)}")
        
        # 检查目录是否可写
        try:
            test_file = os.path.join(tensorboard_dir, 'test.txt')
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            logger.info("TensorBoard日志目录可写")
        except Exception as e:
            logger.warning(f"TensorBoard日志目录可能不可写: {str(e)}")
    
    # 设置随机种子
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)
    
    # 创建输出目录
    os.makedirs(args.output_dir, exist_ok=True)
    
    # 获取绝对路径
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(os.path.dirname(current_file_dir))
    
    # 处理数据路径
    data_path = args.data_path
    # 检查是否需要添加.csv扩展名
    if not data_path.endswith('.csv'):
        data_path += '.csv'
    
    # 检查各种可能的路径
    possible_paths = [
        data_path,  # 原始路径
        os.path.join(os.getcwd(), data_path),  # 当前工作目录
        os.path.join(current_file_dir, data_path),  # 脚本所在目录
        os.path.join(project_root, 'data/processed', data_path),  # 项目processed目录
    ]
    
    # 尝试找到存在的文件路径
    for path in possible_paths:
        if os.path.exists(path):
            data_path = path
            logger.info(f"找到数据文件: {data_path}")
            break
    else:
        logger.error(f"无法找到数据文件。尝试了以下路径: {possible_paths}")
        raise FileNotFoundError(f"找不到数据文件: {args.data_path}")
    
    logger.info(f"使用数据路径: {data_path}")
    
    # 加载数据
    texts, labels = load_data(data_path)
    
    # 划分训练集和验证集
    train_texts, val_texts, train_labels, val_labels = train_test_split(
        texts, labels, test_size=0.1, random_state=args.seed, stratify=labels if len(set(labels)) > 1 else None
    )
    
    # 如果需要平衡数据集
    if args.balance_data:
        logger.info("进行数据集平衡...")
        # 计算类别分布
        label_counts = Counter(train_labels)
        logger.info(f"原始训练集类别分布: {label_counts}")
        
        # 计算最小类别样本数
        min_count = min(label_counts.values())
        
        # 对每个类别进行下采样
        balanced_texts = []
        balanced_labels = []
        indices_by_label = {}
        
        # 对每个类别的索引进行分组
        for i, label in enumerate(train_labels):
            if label not in indices_by_label:
                indices_by_label[label] = []
            indices_by_label[label].append(i)
        
        # 从每个类别中随机选择相同数量的样本
        np.random.seed(args.seed)
        for label, indices in indices_by_label.items():
            # 确保平衡后每个类别至少有200个样本
            sample_size = max(min_count, min(200, len(indices)))
            sampled_indices = np.random.choice(indices, size=sample_size, replace=False)
            for idx in sampled_indices:
                balanced_texts.append(train_texts[idx])
                balanced_labels.append(train_labels[idx])
        
        # 替换原始训练集
        train_texts, train_labels = balanced_texts, balanced_labels
        logger.info(f"平衡后训练集大小: {len(train_texts)}")
        logger.info(f"平衡后训练集类别分布: {Counter(train_labels)}")
    
    logger.info(f"训练集大小: {len(train_texts)}")
    logger.info(f"验证集大小: {len(val_texts)}")
    
    # 处理模型路径
    if not os.path.isabs(args.model_path):
        model_path = os.path.join(current_file_dir, args.model_path)
    else:
        model_path = args.model_path
    
    logger.info(f"使用模型路径: {model_path}")
    
    # 加载tokenizer和模型
    try:
        tokenizer = BertTokenizer.from_pretrained(model_path)
        logger.info("成功加载本地BERT模型")
    except:
        logger.info("本地模型加载失败，尝试从Hugging Face下载...")
        tokenizer = BertTokenizer.from_pretrained("bert-base-chinese")
        
    # 分类数量（根据你的任务调整）
    num_labels = len(set(labels))
    logger.info(f"分类数量: {num_labels}")
    
    try:
        model = BertForSequenceClassification.from_pretrained(
            model_path,
            num_labels=num_labels,
            output_attentions=False,
            output_hidden_states=False,
        )
    except:
        logger.info("本地模型加载失败，尝试从Hugging Face下载...")
        model = BertForSequenceClassification.from_pretrained(
            "bert-base-chinese",
            num_labels=num_labels,
            output_attentions=False,
            output_hidden_states=False,
        )
    
    # 准备数据集
    train_dataset = CommentDataset(train_texts, train_labels, tokenizer, max_length=args.max_length)
    val_dataset = CommentDataset(val_texts, val_labels, tokenizer, max_length=args.max_length)
    
    # 准备数据加载器
    train_dataloader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=args.batch_size)
    
    # 如果启用了类别权重，计算每个类别的权重
    if args.class_weights:
        # 计算类别权重
        unique_labels = np.unique(train_labels)
        class_weights = compute_class_weight('balanced', classes=unique_labels, y=train_labels)
        class_weights_tensor = torch.tensor(class_weights, dtype=torch.float).to(torch.device('cuda' if torch.cuda.is_available() else 'cpu'))
        logger.info(f"类别权重: {class_weights}")
        
        # 设置模型的类别权重 - 仅在训练时使用，不存储在配置中
        # 这样可以避免JSON序列化错误
        model._class_weights = class_weights_tensor
    
    # 训练模型
    model = train_model(model, train_dataloader, val_dataloader, args)
    
    # GPU显存清理（如果启用）
    if args.gpu_memory_cleanup and torch.cuda.is_available():
        try:
            logger.info("清理GPU显存缓存...")
            torch.cuda.empty_cache()
            gc.collect()
            logger.info("GPU显存缓存清理完成")
        except Exception as e:
            logger.warning(f"清理GPU显存时出错: {str(e)}")
    
    # 如果启用了TensorBoard并且要可视化嵌入
    if args.tensorboard and args.visualize_embeddings:
        try:
            logger.info("正在可视化词嵌入...")
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            model.eval()
            
            # 创建TensorBoard writer
            log_dir = os.path.join(args.output_dir, 'tensorboard_logs', 'embeddings')
            os.makedirs(log_dir, exist_ok=True)
            writer = SummaryWriter(log_dir=log_dir)
            
            # 仅选择一小部分验证数据进行可视化
            sample_size = min(100, len(val_dataset))
            sample_indices = np.random.choice(len(val_dataset), sample_size, replace=False)
            
            # 收集数据
            embeddings = []
            labels = []
            texts = []
            
            with torch.no_grad():
                for idx in sample_indices:
                    try:
                        sample = val_dataset[idx]
                        input_ids = sample['input_ids'].unsqueeze(0).to(device)
                        attention_mask = sample['attention_mask'].unsqueeze(0).to(device)
                        label = sample['labels'].item()
                        
                        # 获取[CLS]的隐藏状态作为句子表示
                        outputs = model.bert(input_ids=input_ids, attention_mask=attention_mask)
                        cls_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                        
                        # 解码回原始文本
                        text = tokenizer.decode(input_ids[0].cpu(), skip_special_tokens=True)
                        
                        embeddings.append(cls_embedding)
                        labels.append(label)
                        texts.append(text[:50])  # 取前50个字符作为标签
                    except Exception as e:
                        logger.warning(f"处理样本 {idx} 时出错: {str(e)}")
                        continue
            
            if len(embeddings) > 0:
                # 将数据转换为numpy数组
                embeddings = np.vstack(embeddings)
                
                # 将标签映射为可读的情感标签（使用英文）
                sentiment_labels = {0: "Negative", 1: "Positive"}
                label_names = [sentiment_labels.get(label, f"Class_{label}") for label in labels]
                
                # 添加到TensorBoard
                try:
                    writer.add_embedding(
                        mat=embeddings, 
                        metadata=label_names,
                        metadata_header=["Sentiment"],
                        tag="Sentiment Embeddings"
                    )
                    logger.info(f"嵌入可视化已保存到 {log_dir}")
                except Exception as e:
                    logger.warning(f"保存嵌入可视化时出错: {str(e)}")
            else:
                logger.warning("没有有效样本用于嵌入可视化")
            
            writer.close()
        except Exception as e:
            logger.warning(f"嵌入可视化过程出错，但训练和模型保存将继续: {str(e)}")
    
    # 保存模型
    if not os.path.isabs(args.output_dir):
        output_dir = os.path.join(current_file_dir, args.output_dir)
    else:
        output_dir = args.output_dir
    
    model_save_path = os.path.join(output_dir, 'bert_model')
    
    # 保存模型前，确保移除任何不可序列化的属性
    if hasattr(model, '_class_weights'):
        delattr(model, '_class_weights')
    
    model.save_pretrained(model_save_path)
    tokenizer.save_pretrained(model_save_path)
    
    logger.info(f"模型已保存到 {model_save_path}")

    # 训练结束后，打印TensorBoard查看指令
    if args.tensorboard:
        tensorboard_dir = os.path.join(args.output_dir, 'tensorboard_logs')
        abs_tensorboard_dir = os.path.abspath(tensorboard_dir)
        logger.info("\n" + "="*80)
        logger.info(f"训练完成! 使用以下命令查看TensorBoard:")
        logger.info(f"tensorboard --logdir={abs_tensorboard_dir}")
        logger.info("然后在浏览器中访问 http://localhost:6006")
        logger.info("="*80 + "\n")

if __name__ == "__main__":
    main() 