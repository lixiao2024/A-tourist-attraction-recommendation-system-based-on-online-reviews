
import os
import pandas as pd
# coding=utf-8
folder_path = "I:\\基于在线评论的旅游景点智能推荐系统\\数据收集与预处理\\The_final" # 替换为你的文件夹路径

# 获取文件夹中的所有CSV文件
csv_files = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

# 创建一个空的DataFrame，用于合并所有数据
merged_df = pd.DataFrame()

# 读取并合并每个CSV文件
for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)  # 读取当前CSV文件
    merged_df = pd.concat([merged_df, df], ignore_index=True)  # 合并数据

# 保存合并后的数据到新的CSV文件
merged_df.to_csv('merged_output2.csv', index=False)

