from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import PermissionChecker
from app.models import User
from app.schemas.inventory import ProductCreate, ProductResponse, ProductUpdate, ProductListResponse, WarehouseCreate, WarehouseResponse, WarehouseUpdate, StockRecordCreate, StockRecordResponse, StockRecordListResponse, StockCheckCreate, StockCheckResponse, StockCheckUpdate, StockCheckDetailResponse

router = APIRouter()


@router.get("/products/", response_model=ProductListResponse)
def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    keyword: str = Query(None),
    category_id: int = Query(None),
    current_user: User = Depends(PermissionChecker("product:read")),
    db: Session = Depends(get_db)
):
    """
    获取产品列表
    
    支持分页查询和关键词搜索
    关键词可以搜索产品名称或编码
    可按分类ID筛选
    返回产品列表及总数
    """
    from app.models import Product
    
    query = db.query(Product)
    if keyword:
        query = query.filter(
            (Product.name.contains(keyword)) |
            (Product.code.contains(keyword))
        )
    if category_id:
        query = query.filter(Product.category_id == category_id)
    
    total = query.count()
    products = query.offset(skip).limit(limit).all()
    return ProductListResponse(total=total, items=products)


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    current_user: User = Depends(PermissionChecker("product:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个产品详情
    
    根据产品ID返回详细信息
    如果产品不存在，返回404错误
    """
    from app.models import Product
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/products/", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    current_user: User = Depends(PermissionChecker("product:create")),
    db: Session = Depends(get_db)
):
    """
    创建新产品
    
    接收产品数据，检查编码是否已存在
    如果编码不存在，创建新产品并返回
    """
    from app.models import Product
    
    existing = db.query(Product).filter(Product.code == product.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Product code already exists")
    
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    current_user: User = Depends(PermissionChecker("product:update")),
    db: Session = Depends(get_db)
):
    """
    更新产品信息
    
    根据产品ID更新数据
    只更新提供的字段
    """
    from app.models import Product
    
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for field, value in product_update.model_dump(exclude_unset=True).items():
        setattr(db_product, field, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    current_user: User = Depends(PermissionChecker("product:delete")),
    db: Session = Depends(get_db)
):
    """
    删除产品
    
    根据产品ID删除产品
    """
    from app.models import Product
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}


@router.get("/warehouses/", response_model=List[WarehouseResponse])
def get_warehouses(
    current_user: User = Depends(PermissionChecker("warehouse:read")),
    db: Session = Depends(get_db)
):
    """
    获取仓库列表
    
    返回所有仓库信息
    """
    from app.models import Warehouse
    warehouses = db.query(Warehouse).all()
    return warehouses


@router.post("/warehouses/", response_model=WarehouseResponse)
def create_warehouse(
    warehouse: WarehouseCreate,
    current_user: User = Depends(PermissionChecker("warehouse:create")),
    db: Session = Depends(get_db)
):
    """
    创建新仓库
    
    接收仓库数据，检查编码是否已存在
    """
    from app.models import Warehouse
    
    existing = db.query(Warehouse).filter(Warehouse.code == warehouse.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Warehouse code already exists")
    
    db_warehouse = Warehouse(**warehouse.model_dump())
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


@router.put("/warehouses/{warehouse_id}", response_model=WarehouseResponse)
def update_warehouse(
    warehouse_id: int,
    warehouse_update: WarehouseUpdate,
    current_user: User = Depends(PermissionChecker("warehouse:update")),
    db: Session = Depends(get_db)
):
    """
    更新仓库信息
    
    根据仓库ID更新数据
    只更新提供的字段
    """
    from app.models import Warehouse
    
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    for field, value in warehouse_update.model_dump(exclude_unset=True).items():
        setattr(db_warehouse, field, value)
    
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


@router.delete("/warehouses/{warehouse_id}")
def delete_warehouse(
    warehouse_id: int,
    current_user: User = Depends(PermissionChecker("warehouse:delete")),
    db: Session = Depends(get_db)
):
    """
    删除仓库
    
    根据仓库ID删除仓库
    """
    from app.models import Warehouse
    db_warehouse = db.query(Warehouse).filter(Warehouse.id == warehouse_id).first()
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Warehouse not found")
    
    db.delete(db_warehouse)
    db.commit()
    return {"message": "Warehouse deleted successfully"}


@router.get("/stock-records/", response_model=StockRecordListResponse)
def get_stock_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    warehouse_id: int = Query(None),
    type: str = Query(None),
    current_user: User = Depends(PermissionChecker("stock:read")),
    db: Session = Depends(get_db)
):
    """
    获取库存记录列表
    
    支持分页查询，可按仓库ID和类型筛选
    返回库存记录列表及总数
    """
    from app.models import StockRecord
    
    query = db.query(StockRecord)
    if warehouse_id:
        query = query.filter(StockRecord.warehouse_id == warehouse_id)
    if type:
        query = query.filter(StockRecord.type == type)
    
    total = query.count()
    records = query.order_by(StockRecord.created_at.desc()).offset(skip).limit(limit).all()
    return StockRecordListResponse(total=total, items=records)


@router.post("/stock-records/", response_model=StockRecordResponse)
def create_stock_record(
    record: StockRecordCreate,
    current_user: User = Depends(PermissionChecker("stock:create")),
    db: Session = Depends(get_db)
):
    """
    创建库存记录
    
    自动生成记录编码
    计算金额（数量×单价）
    根据类型更新产品库存：入库增加，出库减少
    出库时检查库存是否充足
    """
    from app.models import StockRecord, Product
    from app.utils.helpers import generate_code
    
    product = db.query(Product).filter(Product.id == record.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    code = generate_code("SR")
    amount = record.quantity * record.unit_price
    
    db_record = StockRecord(
        code=code,
        operator_id=current_user.id,
        amount=amount,
        **record.model_dump()
    )
    db.add(db_record)
    
    if record.type == "in":
        product.current_stock += record.quantity
    elif record.type == "out":
        if product.current_stock < record.quantity:
            raise HTTPException(status_code=400, detail="Insufficient stock")
        product.current_stock -= record.quantity
    
    db.commit()
    db.refresh(db_record)
    return db_record


@router.get("/stock-checks/", response_model=List[StockCheckResponse])
def get_stock_checks(
    current_user: User = Depends(PermissionChecker("stock:read")),
    db: Session = Depends(get_db)
):
    """
    获取库存盘点列表
    
    返回所有库存盘点记录
    """
    from app.models import StockCheck
    checks = db.query(StockCheck).all()
    return checks


@router.post("/stock-checks/", response_model=StockCheckResponse)
def create_stock_check(
    check: StockCheckCreate,
    current_user: User = Depends(PermissionChecker("stock:create")),
    db: Session = Depends(get_db)
):
    """
    创建库存盘点
    
    自动生成盘点编码
    为每个产品计算盘点差异（实际数量-账面数量）
    账面数量默认使用当前库存
    """
    from app.models import StockCheck, StockCheckItem, Product
    from app.utils.helpers import generate_code
    
    code = generate_code("SC")
    
    db_check = StockCheck(
        code=code,
        operator_id=current_user.id,
        **check.model_dump(exclude={"items"})
    )
    db.add(db_check)
    db.flush()
    
    for item in check.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product:
            diff = (item.actual_quantity or 0) - (item.book_quantity or 0)
            db_item = StockCheckItem(
                stock_check_id=db_check.id,
                **item.model_dump(),
                diff_quantity=diff,
                book_quantity=item.book_quantity or product.current_stock
            )
            db.add(db_item)
    
    db.commit()
    db.refresh(db_check)
    return db_check


@router.put("/stock-checks/{check_id}/complete")
def complete_stock_check(
    check_id: int,
    current_user: User = Depends(PermissionChecker("stock:update")),
    db: Session = Depends(get_db)
):
    """
    完成库存盘点
    
    更新盘点状态为已完成
    根据盘点差异调整产品库存
    """
    from app.models import StockCheck, StockCheckItem, Product
    
    db_check = db.query(StockCheck).filter(StockCheck.id == check_id).first()
    if not db_check:
        raise HTTPException(status_code=404, detail="Stock check not found")
    
    if db_check.status != "pending":
        raise HTTPException(status_code=400, detail="Stock check already processed")
    
    db_check.status = "completed"
    
    for item in db_check.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and item.diff_quantity:
            product.current_stock += item.diff_quantity
    
    db.commit()
    return {"message": "Stock check completed successfully"}
