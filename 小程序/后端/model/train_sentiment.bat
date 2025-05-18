@echo off
echo ==============================================
echo BERT情感分析模型训练优化版
echo ==============================================

REM 设置环境变量以防止CUDA错误
set "PYTORCH_CUDA_ALLOC_CONF=max_split_size_mb:32"

REM 命令行参数
set "DATA_PATH=1_cleaned_All_attraction.csv"
set "OUTPUT_DIR=./output/optimized"
set "MODEL_PATH=./bert-base-chinese"

REM 创建输出目录
mkdir "%OUTPUT_DIR%" 2>nul

echo 使用优化配置开始训练BERT情感分析模型...
echo 数据路径: %DATA_PATH%
echo 输出目录: %OUTPUT_DIR%
echo 模型路径: %MODEL_PATH%

REM 运行训练脚本 - 使用优化的超参数
python train_bert.py ^
  --data_path="%DATA_PATH%" ^
  --output_dir="%OUTPUT_DIR%" ^
  --model_path="%MODEL_PATH%" ^
  --batch_size=16 ^
  --gradient_accumulation_steps=4 ^
  --learning_rate=2e-5 ^
  --epochs=10 ^
  --max_grad_norm=0.5 ^
  --warmup_proportion=0.15 ^
  --tensorboard ^
  --tensorboard_logging_freq=10 ^
  --early_stopping ^
  --patience=3 ^
  --slow_decay ^
  --class_weights

echo.
echo 如果训练成功完成，模型将保存在 %OUTPUT_DIR%/bert_model
echo 请使用以下命令运行TensorBoard查看训练过程：
echo tensorboard --logdir=%OUTPUT_DIR%/tensorboard_logs
echo 然后在浏览器中访问 http://localhost:6006

pause 