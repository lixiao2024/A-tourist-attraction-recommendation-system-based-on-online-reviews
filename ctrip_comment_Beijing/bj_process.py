"""
@FileName：bj_process.py\n
@Description：机器学习\n
@Author：Surely\n
@Time： 2025 - 02 - 2025/2/20\n
"""

# import pandas as pd
#
# # 读取 Excel 文件
# file_path = "I:\\基于在线评论的旅游景点智能推荐系统\\ctrip_comment_Beijing\\北京八达岭长城好评.csv"  # 替换为你的 Excel 文件路径
# df = pd.read_excel(file_path)
#
# # 填充 M 列（Excel 的 M 列是 pandas 的第 12 列，因为索引从 0 开始）
# df.iloc[1:852, 12] = "北京八达岭长城"  # 注意 iloc[1:852] 是选取第 2 行到第 852 行
#
# # 保存修改后的 Excel 文件
# output_path = "output_file.xlsx"  # 替换为你想保存的文件名
# df.to_excel(output_path, index=False)
#
# print("Excel M 列填充完成！")

import pandas as pd
import os

# 设定文件夹路径，存放所有 Excel 文件
folder_path = "I:\\基于在线评论的旅游景点智能推荐系统\\ctrip_comment_Beijing"  # 替换为存放 Excel 文件的文件夹路径
output_file = "merged_comments.csv"  # 合并后的 Excel 文件名

# 存放所有数据的 DataFrame
merged_df = pd.DataFrame()

# 遍历文件夹内所有 Excel 文件
for file in os.listdir(folder_path):
    if file.endswith(".csv") or file.endswith(".csv"):  # 只处理 Excel 文件
        file_path = os.path.join(folder_path, file)
        scenic_spot_name = os.path.splitext(file)[0]  # 获取不带扩展名的文件名（景点名称）

        # 读取 Excel 文件
        df = pd.read_csv(file_path, encoding="utf-8", errors="ignore")

        # 确保 M 列存在（如果 Excel 本身没有 M 列，就新建一列）
        df["M"] = scenic_spot_name

        # 合并数据
        merged_df = pd.concat([merged_df, df], ignore_index=True)

# 保存合并后的 Excel 文件
merged_df.to_csv(output_file, index=False)

print(f"合并完成！文件已保存为 {output_file}")
