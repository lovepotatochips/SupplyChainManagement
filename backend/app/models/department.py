from sqlalchemy import Column, String, Integer, ForeignKey, Text  # 导入SQLAlchemy的列类型
from sqlalchemy.orm import relationship  # 导入关系映射功能
from app.db.base import BaseModel  # 导入模型基类


class Department(BaseModel):
    """
    部门模型类
    
    用于存储企业的组织架构信息，支持多级部门结构
    部门通过parent_id实现树形层级关系
    用户与部门是多对一关系，一个用户属于一个部门
    """
    __tablename__ = "departments"  # 对应的数据库表名
    
    name = Column(String(100), nullable=False, comment="部门名称")
    # 部门名称，必填字段，长度限制为100字符
    
    code = Column(String(50), unique=True, index=True, comment="部门编码")
    # 部门编码，全局唯一，用于系统内部标识
    # unique=True: 编码不能重复
    # index=True: 创建索引，提高查询速度
    
    parent_id = Column(Integer, ForeignKey("departments.id"), comment="父部门ID")
    # 父部门ID，用于构建多级部门结构
    # 外键关联到本表的id字段，实现自引用
    # 如果为NULL，表示这是顶级部门
    
    sort_order = Column(Integer, default=0, comment="排序")
    # 排序字段，数字越小排序越靠前
    # 用于控制同级部门的显示顺序
    
    leader = Column(String(50), comment="负责人")
    # 部门负责人姓名
    
    phone = Column(String(20), comment="联系电话")
    # 部门联系电话
    
    address = Column(String(255), comment="地址")
    # 部门所在地址
    
    description = Column(Text, comment="部门描述")
    # 部门描述信息，Text类型支持更长的文本
    
    status = Column(Integer, default=1, comment="状态：1-启用，0-禁用")
    # 部门状态，1表示启用，0表示禁用
    # 禁用的部门不能添加用户
    
    parent = relationship("Department", remote_side="Department.id", backref="children")
    # 建立自引用关系，实现部门树结构
    # remote_side="Department.id": 指定父级端的字段是Department.id
    # backref="children": 创建反向引用，可以通过department.children获取子部门列表
    # 通过department.parent可以获取父部门对象
    
    def to_dict(self):
        """
        将模型对象转换为字典
        
        返回:
            dict: 包含部门信息的字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "parent_id": self.parent_id,
            "sort_order": self.sort_order,
            "leader": self.leader,
            "phone": self.phone,
            "address": self.address,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
