from sqlalchemy import Column, String, Integer, Text, Float, Boolean  # 导入SQLAlchemy的列类型
from app.db.base import BaseModel  # 导入模型基类


class Supplier(BaseModel):
    """
    供应商模型类
    
    用于存储供应商的基本信息和财务信息
    供应商是供应链管理中的重要角色，与采购订单相关联
    """
    __tablename__ = "suppliers"
    # 对应的数据库表名
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="供应商编码")
    # 供应商编码，全局唯一
    # unique=True: 编码不能重复
    # index=True: 创建索引，提高查询速度
    # nullable=False: 必填字段
    
    name = Column(String(200), nullable=False, index=True, comment="供应商名称")
    # 供应商名称，必填字段
    # index=True: 创建索引，提高查询速度
    
    type = Column(String(20), default="manufacturer", comment="供应商类型：manufacturer/distributor/other")
    # 供应商类型，默认为manufacturer（制造商）
    # manufacturer: 制造商
    # distributor: 分销商
    # other: 其他
    
    contact_person = Column(String(50), comment="联系人")
    # 供应商联系人姓名
    
    contact_phone = Column(String(20), comment="联系电话")
    # 供应商联系电话
    
    contact_email = Column(String(100), comment="联系邮箱")
    # 供应商联系邮箱
    
    address = Column(String(255), comment="地址")
    # 供应商地址
    
    tax_number = Column(String(50), comment="税号")
    # 供应商税号，用于开票和税务管理
    
    bank_name = Column(String(100), comment="开户银行")
    # 供应商开户银行名称
    
    bank_account = Column(String(50), comment="银行账号")
    # 供应商银行账号
    
    credit_level = Column(String(20), default="A", comment="信用等级：A/B/C/D")
    # 供应商信用等级，默认为A级
    # A: 信用最好
    # B: 信用良好
    # C: 信用一般
    # D: 信用较差
    
    credit_limit = Column(Float, default=0.0, comment="信用额度")
    # 供应商信用额度，默认为0
    # 用于控制对供应商的欠款上限
    
    balance = Column(Float, default=0.0, comment="余额")
    # 供应商当前余额，默认为0
    # 正数表示供应商欠款，负数表示预付款
    
    status = Column(Boolean, default=True, comment="状态")
    # 供应商状态，默认为启用
    # True: 启用，可以正常交易
    # False: 禁用，不能进行新交易
    
    remark = Column(Text, comment="备注")
    # 供应商备注信息
    
    def to_dict(self):
        """
        将模型对象转换为字典
        
        返回:
            dict: 包含供应商信息的字典
        """
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "type": self.type,
            "contact_person": self.contact_person,
            "contact_phone": self.contact_phone,
            "contact_email": self.contact_email,
            "address": self.address,
            "tax_number": self.tax_number,
            "bank_name": self.bank_name,
            "bank_account": self.bank_account,
            "credit_level": self.credit_level,
            "credit_limit": self.credit_limit,
            "balance": self.balance,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # 将datetime对象转换为ISO格式的字符串
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
