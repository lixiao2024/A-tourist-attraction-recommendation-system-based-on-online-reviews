import csv
import pandas as pd
import os
import sys
import json
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置
from app.config.settings import settings

# 直接创建数据库连接和引擎，不依赖现有模型
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_csv_data(file_path):
    """
    加载CSV文件数据
    
    Args:
        file_path: CSV文件路径
    
    Returns:
        加载的DataFrame
    """
    try:
        # 尝试不同的编码方式读取CSV
        encodings = ['utf-8', 'gb18030', 'gbk', 'gb2312']
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"成功使用{encoding}编码读取CSV")
                break
            except UnicodeDecodeError:
                continue
        else:
            raise ValueError(f"无法以支持的编码读取CSV文件: {file_path}")
        
        print(f"加载了 {len(df)} 条数据")
        print(f"数据列: {df.columns.tolist()}")
        
        return df
    except Exception as e:
        print(f"加载CSV文件时出错: {str(e)}")
        return None

def extract_images_from_row(row):
    """
    从CSV行中提取所有有效的图片URL
    
    Args:
        row: DataFrame中的一行数据
    
    Returns:
        包含所有有效图片URL的列表
    """
    image_columns = [col for col in row.index if 'img' in col.lower() and isinstance(row[col], str) and len(row[col]) > 5]
    images = []
    
    for col in image_columns:
        url = row[col]
        if url and isinstance(url, str) and url.startswith('http'):
            images.append(url)
    
    return images

def clean_tags(tags_list):
    """
    清理标签列表，移除NaN值
    
    Args:
        tags_list: 标签列表
    
    Returns:
        清理后的标签列表
    """
    return [tag for tag in tags_list if tag and not pd.isna(tag)]

def import_comments_to_posts(csv_file_path):
    """
    将CSV中的评论数据导入到posts表中
    
    Args:
        csv_file_path: CSV文件路径
    """
    # 加载CSV数据
    df = load_csv_data(csv_file_path)
    if df is None:
        return
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 导入每一条评论
        for index, row in df.iterrows():
            # 开始每行的独立事务
            conn = engine.connect()
            trans = conn.begin()
            
            try:
                # 从行中提取数据
                username = row['user_detail_name'] if 'user_detail_name' in row else "匿名用户"
                content = row['content_wrap'] if 'content_wrap' in row else ""
                
                if not content:
                    print(f"跳过没有内容的行: {username}")
                    continue
                
                # 提取发布日期
                date_text = row.get('resource_date_text', '')
                created_at = None
                
                if date_text and '发布点评' in date_text:
                    date_str = date_text.split('发布点评')[0].strip()
                    try:
                        created_at = datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        created_at = datetime.now()
                else:
                    created_at = datetime.now()
                
                # 提取图片URL
                images = extract_images_from_row(row)
                
                # 提取点赞数
                likes_count = 0
                if 'like_content 2' in row and not pd.isna(row['like_content 2']):
                    try:
                        likes_count = int(row['like_content 2'])
                    except (ValueError, TypeError):
                        likes_count = 0
                
                # 提取标签信息并清理NaN值
                tags = []
                if 'text 4' in row and not pd.isna(row['text 4']):
                    tags.append(row['text 4'])
                if 'user_detail_tags_text' in row and not pd.isna(row['user_detail_tags_text']):
                    tags.append(row['user_detail_tags_text'])
                
                # 提取位置信息
                location = row.get('iplocation', '')
                if not pd.isna(location):
                    location = location.replace('IP属地:', '') if isinstance(location, str) else ''
                else:
                    location = ''
                
                # 检查是否有openid字段
                has_openid = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'users' AND column_name = 'openid'")).fetchone()
                
                # 创建或查找用户ID
                if has_openid:
                    # 新版用户表结构
                    result = conn.execute(text("SELECT id FROM users WHERE nickname = :username"), {"username": username})
                    user_id = result.fetchone()
                    
                    if not user_id:
                        # 创建新用户
                        result = conn.execute(
                            text("INSERT INTO users (nickname, openid, avatar_url) VALUES (:username, :openid, :avatar) RETURNING id"),
                            {"username": username, "openid": f"import_{username}", "avatar": "https://imgcdn.hulizhushou.com/o_1iqa8jl651qevqj21pdp5098v7.png"}
                        )
                        user_id = result.fetchone()[0]
                    else:
                        user_id = user_id[0]
                else:
                    # 旧版用户表结构
                    result = conn.execute(text("SELECT id FROM users WHERE username = :username"), {"username": username})
                    user_id = result.fetchone()
                    
                    if not user_id:
                        # 创建新用户
                        result = conn.execute(
                            text("INSERT INTO users (username, email, password, avatar) VALUES (:username, :email, :password, :avatar) RETURNING id"),
                            {"username": username, "email": f"{username}@example.com", "password": "hashed_password", "avatar": "https://imgcdn.hulizhushou.com/o_1iqa8jl651qevqj21pdp5098v7.png.png"}
                        )
                        user_id = result.fetchone()[0]
                    else:
                        user_id = user_id[0]
                
                # 使用直接SQL插入post数据
                conn.execute(
                    text("""
                    INSERT INTO posts (title, content, user_id, created_at, images, tags, location, cover_image, likes_count, sentiment_type)
                    VALUES (:title, :content, :user_id, :created_at, :images, :tags, :location, :cover_image, :likes_count, :sentiment_type)
                    """),
                    {
                        "title": f"{username}的青城山的评论",
                        "content": content,
                        "user_id": user_id,
                        "created_at": created_at,
                        "images": json.dumps(images),
                        "tags": json.dumps(["成都", "青城山"]),
                        "location": location,
                        "cover_image": images[0] if images else None,
                        "likes_count": likes_count,
                        "sentiment_type": "positive"
                    }
                )
                
                # 提交此行的事务
                trans.commit()
                print(f"成功添加 {username} 的评论，行号: {index+1}")
                
            except Exception as e:
                # 回滚此行的事务
                trans.rollback()
                print(f"处理行 {index+1} 时出错: {str(e)}")
            finally:
                # 关闭连接
                conn.close()
        
        print("数据导入完成！")
        
    except Exception as e:
        print(f"导入数据时出错: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) < 2:
        print("使用方法: python import_comments.py <csv文件路径>")
        sys.exit(1)
    
    csv_file_path = sys.argv[1]
    
    # 检查文件是否存在
    if not os.path.exists(csv_file_path):
        print(f"错误: 文件 {csv_file_path} 不存在")
        sys.exit(1)
    
    print(f"开始从 {csv_file_path} 导入评论数据...")
    import_comments_to_posts(csv_file_path) 