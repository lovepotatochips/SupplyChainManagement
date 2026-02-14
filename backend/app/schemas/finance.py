from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PaymentBase(BaseModel):
    """
    付款单据基础模型
    
    用于定义付款单据的基本字段
    付款单据记录企业的付款和收款操作
    """
    code: str = Field(..., max_length=50)
    type: str
    amount: float
    payment_method: Optional[str] = Field(None, max_length=20)
    payment_date: Optional[datetime] = None
    reference_code: Optional[str] = Field(None, max_length=50)
    reference_type: Optional[str] = Field(None, max_length=20)
    supplier_id: Optional[int] = None
    customer_id: Optional[int] = None
    bank_account: Optional[str] = Field(None, max_length=50)
    remark: Optional[str] = None


class PaymentCreate(PaymentBase):
    """
    付款单据创建模型
    
    继承自PaymentBase，用于创建新的付款单据
    """
    pass


class PaymentUpdate(BaseModel):
    """
    付款单据更新模型
    
    用于更新付款单据信息
    所有字段都是可选的
    """
    payment_method: Optional[str] = Field(None, max_length=20)
    payment_date: Optional[datetime] = None
    bank_account: Optional[str] = Field(None, max_length=50)
    status: Optional[str] = None
    remark: Optional[str] = None


class PaymentResponse(PaymentBase):
    """
    付款单据响应模型
    
    继承自PaymentBase，并添加了只读字段
    用于API响应返回付款单据数据
    """
    id: int
    status: str
    approval_status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    operator_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PaymentListResponse(BaseModel):
    """
    付款单据列表响应模型
    
    用于返回分页的付款单据列表
    包含总数和单据列表
    """
    total: int
    items: list[PaymentResponse]


class PaymentApprove(BaseModel):
    """
    付款审批模型
    
    用于审批付款单据
    """
    approval_status: str
    remark: Optional[str] = None


class BillBase(BaseModel):
    """
    账单基础模型
    
    用于定义账单的基本字段
    账单记录应收账款和应付账款
    """
    code: str = Field(..., max_length=50)
    type: str
    amount: float
    bill_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    reference_code: Optional[str] = Field(None, max_length=50)
    reference_type: Optional[str] = Field(None, max_length=20)
    supplier_id: Optional[int] = None
    customer_id: Optional[int] = None
    remark: Optional[str] = None


class BillCreate(BillBase):
    """
    账单创建模型
    
    继承自BillBase，用于创建新的账单
    """
    pass


class BillUpdate(BaseModel):
    """
    账单更新模型
    
    用于更新账单信息
    """
    bill_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class BillResponse(BillBase):
    """
    账单响应模型
    
    继承自BillBase，并添加了只读字段
    用于API响应返回账单数据
    """
    id: int
    paid_amount: float
    remaining_amount: float
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class BillListResponse(BaseModel):
    """
    账单列表响应模型
    
    用于返回分页的账单列表
    """
    total: int
    items: list[BillResponse]


class AccountBase(BaseModel):
    """
    银行账户基础模型
    
    用于定义银行账户的基本字段
    银行账户管理企业的所有资金账户
    """
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    type: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=100)
    account_number: Optional[str] = Field(None, max_length=50)
    status: int = 1
    remark: Optional[str] = None


class AccountCreate(AccountBase):
    """
    银行账户创建模型
    
    继承自AccountBase，用于创建新的银行账户
    """
    pass


class AccountUpdate(BaseModel):
    """
    银行账户更新模型
    
    用于更新银行账户信息
    """
    name: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, max_length=20)
    bank_name: Optional[str] = Field(None, max_length=100)
    account_number: Optional[str] = Field(None, max_length=50)
    status: Optional[int] = None
    remark: Optional[str] = None


class AccountResponse(AccountBase):
    """
    银行账户响应模型
    
    继承自AccountBase，并添加了只读字段
    用于API响应返回银行账户数据
    """
    id: int
    balance: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CostCenterBase(BaseModel):
    """
    成本中心基础模型
    
    用于定义成本中心的基本字段
    成本中心是财务管理中的基本核算单元
    """
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    parent_id: Optional[int] = None
    description: Optional[str] = None
    status: int = 1


class CostCenterCreate(CostCenterBase):
    """
    成本中心创建模型
    
    继承自CostCenterBase，用于创建新的成本中心
    """
    pass


class CostCenterUpdate(BaseModel):
    """
    成本中心更新模型
    
    用于更新成本中心信息
    """
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class CostCenterResponse(CostCenterBase):
    """
    成本中心响应模型
    
    继承自CostCenterBase，并添加了只读字段
    用于API响应返回成本中心数据
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
