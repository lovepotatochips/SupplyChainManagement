from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from app.db.base import Base
from app.models import (
    User, Role, Permission, UserRole, RolePermission,
    Department,
    Supplier,
    PurchaseOrder, PurchaseOrderItem,
    Product, ProductCategory, Warehouse, StockRecord, StockCheck, StockCheckItem,
    Customer, SalesOrder, SalesOrderItem,
    Payment, Bill, Account, CostCenter,
    WorkflowDefinition, WorkflowInstance, WorkflowLog
)

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """
    初始化数据库表结构
    
    功能说明:
        1. 创建数据库连接引擎
        2. 根据所有导入的模型类自动创建对应的数据表
        3. 如果表已存在，则跳过创建
    
    技术细节:
        - Base是所有模型类的基类，包含所有模型的元数据
        - create_all方法会检查每个模型对应的表是否存在
        - 如果不存在，则执行CREATE TABLE语句创建表
        - autocommit=False和autoflush=False是SQLAlchemy的推荐设置
    
    使用场景:
        - 首次部署系统时运行
        - 添加新的模型类后运行
    """
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()
