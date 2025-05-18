"""
为用户表添加兴趣标签字段的迁移脚本
"""

from sqlalchemy import create_engine, MetaData, Table, Column, Text
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 连接数据库
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL)
metadata = MetaData()

def upgrade():
    """添加兴趣标签字段到用户表"""
    
    # 获取现有用户表
    users = Table('users', metadata, autoload_with=engine)
    
    # 检查兴趣标签字段是否已存在
    if 'interest_tags' not in users.columns:
        # 如果不存在则添加字段
        print("添加 interest_tags 字段到 users 表...")
        with engine.begin() as conn:
            conn.execute(f"ALTER TABLE users ADD COLUMN interest_tags TEXT")
        print("添加字段完成")
    else:
        print("interest_tags 字段已存在，无需添加")

def downgrade():
    """移除兴趣标签字段"""
    
    # 获取现有用户表
    users = Table('users', metadata, autoload_with=engine)
    
    # 检查兴趣标签字段是否存在
    if 'interest_tags' in users.columns:
        # 如果存在则移除字段
        print("从 users 表中移除 interest_tags 字段...")
        with engine.begin() as conn:
            conn.execute(f"ALTER TABLE users DROP COLUMN interest_tags")
        print("移除字段完成")
    else:
        print("interest_tags 字段不存在，无需移除")

if __name__ == "__main__":
    # 执行迁移操作
    upgrade() 