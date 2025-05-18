import os
import sys
import logging
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# 设置日志
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   handlers=[logging.StreamHandler()])

logger = logging.getLogger(__name__)

# 确保能够导入app模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 从配置文件导入数据库URL
from app.config.settings import settings
from app.models.database import Base, engine

def check_sentiment_type_column():
    """检查posts表中是否存在sentiment_type列"""
    try:
        # 创建连接
        conn = engine.connect()
        
        # 检查PostgreSQL数据库
        if 'postgresql' in str(engine.url):
            query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'posts' AND column_name = 'sentiment_type';
            """)
        # 检查MySQL数据库
        elif 'mysql' in str(engine.url):
            query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'posts' AND column_name = 'sentiment_type';
            """)
        # 检查SQLite数据库
        else:
            query = text("""
                PRAGMA table_info(posts);
            """)
            
        result = conn.execute(query)
        rows = result.fetchall()
        
        # 对于SQLite，检查返回的行中是否有sentiment_type列
        if 'sqlite' in str(engine.url):
            for row in rows:
                if 'sentiment_type' in row:
                    logger.info("sentiment_type列已存在于posts表中")
                    return True
            logger.info("posts表中不存在sentiment_type列")
            return False
        
        # 对于其他数据库，如果查询返回结果，则列存在
        elif rows:
            logger.info("sentiment_type列已存在于posts表中")
            return True
        else:
            logger.info("posts表中不存在sentiment_type列")
            return False
            
    except Exception as e:
        logger.error(f"检查列时出错: {str(e)}")
        return False
    finally:
        conn.close()

def add_sentiment_type_column():
    """添加sentiment_type列到posts表"""
    try:
        # 创建连接
        conn = engine.connect()
        
        # 为不同类型的数据库准备SQL语句
        if 'postgresql' in str(engine.url) or 'mysql' in str(engine.url):
            query = text("""
                ALTER TABLE posts 
                ADD COLUMN IF NOT EXISTS sentiment_type VARCHAR(50);
            """)
        else:  # SQLite
            # 检查是否存在列
            check_query = text("""
                PRAGMA table_info(posts);
            """)
            result = conn.execute(check_query)
            rows = result.fetchall()
            
            # 检查列是否存在
            column_exists = False
            for row in rows:
                if row[1] == 'sentiment_type':  # 列名在SQLite的PRAGMA查询中是第二个字段
                    column_exists = True
                    break
            
            # 如果列不存在，则添加
            if not column_exists:
                query = text("""
                    ALTER TABLE posts 
                    ADD COLUMN sentiment_type VARCHAR(50);
                """)
                conn.execute(query)
                logger.info("成功添加sentiment_type列到posts表")
            else:
                logger.info("sentiment_type列已存在，无需添加")
            
            return True
        
        # 执行ALTER TABLE语句（对于PostgreSQL和MySQL）
        if 'postgresql' in str(engine.url) or 'mysql' in str(engine.url):
            conn.execute(query)
            logger.info("成功添加sentiment_type列到posts表")
        
        return True
        
    except Exception as e:
        logger.error(f"添加列时出错: {str(e)}")
        return False
    finally:
        conn.close()

def main():
    """主函数"""
    try:
        # 检查是否存在sentiment_type列
        if not check_sentiment_type_column():
            # 如果不存在，添加该列
            if add_sentiment_type_column():
                logger.info("数据库更新成功")
            else:
                logger.error("更新数据库失败")
        else:
            logger.info("数据库已经是最新的，无需更新")
            
    except Exception as e:
        logger.error(f"更新数据库时出错: {str(e)}")

if __name__ == "__main__":
    logger.info(f"开始更新数据库，数据库URL: {settings.DATABASE_URL}")
    main() 