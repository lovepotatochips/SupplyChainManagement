from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class PurchaseOrder(BaseModel):
    """
    采购订单模型类
    
    用于记录采购订单的主信息
    采购订单是企业向供应商采购产品时创建的正式文件，包含了采购的所有基本信息
    """
    __tablename__ = "purchase_orders"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="采购单号")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, comment="供应商ID")
    purchase_date = Column(DateTime, comment="采购日期")
    expected_date = Column(DateTime, comment="预计到货日期")
    total_amount = Column(Float, default=0.0, comment="总金额")
    paid_amount = Column(Float, default=0.0, comment="已付金额")
    status = Column(String(20), default="pending", comment="状态：pending/approved/shipped/completed/cancelled")
    approval_status = Column(String(20), default="pending", comment="审批状态：pending/approved/rejected")
    approved_by = Column(Integer, ForeignKey("users.id"), comment="审批人")
    approved_at = Column(DateTime, comment="审批时间")
    remark = Column(Text, comment="备注")
    
    supplier = relationship("Supplier")
    approver = relationship("User", foreign_keys=[approved_by])
    items = relationship("PurchaseOrderItem", back_populates="purchase_order", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "supplier_id": self.supplier_id,
            "purchase_date": self.purchase_date.isoformat() if self.purchase_date else None,
            "expected_date": self.expected_date.isoformat() if self.expected_date else None,
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


class PurchaseOrderItem(BaseModel):
    """
    采购订单明细模型类
    
    用于记录采购订单中每个产品的详细信息
    一个采购订单可以包含多个产品，每个产品对应一条明细记录
    """
    __tablename__ = "purchase_order_items"
    
    purchase_order_id = Column(Integer, ForeignKey("purchase_orders.id", ondelete="CASCADE"), nullable=False, comment="采购单ID")
    product_code = Column(String(50), comment="产品编码")
    product_name = Column(String(200), nullable=False, comment="产品名称")
    specification = Column(String(100), comment="规格型号")
    unit = Column(String(20), comment="单位")
    quantity = Column(Float, nullable=False, comment="数量")
    unit_price = Column(Float, nullable=False, comment="单价")
    amount = Column(Float, nullable=False, comment="金额")
    received_quantity = Column(Float, default=0.0, comment="已收货数量")
    
    purchase_order = relationship("PurchaseOrder", back_populates="items")
    
    def to_dict(self):
        return {
            "id": self.id,
            "purchase_order_id": self.purchase_order_id,
            "product_code": self.product_code,
            "product_name": self.product_name,
            "specification": self.specification,
            "unit": self.unit,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "received_quantity": self.received_quantity,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
