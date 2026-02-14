from sqlalchemy import create_engine  # 导入创建数据库引擎的函数
from sqlalchemy.ext.declarative import declarative_base  # 导入声明式基类
from sqlalchemy.orm import sessionmaker  # 导入会话工厂类
from app.core.config import get_settings  # 导入配置获取函数

settings = get_settings()

engine = create_engine(
    settings.DATABASE_URL,  # 数据库连接字符串
    pool_pre_ping=True,  # 在每次连接前检测连接是否有效，自动断开无效连接
    pool_recycle=3600,  # 连接回收时间（秒），超过3600秒的连接会被回收，防止连接过期
    pool_size=10,  # 连接池大小，保持10个空闲连接
    max_overflow=20,  # 最大溢出连接数，连接池满时可额外创建20个连接
    echo=False  # 是否打印SQL语句到控制台，开发时可设为True调试
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 创建数据库会话工厂
# autocommit=False: 不自动提交事务，需要手动commit
# autoflush=False: 不自动刷新，需要手动flush
# bind=engine: 绑定到上面创建的引擎

Base = declarative_base()
# 创建声明式基类
# 所有数据库模型都要继承这个基类
# 这个基类提供了表元数据和ORM映射功能


def get_db():
    """
    获取数据库会话（依赖注入函数）
    
    这是FastAPI的依赖注入函数，用于在路由中获取数据库会话
    使用yield关键字，确保请求结束后会话会被正确关闭
    
    使用示例:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()  # 创建数据库会话
    try:
        yield db  # 将会话提供给依赖此函数的函数使用
    finally:
        db.close()  # 无论是否发生异常，都要关闭会话，释放数据库连接


def init_db():
    """
    初始化数据库表结构
    
    导入所有模型类后，创建所有表
    如果表已存在则跳过，不会删除数据
    
    说明:
        这个函数应该在应用启动时或首次部署时调用
        它会根据模型类的定义，在数据库中创建对应的表结构
    """
    from app.models import (
        User, Role, Permission, UserRole, RolePermission,
        Department, Supplier, Customer,
        Product, ProductCategory, Warehouse, StockRecord, StockCheck, StockCheckItem,
        PurchaseOrder, PurchaseOrderItem,
        SalesOrder, SalesOrderItem,
        Payment, Bill, Account, CostCenter,
        WorkflowDefinition, WorkflowInstance, WorkflowLog
    )
    # 根据所有模型类的定义，创建数据库表
    Base.metadata.create_all(bind=engine)
