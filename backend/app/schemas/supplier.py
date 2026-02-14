from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime


class SupplierBase(BaseModel):
    """
    供应商基础模型
    
    用于定义供应商的基本字段
    供应商是供应链管理中的重要角色，与采购订单相关联
    """
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    type: str = Field(default="manufacturer", max_length=20)
    contact_person: Optional[str] = Field(None, max_length=50)
    contact_phone: Optional[str] = Field(None, max_length=20)
    contact_email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=255)
    tax_number: Optional[str] = Field(None, max_length=50)
    bank_name: Optional[str] = Field(None, max_length=100)
    bank_account: Optional[str] = Field(None, max_length=50)
    credit_level: str = Field(default="A", max_length=20)
    credit_limit: float = 0.0
    remark: Optional[str] = None


class SupplierCreate(SupplierBase):
    """
    供应商创建模型
    
    继承自SupplierBase，用于创建新供应商
    """
    pass


class SupplierUpdate(BaseModel):
    """
    供应商更新模型
    
    用于更新供应商信息
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
    credit_level: Optional[str] = Field(None, max_length=20)
    credit_limit: Optional[float] = None
    status: Optional[bool] = None
    remark: Optional[str] = None


class SupplierResponse(SupplierBase):
    """
    供应商响应模型
    
    继承自SupplierBase，并添加了只读字段
    用于API响应返回供应商数据
    """
    id: int
    balance: float
    status: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SupplierListResponse(BaseModel):
    """
    供应商列表响应模型
    
    用于返回分页的供应商列表
    """
    total: int
    items: list[SupplierResponse]
