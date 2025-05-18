from app.models.database import Base, engine
from app.models.user import User

def init_db():
    """初始化数据库，创建所有表"""
    print("正在删除已存在的表...")
    Base.metadata.drop_all(bind=engine)
    print("表删除完成。")
    
    print("正在创建新的数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成！")

if __name__ == "__main__":
    init_db() 