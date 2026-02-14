from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    """
    产品基础模型
    
    用于定义产品的基本字段
    产品是供应链管理的核心对象
    """
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=200)
    category_id: Optional[int] = None
    specification: Optional[str] = Field(None, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    purchase_price: float = 0.0
    sale_price: float = 0.0
    min_stock: float = 0.0
    max_stock: float = 0.0
    status: str = Field(default="active", max_length=20)
    remark: Optional[str] = None


class ProductCreate(ProductBase):
    """
    产品创建模型
    
    继承自ProductBase，用于创建新产品
    """
    pass


class ProductUpdate(BaseModel):
    """
    产品更新模型
    
    用于更新产品信息
    所有字段都是可选的
    """
    name: Optional[str] = Field(None, max_length=200)
    category_id: Optional[int] = None
    specification: Optional[str] = Field(None, max_length=100)
    unit: Optional[str] = Field(None, max_length=20)
    purchase_price: Optional[float] = None
    sale_price: Optional[float] = None
    min_stock: Optional[float] = None
    max_stock: Optional[float] = None
    status: Optional[str] = None
    remark: Optional[str] = None


class ProductResponse(ProductBase):
    """
    产品响应模型
    
    继承自ProductBase，并添加了只读字段
    用于API响应返回产品数据
    """
    id: int
    current_stock: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """
    产品列表响应模型
    
    用于返回分页的产品列表
    """
    total: int
    items: List[ProductResponse]


class ProductCategoryBase(BaseModel):
    """
    产品分类基础模型
    
    用于定义产品分类的基本字段
    产品分类用于组织和管理产品
    """
    name: str = Field(..., max_length=100)
    code: str = Field(..., max_length=50)
    parent_id: Optional[int] = None
    sort_order: int = 0
    description: Optional[str] = None
    status: int = 1


class ProductCategoryCreate(ProductCategoryBase):
    """
    产品分类创建模型
    
    继承自ProductCategoryBase，用于创建新产品分类
    """
    pass


class ProductCategoryUpdate(BaseModel):
    """
    产品分类更新模型
    
    用于更新产品分类信息
    """
    name: Optional[str] = Field(None, max_length=100)
    parent_id: Optional[int] = None
    sort_order: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None


class ProductCategoryResponse(ProductCategoryBase):
    """
    产品分类响应模型
    
    继承自ProductCategoryBase，并添加了只读字段
    用于API响应返回产品分类数据
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class WarehouseBase(BaseModel):
    """
    仓库基础模型
    
    用于定义仓库的基本字段
    仓库是库存管理的物理场所
    """
    code: str = Field(..., max_length=50)
    name: str = Field(..., max_length=100)
    type: str = Field(default="normal", max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    manager: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    capacity: float = 0.0
    status: int = 1
    remark: Optional[str] = None


class WarehouseCreate(WarehouseBase):
    """
    仓库创建模型
    
    继承自WarehouseBase，用于创建新仓库
    """
    pass


class WarehouseUpdate(BaseModel):
    """
    仓库更新模型
    
    用于更新仓库信息
    """
    name: Optional[str] = Field(None, max_length=100)
    type: Optional[str] = Field(None, max_length=20)
    address: Optional[str] = Field(None, max_length=255)
    manager: Optional[str] = Field(None, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    capacity: Optional[float] = None
    status: Optional[int] = None
    remark: Optional[str] = None


class WarehouseResponse(WarehouseBase):
    """
    仓库响应模型
    
    继承自WarehouseBase，并添加了只读字段
    用于API响应返回仓库数据
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockRecordBase(BaseModel):
    """
    库存记录基础模型
    
    用于定义库存记录的基本字段
    库存记录记录所有的库存变动
    """
    type: str
    warehouse_id: int
    product_id: int
    quantity: float
    unit_price: float = 0.0
    reference_code: Optional[str] = Field(None, max_length=50)
    reference_type: Optional[str] = Field(None, max_length=20)
    remark: Optional[str] = None


class StockRecordCreate(StockRecordBase):
    """
    库存记录创建模型
    
    继承自StockRecordBase，用于创建新的库存记录
    """
    pass


class StockRecordResponse(StockRecordBase):
    """
    库存记录响应模型
    
    继承自StockRecordBase，并添加了只读字段
    用于API响应返回库存记录数据
    """
    id: int
    code: str
    amount: float
    operator_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockRecordListResponse(BaseModel):
    """
    库存记录列表响应模型
    
    用于返回分页的库存记录列表
    """
    total: int
    items: List[StockRecordResponse]


class StockCheckItemBase(BaseModel):
    """
    库存盘点明细基础模型
    
    用于定义库存盘点明细的基本字段
    盘点明细记录每个产品的盘点结果
    """
    product_id: int
    book_quantity: Optional[float] = None
    actual_quantity: Optional[float] = None
    remark: Optional[str] = None


class StockCheckItemCreate(StockCheckItemBase):
    """
    库存盘点明细创建模型
    
    继承自StockCheckItemBase，用于创建库存盘点明细
    """
    pass


class StockCheckItemResponse(StockCheckItemBase):
    """
    库存盘点明细响应模型
    
    继承自StockCheckItemBase，并添加了只读字段
    用于API响应返回库存盘点明细数据
    """
    id: int
    stock_check_id: int
    diff_quantity: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockCheckBase(BaseModel):
    """
    库存盘点基础模型
    
    用于定义库存盘点的基本字段
    库存盘点用于确保账实相符
    """
    warehouse_id: int
    check_date: Optional[datetime] = None
    remark: Optional[str] = None


class StockCheckCreate(StockCheckBase):
    """
    库存盘点创建模型
    
    继承自StockCheckBase，并添加了明细列表
    用于创建库存盘点
    """
    items: List[StockCheckItemCreate]


class StockCheckUpdate(BaseModel):
    """
    库存盘点更新模型
    
    用于更新库存盘点信息
    """
    status: Optional[str] = None
    remark: Optional[str] = None


class StockCheckResponse(StockCheckBase):
    """
    库存盘点响应模型
    
    继承自StockCheckBase，并添加了只读字段
    用于API响应返回库存盘点数据
    """
    id: int
    code: str
    status: str
    operator_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class StockCheckDetailResponse(StockCheckResponse):
    """
    库存盘点详情响应模型
    
    继承自StockCheckResponse，并添加了明细列表
    用于返回库存盘点的完整信息
    """
    items: List[StockCheckItemResponse]
