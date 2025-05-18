# 图表英文化说明

为解决服务器环境中文字体缺失导致的图表乱码问题，我们对训练脚本进行了英文化修改。

## 修改内容

1. **字体设置**

   - 将`SimHei`中文字体改为通用的`DejaVu Sans`字体
   - 移除对特定中文字体的依赖，避免字体缺失警告
   - 保留了负号正常显示的设置

2. **图表标签**

   - 损失曲线图表名称由"训练与验证损失"改为"Training and Validation Loss"
   - 横轴标签由"轮次"改为"Epoch"
   - 纵轴标签由"损失"改为"Loss"
   - 图例由"训练损失"、"验证损失"改为"Training Loss"、"Validation Loss"

3. **准确率图表**

   - 图表名称由"验证准确率"改为"Validation Accuracy"
   - 横轴标签由"轮次"改为"Epoch"
   - 纵轴标签由"准确率"改为"Accuracy"
   - 图例由"验证准确率"、"最佳准确率"改为"Validation Accuracy"、"Best Accuracy"

4. **混淆矩阵**

   - 图表名称由"混淆矩阵"改为"Confusion Matrix"
   - 横轴标签由"预测标签"改为"Predicted Label"
   - 纵轴标签由"真实标签"改为"True Label"

5. **嵌入可视化**
   - 情感标签由"消极"、"积极"改为"Negative"、"Positive"
   - 标签分类名由"情感"改为"Sentiment"
   - 可视化标签由"情感嵌入"改为"Sentiment Embeddings"

## 效果

通过这些修改，解决了以下问题：

1. 避免了因中文字体缺失导致的`findfont: Generic family 'sans-serif' not found because none of the following families were found: SimHei`警告
2. 确保图表在任何环境下都能正常显示
3. 保持了图表的专业性和可读性

## 备注

若希望在不同环境下都能显示中文，可考虑以下方案：

1. 在服务器上安装中文字体包（如`fonts-wqy-microhei`）
2. 使用图片格式保存图表，避免字体问题
3. 使用 matplotlib 内嵌的中文字体（虽然支持有限）

对于本项目，考虑到在多种环境下的兼容性，我们选择了完全使用英文标签的方案，这是最稳定可靠的解决方案。
