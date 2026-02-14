from datetime import datetime  # 导入日期时间模块
from sqlalchemy import Column, Integer, DateTime  # 导入SQLAlchemy的列类型
from app.db.session import Base  # 导入声明式基类


class BaseModel(Base):
    """
    数据库模型基类
    
    所有其他模型类都应该继承这个基类
    提供通用的字段：id, created_at, updated_at
    
    使用示例:
        class User(BaseModel):
            __tablename__ = "users"
            username = Column(String(50))
    """
    __abstract__ = True  # 声明这是一个抽象基类，不会创建对应的数据库表
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    # 主键字段
    # Integer: 整数类型
    # primary_key=True: 设置为主键
    # index=True: 创建索引，提高查询速度
    # autoincrement=True: 自动递增
    
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # 创建时间字段
    # DateTime: 日期时间类型
    # default=datetime.utcnow: 默认值为当前UTC时间
    # nullable=False: 不允许为空
    
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    # 更新时间字段
    # default=datetime.utcnow: 创建时的默认值
    # onupdate=datetime.utcnow: 每次更新时自动设置为当前时间
    # nullable=False: 不允许为空
