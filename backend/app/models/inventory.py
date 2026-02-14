from sqlalchemy import Column, String, Integer, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.base import BaseModel


class Product(BaseModel):
    """
    产品模型类
    
    用于存储产品的基本信息、价格信息和库存信息
    产品是供应链管理的核心对象，与采购订单、销售订单、库存记录等紧密关联
    """
    __tablename__ = "products"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="产品编码")
    name = Column(String(200), nullable=False, index=True, comment="产品名称")
    category_id = Column(Integer, ForeignKey("product_categories.id"), comment="分类ID")
    specification = Column(String(100), comment="规格型号")
    unit = Column(String(20), comment="单位")
    purchase_price = Column(Float, default=0.0, comment="采购价")
    sale_price = Column(Float, default=0.0, comment="销售价")
    min_stock = Column(Float, default=0.0, comment="最小库存")
    max_stock = Column(Float, default=0.0, comment="最大库存")
    current_stock = Column(Float, default=0.0, comment="当前库存")
    status = Column(String(20), default="active", comment="状态：active/inactive")
    remark = Column(Text, comment="备注")
    
    category = relationship("ProductCategory", back_populates="products")
    stock_records = relationship("StockRecord", back_populates="product")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "category_id": self.category_id,
            "specification": self.specification,
            "unit": self.unit,
            "purchase_price": self.purchase_price,
            "sale_price": self.sale_price,
            "min_stock": self.min_stock,
            "max_stock": self.max_stock,
            "current_stock": self.current_stock,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class ProductCategory(BaseModel):
    """
    产品分类模型类
    
    用于对产品进行分类管理，支持多级分类结构
    产品分类可以帮助更好地组织和管理产品，方便用户快速查找和统计
    """
    __tablename__ = "product_categories"
    
    name = Column(String(100), nullable=False, comment="分类名称")
    code = Column(String(50), unique=True, index=True, comment="分类编码")
    parent_id = Column(Integer, ForeignKey("product_categories.id"), comment="父分类ID")
    sort_order = Column(Integer, default=0, comment="排序")
    description = Column(Text, comment="描述")
    status = Column(Integer, default=1, comment="状态")
    
    products = relationship("Product", back_populates="category")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "parent_id": self.parent_id,
            "sort_order": self.sort_order,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Warehouse(BaseModel):
    """
    仓库模型类
    
    用于存储仓库的基本信息和管理信息
    仓库是库存管理的物理场所，不同的仓库可以存储不同类型的产品
    """
    __tablename__ = "warehouses"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="仓库编码")
    name = Column(String(100), nullable=False, comment="仓库名称")
    type = Column(String(20), default="normal", comment="仓库类型：normal/raw/finished/return")
    address = Column(String(255), comment="地址")
    manager = Column(String(50), comment="负责人")
    phone = Column(String(20), comment="联系电话")
    capacity = Column(Float, default=0.0, comment="容量")
    status = Column(Integer, default=1, comment="状态")
    remark = Column(Text, comment="备注")
    
    stock_records = relationship("StockRecord", back_populates="warehouse")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "type": self.type,
            "address": self.address,
            "manager": self.manager,
            "phone": self.phone,
            "capacity": self.capacity,
            "status": self.status,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class StockRecord(BaseModel):
    """
    库存记录模型类
    
    用于记录所有库存变动，包括入库、出库、调拨、盘点等操作
    每次库存变动都会生成一条记录，确保库存数据的可追溯性
    """
    __tablename__ = "stock_records"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="出入库单号")
    type = Column(String(20), nullable=False, comment="类型：in/out/transfer/check/adjust")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    quantity = Column(Float, nullable=False, comment="数量")
    unit_price = Column(Float, default=0.0, comment="单价")
    amount = Column(Float, default=0.0, comment="金额")
    reference_code = Column(String(50), comment="关联单号")
    reference_type = Column(String(20), comment="关联类型：purchase/sale/transfer")
    operator_id = Column(Integer, ForeignKey("users.id"), comment="操作人")
    remark = Column(Text, comment="备注")
    
    warehouse = relationship("Warehouse", back_populates="stock_records")
    product = relationship("Product", back_populates="stock_records")
    operator = relationship("User")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "type": self.type,
            "warehouse_id": self.warehouse_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "amount": self.amount,
            "reference_code": self.reference_code,
            "reference_type": self.reference_type,
            "operator_id": self.operator_id,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class StockCheck(BaseModel):
    """
    库存盘点模型类
    
    用于记录库存盘点操作
    库存盘点是确保账实相符的重要手段，定期盘点可以发现问题并及时纠正
    """
    __tablename__ = "stock_checks"
    
    code = Column(String(50), unique=True, index=True, nullable=False, comment="盘点单号")
    warehouse_id = Column(Integer, ForeignKey("warehouses.id"), nullable=False, comment="仓库ID")
    check_date = Column(DateTime, comment="盘点日期")
    status = Column(String(20), default="pending", comment="状态：pending/completed")
    operator_id = Column(Integer, ForeignKey("users.id"), comment="盘点人")
    remark = Column(Text, comment="备注")
    
    warehouse = relationship("Warehouse")
    operator = relationship("User")
    items = relationship("StockCheckItem", back_populates="stock_check", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "warehouse_id": self.warehouse_id,
            "check_date": self.check_date.isoformat() if self.check_date else None,
            "status": self.status,
            "operator_id": self.operator_id,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class StockCheckItem(BaseModel):
    """
    库存盘点明细模型类
    
    用于记录每个产品的盘点结果
    通过对比账面数量和实际数量，发现库存差异
    """
    __tablename__ = "stock_check_items"
    
    stock_check_id = Column(Integer, ForeignKey("stock_checks.id", ondelete="CASCADE"), nullable=False, comment="盘点单ID")
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, comment="产品ID")
    book_quantity = Column(Float, comment="账面数量")
    actual_quantity = Column(Float, comment="实际数量")
    diff_quantity = Column(Float, comment="差异数量")
    remark = Column(Text, comment="备注")
    
    stock_check = relationship("StockCheck", back_populates="items")
    product = relationship("Product")
    
    def to_dict(self):
        return {
            "id": self.id,
            "stock_check_id": self.stock_check_id,
            "product_id": self.product_id,
            "book_quantity": self.book_quantity,
            "actual_quantity": self.actual_quantity,
            "diff_quantity": self.diff_quantity,
            "remark": self.remark,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
