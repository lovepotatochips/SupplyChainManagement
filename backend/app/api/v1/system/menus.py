from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.session import get_db
from app.models import Menu
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from app.core.deps import get_current_user
from app.models import User

router = APIRouter()


@router.get("", response_model=List[MenuResponse])
def get_menus(
    parent_id: Optional[int] = Query(None, description="父菜单ID"),
    status: Optional[bool] = Query(None, description="状态"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取菜单列表
    
    支持按父菜单ID和状态筛选
    返回按排序和ID排序的菜单列表
    """
    query = db.query(Menu)
    
    if parent_id is not None:
        query = query.filter(Menu.parent_id == parent_id)
    
    if status is not None:
        query = query.filter(Menu.status == status)
    
    menus = query.order_by(Menu.sort_order, Menu.id).all()
    return menus


@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    获取单个菜单详情
    
    根据菜单ID返回菜单的详细信息
    如果菜单不存在，返回404错误
    """
    menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    return menu


@router.post("", response_model=MenuResponse)
def create_menu(
    menu: MenuCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    创建新菜单
    
    接收菜单数据，检查编码是否已存在
    如果编码不存在，创建新菜单并返回
    """
    existing_code = db.query(Menu).filter(Menu.code == menu.code).first()
    if existing_code:
        raise HTTPException(status_code=400, detail="菜单编码已存在")
    
    db_menu = Menu(**menu.model_dump())
    db.add(db_menu)
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.put("/{menu_id}", response_model=MenuResponse)
def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    更新菜单信息
    
    根据菜单ID更新菜单数据
    如果修改了编码，需要检查新编码是否已存在
    """
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    if menu.code != db_menu.code:
        existing_code = db.query(Menu).filter(Menu.code == menu.code).first()
        if existing_code:
            raise HTTPException(status_code=400, detail="菜单编码已存在")
    
    for key, value in menu.model_dump(exclude_unset=True).items():
        setattr(db_menu, key, value)
    
    db.commit()
    db.refresh(db_menu)
    return db_menu


@router.delete("/{menu_id}")
def delete_menu(
    menu_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    删除菜单
    
    根据菜单ID删除菜单
    如果菜单有子菜单，不允许删除
    """
    db_menu = db.query(Menu).filter(Menu.id == menu_id).first()
    if not db_menu:
        raise HTTPException(status_code=404, detail="菜单不存在")
    
    if db_menu.children:
        raise HTTPException(status_code=400, detail="请先删除子菜单")
    
    db.delete(db_menu)
    db.commit()
    return {"message": "删除成功"}
