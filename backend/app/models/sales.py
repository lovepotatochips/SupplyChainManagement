from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Customer(BaseModel):
    """
    客户模型类
    
    用于存储客户的基本信息和财务信息
    客户是企业销售业务的重要伙伴，与销售订单、应收账款等紧密关联
    """
    __tablename__ = "customers"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="客户编码")
    name = Column(String(200), nullable=False, index=True, comment="客户名称")
    type = Column(String(20), default="normal", comment="客户类型：normal/vip/wholesale/retail")
    contact_person = Column(String(50), comment="联系人")
    contact_phone = Column(String(20), comment="联系电话")
    contact_email = Column(String(100), comment="联系邮箱")
    address = Column(String(255), comment="地址")
    tax_number = Column(String(50), comment="税号")
    bank_name = Column(String(100), comment="开户银行")
    bank_account = Column(String(50), comment="银行账号")
    credit_limit = Column(Float, default=0.0, comment="信用额度")
    balance = Column(Float, default=0.0, comment="余额")
    status = Column(Boolean, default=True, comment="状态")
    remark = Column(Text, comment="备注")
    
    sales_orders = relationship("SalesOrder", back_populates="customer")
    
    def to_dict(self):
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
            "credit_limit": self.credit_limit,
            "balance": self.balance,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class SalesOrder(BaseModel):
    """
    销售订单模型类
    
    用于记录销售订单的主信息
    销售订单是企业向客户销售产品时创建的正式文件，包含了销售的所有基本信息
    """
    __tablename__ = "sales_orders"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="销售单号")
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False, comment="客户ID")
    sale_date = Column(DateTime, comment="销售日期")
    delivery_date = Column(DateTime, comment="交货日期")
    total_amount = Column(Float, default=0.0, comment="总金额")
    paid_amount = Column(Float, default=0.0, comment="已付金额")
    status = Column(String(20), default="pending", comment="状态：pending/shipped/delivered/completed/cancelled")
    approval_status = Column(String(20), default="pending", comment="审批状态")
    approved_by = Column(Integer, ForeignKey("users.id"), comment="审批人")
    approved_at = Column(DateTime, comment="审批时间")
    remark = Column(Text, comment="备注")
    
    customer = relationship("Customer", back_populates="sales_orders")
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("SalesOrderItem", back_populates="sales_order", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "customer_id": self.customer_id,
            "sale_date": self.sale_date.isoformat() if self.sale_date else None,
            "delivery_date": self.delivery_date.isoformat() if self.delivery_date else None,
            "total_amount": self.total_amount,
            "paid_amount": self.paid_amount,
            "status": self.status,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class SalesOrderItem(BaseModel):
    """
    销售订单明细模型类
    
    用于记录销售订单中每个产品的详细信息
    一个销售订单可以包含多个产品，每个产品对应一条明细记录
    """
    __tablename__ = "sales_order_items"
    
    sales_order_id = Column(Integer, ForeignKey("sales_orders.id", ondelete="CASCADE"), nullable=False, comment="销售单ID")
    product_code = Column(String(50), comment="产品编码")
    product_name = Column(String(200), nullable=False, comment="产品名称")
    specification = Column(String(100), comment="规格型号")
    unit = Column(String(20), comment="单位")
    quantity = Column(Float, nullable=False, comment="数量")
    unit_price = Column(Float, nullable=False, comment="单价")
    amount = Column(Float, nullable=False, comment="金额")
    shipped_quantity = Column(Float, default=0.0, comment="已发货数量")
    
    sales_order = relationship("SalesOrder", back_populates="items")
    
    def to_dict(self):
        return {
            "id": self.id,
            "sales_order_id": self.sales_order_id,
            "product_code": self.product_code,
            "product_name": self.product_name,
            "specification": self.specification,
            "unit": self.unit,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "shipped_quantity": self.shipped_quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
