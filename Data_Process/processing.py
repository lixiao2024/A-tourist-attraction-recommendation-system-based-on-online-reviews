"""
@FileName??processing.py\n
@Description????????\n
@Author??Surely\n
@Time?? 2025 - 02 - 2025/2/21\n
"""
# -*- coding: utf-8 -*-
import os
import pandas as pd
folder_path = "I:\\基于在线评论的旅游景点智能推荐系统\\Data_Process\\test"

csv_files = [f for f in os.listdir(folder_path) if f.endswith('.xlsx')]


merged_df = pd.DataFrame()


for csv_file in csv_files:
    file_path = os.path.join(folder_path, csv_file)
    df = pd.read_csv(file_path)
    merged_df = pd.concat([merged_df, df], ignore_index=True)


merged_df.to_csv("I:\\基于在线评论的旅游景点智能推荐系统\\Data_Process\\chongqing_attraction.xlsx", index=False)