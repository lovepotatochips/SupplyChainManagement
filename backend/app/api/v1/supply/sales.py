from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import PermissionChecker
from app.models import User
from app.schemas.sales import CustomerCreate, CustomerResponse, CustomerUpdate, CustomerListResponse, SalesOrderCreate, SalesOrderResponse, SalesOrderUpdate, SalesOrderListResponse, SalesOrderDetailResponse, SalesOrderApprove

router = APIRouter()


@router.get("/customers/", response_model=CustomerListResponse)
def get_customers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    keyword: str = Query(None),
    current_user: User = Depends(PermissionChecker("customer:read")),
    db: Session = Depends(get_db)
):
    """
    获取客户列表
    
    支持分页查询和关键词搜索
    关键词可以搜索客户名称或编码
    返回客户列表及总数
    """
    from app.models import Customer
    
    query = db.query(Customer)
    if keyword:
        query = query.filter(
            (Customer.name.contains(keyword)) |
            (Customer.code.contains(keyword))
        )
    
    total = query.count()
    customers = query.offset(skip).limit(limit).all()
    return CustomerListResponse(total=total, items=customers)


@router.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(
    customer_id: int,
    current_user: User = Depends(PermissionChecker("customer:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个客户详情
    
    根据客户ID返回详细信息
    如果客户不存在，返回404错误
    """
    from app.models import Customer
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("/customers/", response_model=CustomerResponse)
def create_customer(
    customer: CustomerCreate,
    current_user: User = Depends(PermissionChecker("customer:create")),
    db: Session = Depends(get_db)
):
    """
    创建新客户
    
    接收客户数据，检查编码是否已存在
    如果编码不存在，创建新客户并返回
    """
    from app.models import Customer
    
    existing = db.query(Customer).filter(Customer.code == customer.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Customer code already exists")
    
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    current_user: User = Depends(PermissionChecker("customer:update")),
    db: Session = Depends(get_db)
):
    """
    更新客户信息
    
    根据客户ID更新数据
    只更新提供的字段
    """
    from app.models import Customer
    
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    for field, value in customer_update.model_dump(exclude_unset=True).items():
        setattr(db_customer, field, value)
    
    db.commit()
    db.refresh(db_customer)
    return db_customer


@router.delete("/customers/{customer_id}")
def delete_customer(
    customer_id: int,
    current_user: User = Depends(PermissionChecker("customer:delete")),
    db: Session = Depends(get_db)
):
    """
    删除客户
    
    根据客户ID删除客户
    """
    from app.models import Customer
    db_customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not db_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    db.delete(db_customer)
    db.commit()
    return {"message": "Customer deleted successfully"}


@router.get("/sales-orders/", response_model=SalesOrderListResponse)
def get_sales_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    status: str = Query(None),
    customer_id: int = Query(None),
    current_user: User = Depends(PermissionChecker("sales:read")),
    db: Session = Depends(get_db)
):
    """
    获取销售订单列表
    
    支持分页查询，可按状态和客户ID筛选
    返回销售订单列表及总数
    """
    from app.models import SalesOrder
    
    query = db.query(SalesOrder)
    if status:
        query = query.filter(SalesOrder.status == status)
    if customer_id:
        query = query.filter(SalesOrder.customer_id == customer_id)
    
    total = query.count()
    orders = query.order_by(SalesOrder.created_at.desc()).offset(skip).limit(limit).all()
    return SalesOrderListResponse(total=total, items=orders)


@router.get("/sales-orders/{order_id}", response_model=SalesOrderDetailResponse)
def get_sales_order(
    order_id: int,
    current_user: User = Depends(PermissionChecker("sales:read")),
    db: Session = Depends(get_db)
):
    """
    获取销售订单详情
    
    根据订单ID返回订单详细信息，包括订单明细
    如果订单不存在，返回404错误
    """
    from app.models import SalesOrder
    
    order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    return order


@router.post("/sales-orders/", response_model=SalesOrderResponse)
def create_sales_order(
    order: SalesOrderCreate,
    current_user: User = Depends(PermissionChecker("sales:create")),
    db: Session = Depends(get_db)
):
    """
    创建新的销售订单
    
    自动生成订单编码（SO前缀）
    计算订单总金额（所有明细金额之和）
    检查产品库存是否充足
    创建订单和订单明细
    """
    from app.models import SalesOrder, SalesOrderItem, Product
    from app.utils.helpers import generate_code
    
    code = generate_code("SO")
    
    total_amount = sum(item.quantity * item.unit_price for item in order.items)
    
    for item in order.items:
        product = db.query(Product).filter(Product.code == item.product_code).first()
        if product and product.current_stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {item.product_name}")
    
    db_order = SalesOrder(
        code=code,
        customer_id=order.customer_id,
        sale_date=order.sale_date,
        delivery_date=order.delivery_date,
        total_amount=total_amount,
        remark=order.remark
    )
    db.add(db_order)
    db.flush()
    
    for item in order.items:
        db_item = SalesOrderItem(
            sales_order_id=db_order.id,
            **item.model_dump(),
            amount=item.quantity * item.unit_price
        )
        db.add(db_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.put("/sales-orders/{order_id}", response_model=SalesOrderResponse)
def update_sales_order(
    order_id: int,
    order_update: SalesOrderUpdate,
    current_user: User = Depends(PermissionChecker("sales:update")),
    db: Session = Depends(get_db)
):
    """
    更新销售订单信息
    
    只能更新待处理的订单
    只更新提供的字段
    """
    from app.models import SalesOrder
    
    db_order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
    if db_order.status != "pending":
        raise HTTPException(status_code=400, detail="Can only update pending orders")
    
    for field, value in order_update.model_dump(exclude_unset=True).items():
        setattr(db_order, field, value)
    
    db.commit()
    db.refresh(db_order)
    return db_order


@router.post("/sales-orders/{order_id}/approve")
def approve_sales_order(
    order_id: int,
    approve: SalesOrderApprove,
    current_user: User = Depends(PermissionChecker("sales:approve")),
    db: Session = Depends(get_db)
):
    """
    审批销售订单
    
    接收审批结果，更新订单状态和审批信息
    只有待审批的订单才能审批
    审批通过后订单状态变为已审批，拒绝则变为已取消
    """
    from app.models import SalesOrder
    from datetime import datetime
    
    db_order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
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


@router.delete("/sales-orders/{order_id}")
def delete_sales_order(
    order_id: int,
    current_user: User = Depends(PermissionChecker("sales:delete")),
    db: Session = Depends(get_db)
):
    """
    删除销售订单
    
    只能删除待处理或已取消的订单
    已处理的订单不能删除
    """
    from app.models import SalesOrder
    
    db_order = db.query(SalesOrder).filter(SalesOrder.id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Sales order not found")
    
    if db_order.status not in ["pending", "cancelled"]:
        raise HTTPException(status_code=400, detail="Cannot delete processed orders")
    
    db.delete(db_order)
    db.commit()
    return {"message": "Sales order deleted successfully"}
