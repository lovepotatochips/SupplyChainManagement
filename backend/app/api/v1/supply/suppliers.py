from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import PermissionChecker
from app.models import User
from app.schemas.supplier import SupplierCreate, SupplierResponse, SupplierUpdate, SupplierListResponse

router = APIRouter()


@router.get("/", response_model=SupplierListResponse)
def get_suppliers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    keyword: str = Query(None),
    current_user: User = Depends(PermissionChecker("supplier:read")),
    db: Session = Depends(get_db)
):
    """
    获取供应商列表
    
    支持分页查询和关键词搜索
    关键词可以搜索供应商名称或编码
    返回供应商列表及总数
    """
    from app.models import Supplier
    
    query = db.query(Supplier)
    if keyword:
        query = query.filter(
            (Supplier.name.contains(keyword)) |
            (Supplier.code.contains(keyword))
        )
    
    total = query.count()
    suppliers = query.offset(skip).limit(limit).all()
    return SupplierListResponse(total=total, items=suppliers)


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    current_user: User = Depends(PermissionChecker("supplier:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个供应商详情
    
    根据供应商ID返回详细信息
    如果供应商不存在，返回404错误
    """
    from app.models import Supplier
    supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return supplier


@router.post("/", response_model=SupplierResponse)
def create_supplier(
    supplier: SupplierCreate,
    current_user: User = Depends(PermissionChecker("supplier:create")),
    db: Session = Depends(get_db)
):
    """
    创建新供应商
    
    接收供应商数据，检查编码是否已存在
    如果编码不存在，创建新供应商并返回
    """
    from app.models import Supplier
    
    existing = db.query(Supplier).filter(Supplier.code == supplier.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Supplier code already exists")
    
    db_supplier = Supplier(**supplier.model_dump())
    db.add(db_supplier)
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier_update: SupplierUpdate,
    current_user: User = Depends(PermissionChecker("supplier:update")),
    db: Session = Depends(get_db)
):
    """
    更新供应商信息
    
    根据供应商ID更新数据
    只更新提供的字段
    """
    from app.models import Supplier
    
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    for field, value in supplier_update.model_dump(exclude_unset=True).items():
        setattr(db_supplier, field, value)
    
    db.commit()
    db.refresh(db_supplier)
    return db_supplier


@router.delete("/{supplier_id}")
def delete_supplier(
    supplier_id: int,
    current_user: User = Depends(PermissionChecker("supplier:delete")),
    db: Session = Depends(get_db)
):
    """
    删除供应商
    
    根据供应商ID删除供应商
    """
    from app.models import Supplier
    db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
    if not db_supplier:
        raise HTTPException(status_code=404, detail="Supplier not found")
    
    db.delete(db_supplier)
    db.commit()
    return {"message": "Supplier deleted successfully"}
