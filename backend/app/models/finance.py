from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class CostCenter(BaseModel):
    """
    成本中心模型类
    
    用于管理企业的成本核算单位
    成本中心是财务管理中的基本核算单元，用于归集和分配成本
    支持多级结构，可以实现成本的分层次管理
    """
    __tablename__ = "cost_centers"
    
    name = Column(String(100), nullable=False, comment="成本中心名称")
    code = Column(String(50), unique=True, index=True, comment="编码")
    parent_id = Column(Integer, ForeignKey("cost_centers.id"), comment="父级ID")
    description = Column(Text, comment="描述")
    status = Column(Integer, default=1, comment="状态")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "parent_id": self.parent_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Payment(BaseModel):
    """
    付款单据模型类
    
    用于记录所有的付款和收款操作
    包括向供应商付款和从客户收款
    每笔资金流动都会产生一条付款记录
    """
    __tablename__ = "payments"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="付款单号")
    type = Column(String(20), nullable=False, comment="类型：pay/receive")
    amount = Column(Float, nullable=False, comment="金额")
    payment_method = Column(String(20), comment="付款方式：cash/transfer/check/online")
    payment_date = Column(DateTime, comment="付款日期")
    reference_code = Column(String(50), comment="关联单号")
    reference_type = Column(String(20), comment="关联类型：purchase/sale/other")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), comment="供应商ID")
    customer_id = Column(Integer, ForeignKey("customers.id"), comment="客户ID")
    bank_account = Column(String(50), comment="银行账号")
    status = Column(String(20), default="pending", comment="状态：pending/completed/cancelled")
    approval_status = Column(String(20), default="pending", comment="审批状态")
    approved_by = Column(Integer, ForeignKey("users.id"), comment="审批人")
    approved_at = Column(DateTime, comment="审批时间")
    operator_id = Column(Integer, ForeignKey("users.id"), comment="操作人")
    remark = Column(Text, comment="备注")
    
    supplier = relationship("Supplier")
    customer = relationship("Customer")
    approver = relationship("User", foreign_keys=[approved_by])
    operator = relationship("User", foreign_keys=[operator_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "type": self.type,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_date": self.payment_date.isoformat() if self.payment_date else None,
            "reference_code": self.reference_code,
            "reference_type": self.reference_type,
            "supplier_id": self.supplier_id,
            "customer_id": self.customer_id,
            "bank_account": self.bank_account,
            "status": self.status,
            "approval_status": self.approval_status,
            "approved_by": self.approved_by,
            "approved_at": self.approved_at.isoformat() if self.approved_at else None,
            "operator_id": self.operator_id,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Bill(BaseModel):
    """
    账单模型类
    
    用于记录应收账款和应付账款
    应收账款是客户欠企业的钱，应付账款是企业欠供应商的钱
    帮助企业跟踪和管理所有未结清的账务
    """
    __tablename__ = "bills"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="单据号")
    type = Column(String(20), nullable=False, comment="类型：receivable/payable")
    amount = Column(Float, nullable=False, comment="金额")
    bill_date = Column(DateTime, comment="单据日期")
    due_date = Column(DateTime, comment="到期日期")
    reference_code = Column(String(50), comment="关联单号")
    reference_type = Column(String(20), comment="关联类型")
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), comment="供应商ID")
    customer_id = Column(Integer, ForeignKey("customers.id"), comment="客户ID")
    paid_amount = Column(Float, default=0.0, comment="已付金额")
    remaining_amount = Column(Float, comment="剩余金额")
    status = Column(String(20), default="unpaid", comment="状态：unpaid/partial/paid/overdue")
    remark = Column(Text, comment="备注")
    
    supplier = relationship("Supplier")
    customer = relationship("Customer")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "type": self.type,
            "amount": self.amount,
            "bill_date": self.bill_date.isoformat() if self.bill_date else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reference_code": self.reference_code,
            "reference_type": self.reference_type,
            "supplier_id": self.supplier_id,
            "customer_id": self.customer_id,
            "paid_amount": self.paid_amount,
            "remaining_amount": self.remaining_amount,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Account(BaseModel):
    """
    银行账户模型类
    
    用于管理企业的所有银行账户和现金账户
    包括企业账户、个人账户、在线支付账户等
    用于跟踪资金流动和账户余额
    """
    __tablename__ = "accounts"
    
    name = Column(String(100), nullable=False, comment="账户名称")
    code = Column(String(50), unique=True, index=True, comment="账户编码")
    type = Column(String(20), comment="账户类型：bank/cash/online")
    bank_name = Column(String(100), comment="开户银行")
    account_number = Column(String(50), comment="账号")
    balance = Column(Float, default=0.0, comment="余额")
    status = Column(Integer, default=1, comment="状态")
    remark = Column(Text, comment="备注")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "bank_name": self.bank_name,
            "account_number": self.account_number,
            "balance": self.balance,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
