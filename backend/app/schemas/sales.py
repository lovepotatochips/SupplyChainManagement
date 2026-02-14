from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class CustomerBase(BaseModel):
    """
    客户基础模型
    
    用于定义客户的基本字段
    客户是企业销售业务的重要伙伴
    """
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    type: str = Field(default="normal", max_length=20)
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=255)
    tax_number: Optional[str] = Field(None, max_length=50)
    bank_name: Optional[str] = Field(None, max_length=100)
    bank_account: Optional[str] = Field(None, max_length=50)
    credit_limit: float = 0.0
    remark: Optional[str] = None


class CustomerCreate(CustomerBase):
    """
    客户创建模型
    
    继承自CustomerBase，用于创建新客户
    """
    pass


class CustomerUpdate(BaseModel):
    """
    客户更新模型
    
    用于更新客户信息
    所有字段都是可选的
    """
    name: Optional[str] = Field(None, max_length=200)
    type: Optional[str] = Field(None, max_length=20)
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=255)
    tax_number: Optional[str] = Field(None, max_length=50)
    bank_name: Optional[str] = Field(None, max_length=100)
    bank_account: Optional[str] = Field(None, max_length=50)
    credit_limit: Optional[float] = None
    status: Optional[bool] = None
    remark: Optional[str] = None


class CustomerResponse(CustomerBase):
    """
    客户响应模型
    
    继承自CustomerBase，并添加了只读字段
    用于API响应返回客户数据
    """
    id: int
    balance: float
    status: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class CustomerListResponse(BaseModel):
    """
    客户列表响应模型
    
    用于返回分页的客户列表
    """
    total: int
    items: List[CustomerResponse]


class SalesOrderItemBase(BaseModel):
    """
    销售订单明细基础模型
    
    用于定义销售订单明细的基本字段
    一个销售订单包含多个产品明细
    """
    product_code: Optional[str] = Field(None, max_length=50)
    product_name: str = Field(..., max_length=200)
    specification: Optional[str] = Field(None, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    quantity: float
    unit_price: float


class SalesOrderItemCreate(SalesOrderItemBase):
    """
    销售订单明细创建模型
    
    继承自SalesOrderItemBase，用于创建销售订单明细
    """
    pass


class SalesOrderItemResponse(SalesOrderItemBase):
    """
    销售订单明细响应模型
    
    继承自SalesOrderItemBase，并添加了只读字段
    用于API响应返回销售订单明细数据
    """
    id: int
    sales_order_id: int
    amount: float
    shipped_quantity: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SalesOrderBase(BaseModel):
    """
    销售订单基础模型
    
    用于定义销售订单的基本字段
    销售订单是企业向客户销售产品时创建的正式文件
    """
    customer_id: int
    sale_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    remark: Optional[str] = None


class SalesOrderCreate(SalesOrderBase):
    """
    销售订单创建模型
    
    继承自SalesOrderBase，并添加了明细列表
    用于创建销售订单
    """
    items: List[SalesOrderItemCreate]


class SalesOrderUpdate(BaseModel):
    """
    销售订单更新模型
    
    用于更新销售订单信息
    """
    sale_date: Optional[datetime] = None
    delivery_date: Optional[datetime] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class SalesOrderResponse(SalesOrderBase):
    """
    销售订单响应模型
    
    继承自SalesOrderBase，并添加了只读字段
    用于API响应返回销售订单数据
    """
    id: int
    code: str
    total_amount: float
    paid_amount: float
    status: str
    approval_status: str
    approved_by: Optional[int] = None
    approved_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SalesOrderDetailResponse(SalesOrderResponse):
    """
    销售订单详情响应模型
    
    继承自SalesOrderResponse，并添加了明细列表
    用于返回销售订单的完整信息
    """
    items: List[SalesOrderItemResponse]


class SalesOrderListResponse(BaseModel):
    """
    销售订单列表响应模型
    
    用于返回分页的销售订单列表
    """
    total: int
    items: List[SalesOrderResponse]


class SalesOrderApprove(BaseModel):
    """
    销售订单审批模型
    
    用于审批销售订单
    """
    approval_status: str
    remark: Optional[str] = None
