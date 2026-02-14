from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PurchaseOrderItemBase(BaseModel):
    """
    采购订单明细基础模型
    
    用于定义采购订单明细的基本字段
    一个采购订单包含多个产品明细
    """
    product_code: Optional[str] = Field(None, max_length=50)
    product_name: str = Field(..., max_length=200)
    specification: Optional[str] = Field(None, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    quantity: float
    unit_price: float


class PurchaseOrderItemCreate(PurchaseOrderItemBase):
    """
    采购订单明细创建模型
    
    继承自PurchaseOrderItemBase，用于创建采购订单明细
    """
    pass


class PurchaseOrderItemResponse(PurchaseOrderItemBase):
    """
    采购订单明细响应模型
    
    继承自PurchaseOrderItemBase，并添加了只读字段
    用于API响应返回采购订单明细数据
    """
    id: int
    purchase_order_id: int
    amount: float
    received_quantity: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseOrderBase(BaseModel):
    """
    采购订单基础模型
    
    用于定义采购订单的基本字段
    采购订单是企业向供应商采购产品时创建的正式文件
    """
    supplier_id: int
    purchase_date: Optional[datetime] = None
    expected_date: Optional[datetime] = None
    remark: Optional[str] = None


class PurchaseOrderCreate(PurchaseOrderBase):
    """
    采购订单创建模型
    
    继承自PurchaseOrderBase，并添加了明细列表
    用于创建采购订单
    """
    items: List[PurchaseOrderItemCreate]


class PurchaseOrderUpdate(BaseModel):
    """
    采购订单更新模型
    
    用于更新采购订单信息
    """
    purchase_date: Optional[datetime] = None
    expected_date: Optional[datetime] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class PurchaseOrderResponse(PurchaseOrderBase):
    """
    采购订单响应模型
    
    继承自PurchaseOrderBase，并添加了只读字段
    用于API响应返回采购订单数据
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


class PurchaseOrderDetailResponse(PurchaseOrderResponse):
    """
    采购订单详情响应模型
    
    继承自PurchaseOrderResponse，并添加了明细列表
    用于返回采购订单的完整信息
    """
    items: List[PurchaseOrderItemResponse]


class PurchaseOrderListResponse(BaseModel):
    """
    采购订单列表响应模型
    
    用于返回分页的采购订单列表
    """
    total: int
    items: List[PurchaseOrderResponse]


class PurchaseOrderApprove(BaseModel):
    """
    采购订单审批模型
    
    用于审批采购订单
    """
    approval_status: str
    remark: Optional[str] = None
