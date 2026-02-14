from sqlalchemy.orm import Session
from app.core.config import get_settings
from app.db.session import engine, SessionLocal
from app.models import User, Role, UserRole, Department
from app.core.security import get_password_hash

def create_admin_user():
    """
    创建系统管理员用户
    
    功能说明:
        1. 检查admin用户是否已存在
        2. 如果不存在，则创建admin用户
        3. 设置默认密码为admin123
        4. 标记为超级用户，拥有所有权限
    
    技术细节:
        - 使用get_password_hash对密码进行加密存储
        - 使用bcrypt算法，密码不可逆
        - is_superuser=True表示超级用户，拥有所有权限
        - status=True表示用户处于激活状态
    
    默认账号信息:
        - 用户名: admin
        - 密码: admin123
        - 真实姓名: 系统管理员
        - 邮箱: admin@example.com
        - 电话: 13800138000
    
    异常处理:
        - 如果创建失败，执行rollback回滚事务
        - 使用try-finally确保数据库连接被正确关闭
    """
    settings = get_settings()
    db: Session = SessionLocal()
    
    try:
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Admin user already exists")
            return
        
        admin_user = User(
            username="admin",
            password=get_password_hash("admin123"),
            real_name="系统管理员",
            email="admin@example.com",
            phone="13800138000",
            is_superuser=True,
            status=True
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
