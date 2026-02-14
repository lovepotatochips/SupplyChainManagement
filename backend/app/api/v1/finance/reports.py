from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from app.db.session import get_db
from app.core.deps import PermissionChecker, get_current_active_user
from app.models import User

router = APIRouter()


@router.get("/purchase-summary")
def get_purchase_summary(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    采购汇总报表
    
    按日期统计采购订单数量和总金额
    支持按日期范围筛选
    """
    from app.models import PurchaseOrder
    from datetime import datetime
    
    query = db.query(
        func.date(PurchaseOrder.created_at).label("date"),
        func.count(PurchaseOrder.id).label("count"),
        func.sum(PurchaseOrder.total_amount).label("total_amount")
    )
    
    if start_date:
        query = query.filter(PurchaseOrder.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(PurchaseOrder.created_at <= datetime.fromisoformat(end_date))
    
    result = query.group_by(func.date(PurchaseOrder.created_at)).all()
    
    return {
        "data": [
            {
                "date": str(r.date),
                "count": r.count or 0,
                "total_amount": float(r.total_amount or 0)
            }
            for r in result
        ]
    }


@router.get("/sales-summary")
def get_sales_summary(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    销售汇总报表
    
    按日期统计销售订单数量和总金额
    支持按日期范围筛选
    """
    from app.models import SalesOrder
    from datetime import datetime
    
    query = db.query(
        func.date(SalesOrder.created_at).label("date"),
        func.count(SalesOrder.id).label("count"),
        func.sum(SalesOrder.total_amount).label("total_amount")
    )
    
    if start_date:
        query = query.filter(SalesOrder.created_at >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(SalesOrder.created_at <= datetime.fromisoformat(end_date))
    
    result = query.group_by(func.date(SalesOrder.created_at)).all()
    
    return {
        "data": [
            {
                "date": str(r.date),
                "count": r.count or 0,
                "total_amount": float(r.total_amount or 0)
            }
            for r in result
        ]
    }


@router.get("/inventory-status")
def get_inventory_status(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    库存状态报表
    
    统计正常、低库存和超库存产品数量
    返回低库存产品列表
    """
    from app.models import Product, ProductCategory
    
    products = db.query(Product).all()
    
    normal_products = [p for p in products if p.min_stock <= p.current_stock <= p.max_stock]
    low_stock_products = [p for p in products if p.current_stock < p.min_stock]
    overstock_products = [p for p in products if p.current_stock > p.max_stock]
    
    return {
        "total": len(products),
        "normal": len(normal_products),
        "low_stock": len(low_stock_products),
        "overstock": len(overstock_products),
        "low_stock_products": [{"id": p.id, "name": p.name, "code": p.code, "current_stock": p.current_stock, "min_stock": p.min_stock} for p in low_stock_products[:10]]
    }


@router.get("/supplier-performance")
def get_supplier_performance(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    供应商绩效报表
    
    统计每个供应商的订单数量和总金额
    按总金额降序排列
    """
    from app.models import PurchaseOrder, Supplier
    
    result = db.query(
        Supplier.id,
        Supplier.name,
        Supplier.code,
        func.count(PurchaseOrder.id).label("order_count"),
        func.sum(PurchaseOrder.total_amount).label("total_amount")
    ).join(
        PurchaseOrder, Supplier.id == PurchaseOrder.supplier_id
    ).group_by(
        Supplier.id
    ).all()
    
    return {
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code,
                "order_count": r.order_count or 0,
                "total_amount": float(r.total_amount or 0)
            }
            for r in result
        ]
    }


@router.get("/customer-analysis")
def get_customer_analysis(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    客户分析报表
    
    统计每个客户的订单数量和总金额
    按总金额降序排列
    """
    from app.models import SalesOrder, Customer
    
    result = db.query(
        Customer.id,
        Customer.name,
        Customer.code,
        func.count(SalesOrder.id).label("order_count"),
        func.sum(SalesOrder.total_amount).label("total_amount")
    ).join(
        SalesOrder, Customer.id == SalesOrder.customer_id
    ).group_by(
        Customer.id
    ).all()
    
    return {
        "data": [
            {
                "id": r.id,
                "name": r.name,
                "code": r.code,
                "order_count": r.order_count or 0,
                "total_amount": float(r.total_amount or 0)
            }
            for r in result
        ]
    }


@router.get("/financial-summary")
def get_financial_summary(
    start_date: str = Query(None),
    end_date: str = Query(None),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    财务汇总报表
    
    统计收款和付款总金额
    统计应收和应付账单总金额
    支持按日期范围筛选
    """
    from app.models import Payment, Bill
    from datetime import datetime
    
    payment_query = db.query(Payment)
    bill_query = db.query(Bill)
    
    if start_date:
        start = datetime.fromisoformat(start_date)
        payment_query = payment_query.filter(Payment.payment_date >= start)
        bill_query = bill_query.filter(Bill.bill_date >= start)
    if end_date:
        end = datetime.fromisoformat(end_date)
        payment_query = payment_query.filter(Payment.payment_date <= end)
        bill_query = bill_query.filter(Bill.bill_date <= end)
    
    total_in = db.query(func.sum(Payment.amount)).filter(Payment.type == "receive").scalar() or 0
    total_out = db.query(func.sum(Payment.amount)).filter(Payment.type == "pay").scalar() or 0
    
    total_receivable = db.query(func.sum(Bill.amount)).filter(Bill.type == "receivable").scalar() or 0
    total_payable = db.query(func.sum(Bill.amount)).filter(Bill.type == "payable").scalar() or 0
    
    return {
        "total_in": float(total_in),
        "total_out": float(total_out),
        "net": float(total_in - total_out),
        "total_receivable": float(total_receivable),
        "total_payable": float(total_payable)
    }


@router.get("/dashboard")
def get_dashboard_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    仪表板统计数据
    
    统计产品、供应商、客户数量
    统计待处理订单数量
    统计未收未付金额
    """
    from app.models import Product, Supplier, Customer, PurchaseOrder, SalesOrder, Bill
    
    total_products = db.query(func.count(Product.id)).scalar() or 0
    low_stock_count = db.query(func.count(Product.id)).filter(Product.current_stock < Product.min_stock).scalar() or 0
    
    total_suppliers = db.query(func.count(Supplier.id)).scalar() or 0
    total_customers = db.query(func.count(Customer.id)).scalar() or 0
    
    pending_orders = db.query(func.count(PurchaseOrder.id)).filter(PurchaseOrder.status == "pending").scalar() or 0
    pending_sales = db.query(func.count(SalesOrder.id)).filter(SalesOrder.status == "pending").scalar() or 0
    
    unpaid_receivable = db.query(func.sum(Bill.amount)).filter(Bill.type == "receivable", Bill.status != "paid").scalar() or 0
    unpaid_payable = db.query(func.sum(Bill.amount)).filter(Bill.type == "payable", Bill.status != "paid").scalar() or 0
    
    return {
        "products": {
            "total": total_products,
            "low_stock": low_stock_count
        },
        "partners": {
            "suppliers": total_suppliers,
            "customers": total_customers
        },
        "orders": {
            "pending_purchase": pending_orders,
            "pending_sales": pending_sales
        },
        "finance": {
            "unpaid_receivable": float(unpaid_receivable),
            "unpaid_payable": float(unpaid_payable)
        }
    }
