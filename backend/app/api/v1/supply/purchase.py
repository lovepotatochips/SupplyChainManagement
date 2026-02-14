from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import PermissionChecker
from app.models import User
from app.schemas.purchase import PurchaseOrderCreate, PurchaseOrderResponse, PurchaseOrderUpdate, PurchaseOrderListResponse, PurchaseOrderDetailResponse, PurchaseOrderApprove

router = APIRouter()


@router.get("/", response_model=PurchaseOrderListResponse)
def get_purchase_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    supplier_id: int = Query(None),
    current_user: User = Depends(PermissionChecker("purchase:read")),
    db: Session = Depends(get_db)
):
    """
    获取采购订单列表
    
    支持分页查询，可按状态和供应商ID筛选
    返回采购订单列表及总数
    """
    from app.models import PurchaseOrder
    
    query = db.query(PurchaseOrder)
    if status:
        query = query.filter(PurchaseOrder.status == status)
    if supplier_id:
        query = query.filter(PurchaseOrder.supplier_id == supplier_id)
    
    total = query.count()
    orders = query.order_by(PurchaseOrder.created_at.desc()).offset(skip).limit(limit).all()
    return PurchaseOrderListResponse(total=total, items=orders)


@router.get("/{order_id}", response_model=PurchaseOrderDetailResponse)
def get_purchase_order(
    order_id: int,
    current_user: User = Depends(PermissionChecker("purchase:read")),
    db: Session = Depends(get_db)
):
    """
    获取采购订单详情
    
    根据订单ID返回订单详细信息，包括订单明细
    如果订单不存在，返回404错误
    """
    from app.models import PurchaseOrder
    
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    return order


@router.post("/", response_model=PurchaseOrderResponse)
def create_purchase_order(
    order: PurchaseOrderCreate,
    current_user: User = Depends(PermissionChecker("purchase:create")),
    db: Session = Depends(get_db)
):
    """
    创建新的采购订单
    
    自动生成订单编码（PO前缀）
    计算订单总金额（所有明细金额之和）
    创建订单和订单明细
    """
    from app.models import PurchaseOrder, PurchaseOrderItem
    from app.utils.helpers import generate_code
    
    code = generate_code("PO")
    
    total_amount = sum(item.quantity * item.unit_price for item in order.items)
    
    db_order = PurchaseOrder(
        code=code,
        supplier_id=order.supplier_id,
        purchase_date=order.purchase_date,
        expected_date=order.expected_date,
        total_amount=total_amount,
        remark=order.remark
    )
    db.add(db_order)
    db.flush()
    
    for item in order.items:
        db_item = PurchaseOrderItem(
            purchase_order_id=db_order.id,
            **item.model_dump(),
            amount=item.quantity * item.unit_price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.put("/{order_id}", response_model=PurchaseOrderResponse)
def update_purchase_order(
    order_id: int,
    order_update: PurchaseOrderUpdate,
    current_user: User = Depends(PermissionChecker("purchase:update")),
    db: Session = Depends(get_db)
):
    """
    更新采购订单信息
    
    只能更新待处理的订单
    只更新提供的字段
    """
    from app.models import PurchaseOrder
    
    db_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if db_order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only update pending orders")
    
    for field, value in order_update.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/{order_id}/approve")
def approve_purchase_order(
    order_id: int,
    approve: PurchaseOrderApprove,
    current_user: User = Depends(PermissionChecker("purchase:approve")),
    db: Session = Depends(get_db)
):
    """
    审批采购订单
    
    接收审批结果，更新订单状态和审批信息
    只有待审批的订单才能审批
    审批通过后订单状态变为已审批，拒绝则变为已取消
    """
    from app.models import PurchaseOrder
    from datetime import datetime
    
    db_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if db_order.approval_status != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")
    
    db_order.approval_status = approve.approval_status
    db_order.approved_by = current_user.id
    db_order.approved_at = datetime.utcnow()
    
    if approve.approval_status == "approved":
        db_order.status = "approved"
    else:
        db_order.status = "cancelled"
    
    db.commit()
    return {"message": f"Order {approve.approval_status} successfully"}


@router.delete("/{order_id}")
def delete_purchase_order(
    order_id: int,
    current_user: User = Depends(PermissionChecker("purchase:delete")),
    db: Session = Depends(get_db)
):
    """
    删除采购订单
    
    只能删除待处理或已取消的订单
    已处理的订单不能删除
    """
    from app.models import PurchaseOrder
    
    db_order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Purchase order not found")
    
    if db_order.status not in ["pending", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot delete processed orders")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Purchase order deleted successfully"}
