from sqlalchemy.orm import Session
from app.models.database import engine, SessionLocal
from app.models.user import User

def test_db_connection():
    """测试数据库连接和基本操作"""
    print("正在测试数据库连接...")
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 测试查询用户表
        user_count = db.query(User).count()
        print(f"数据库连接成功！当前用户表中有 {user_count} 条记录。")
        
        # 创建测试用户
        test_user = User(
            openid="test_openid",
            session_key="test_session_key",
            nickname="测试用户",
            avatar_url="https://example.com/avatar.jpg",
            gender=1,
            country="中国",
            province="广东",
            city="深圳",
            language="zh_CN"
        )
        
        # 添加到数据库
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"测试用户创建成功！用户ID: {test_user.id}")
        
        # 查询并显示用户
        users = db.query(User).all()
        print(f"\n当前所有用户 ({len(users)}):")
        for user in users:
            print(f"ID: {user.id}, 昵称: {user.nickname}, OpenID: {user.openid}")
            
    except Exception as e:
        print(f"数据库操作失败: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection() 