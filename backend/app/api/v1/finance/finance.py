from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.deps import PermissionChecker
from app.models import User
from app.schemas.finance import PaymentCreate, PaymentResponse, PaymentUpdate, PaymentListResponse, PaymentApprove, BillCreate, BillResponse, BillUpdate, BillListResponse, AccountCreate, AccountResponse, AccountUpdate, CostCenterCreate, CostCenterResponse, CostCenterUpdate

router = APIRouter()


@router.get("/payments/", response_model=PaymentListResponse)
def get_payments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    type: str = Query(None),
    status: str = Query(None),
    current_user: User = Depends(PermissionChecker("payment:read")),
    db: Session = Depends(get_db)
):
    """
    获取付款单据列表
    
    支持分页查询，可按类型和状态筛选
    返回付款单据列表及总数
    """
    from app.models import Payment
    
    query = db.query(Payment)
    if type:
        query = query.filter(Payment.type == type)
    if status:
        query = query.filter(Payment.status == status)
    
    total = query.count()
    payments = query.order_by(Payment.created_at.desc()).offset(skip).limit(limit).all()
    return PaymentListResponse(total=total, items=payments)


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(
    payment_id: int,
    current_user: User = Depends(PermissionChecker("payment:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个付款单据详情
    
    根据付款单据ID返回详细信息
    如果单据不存在，返回404错误
    """
    from app.models import Payment
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@router.post("/payments/", response_model=PaymentResponse)
def create_payment(
    payment: PaymentCreate,
    current_user: User = Depends(PermissionChecker("payment:create")),
    db: Session = Depends(get_db)
):
    """
    创建新的付款单据
    
    接收付款数据，检查编码是否已存在
    自动记录操作人员ID
    """
    from app.models import Payment
    
    existing = db.query(Payment).filter(Payment.code == payment.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Payment code already exists")
    
    db_payment = Payment(
        operator_id=current_user.id,
        **payment.model_dump()
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(
    payment_id: int,
    payment_update: PaymentUpdate,
    current_user: User = Depends(PermissionChecker("payment:update")),
    db: Session = Depends(get_db)
):
    """
    更新付款单据信息
    
    根据付款单据ID更新数据
    只更新提供的字段
    """
    from app.models import Payment
    
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    for field, value in payment_update.model_dump(exclude_unset=True).items():
        setattr(db_payment, field, value)
    
    db.commit()
    db.refresh(db_payment)
    return db_payment


@router.post("/payments/{payment_id}/approve")
def approve_payment(
    payment_id: int,
    approve: PaymentApprove,
    current_user: User = Depends(PermissionChecker("payment:approve")),
    db: Session = Depends(get_db)
):
    """
    审批付款单据
    
    接收审批结果，更新单据状态和审批信息
    只有待审批的单据才能审批
    """
    from app.models import Payment
    from datetime import datetime
    
    db_payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    if db_payment.approval_status != "pending":
        raise HTTPException(status_code=400, detail="Payment already processed")
    
    db_payment.approval_status = approve.approval_status
    db_payment.approved_by = current_user.id
    db_payment.approved_at = datetime.utcnow()
    
    if approve.approval_status == "approved":
        db_payment.status = "completed"
    else:
        db_payment.status = "cancelled"
    
    db.commit()
    return {"message": f"Payment {approve.approval_status} successfully"}


@router.get("/bills/", response_model=BillListResponse)
def get_bills(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    type: str = Query(None),
    status: str = Query(None),
    current_user: User = Depends(PermissionChecker("bill:read")),
    db: Session = Depends(get_db)
):
    """
    获取账单列表
    
    支持分页查询，可按类型和状态筛选
    返回账单列表及总数
    """
    from app.models import Bill
    
    query = db.query(Bill)
    if type:
        query = query.filter(Bill.type == type)
    if status:
        query = query.filter(Bill.status == status)
    
    total = query.count()
    bills = query.order_by(Bill.created_at.desc()).offset(skip).limit(limit).all()
    return BillListResponse(total=total, items=bills)


@router.get("/bills/{bill_id}", response_model=BillResponse)
def get_bill(
    bill_id: int,
    current_user: User = Depends(PermissionChecker("bill:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个账单详情
    
    根据账单ID返回详细信息
    如果账单不存在，返回404错误
    """
    from app.models import Bill
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    return bill


@router.post("/bills/", response_model=BillResponse)
def create_bill(
    bill: BillCreate,
    current_user: User = Depends(PermissionChecker("bill:create")),
    db: Session = Depends(get_db)
):
    """
    创建新账单
    
    接收账单数据，检查编码是否已存在
    自动初始化已付金额和剩余金额
    """
    from app.models import Bill
    
    existing = db.query(Bill).filter(Bill.code == bill.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bill code already exists")
    
    remaining_amount = bill.amount
    db_bill = Bill(
        paid_amount=0.0,
        remaining_amount=remaining_amount,
        **bill.model_dump()
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return db_bill


@router.put("/bills/{bill_id}", response_model=BillResponse)
def update_bill(
    bill_id: int,
    bill_update: BillUpdate,
    current_user: User = Depends(PermissionChecker("bill:update")),
    db: Session = Depends(get_db)
):
    """
    更新账单信息
    
    根据账单ID更新数据
    如果更新状态为已付，自动计算已付和剩余金额
    """
    from app.models import Bill
    
    db_bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not db_bill:
        raise HTTPException(status_code=404, detail="Bill not found")
    
    for field, value in bill_update.model_dump(exclude_unset=True).items():
        setattr(db_bill, field, value)
    
    if bill_update.status:
        if bill_update.status == "paid":
            db_bill.remaining_amount = 0
            db_bill.paid_amount = db_bill.amount
        elif bill_update.status == "partial":
            pass
    
    db.commit()
    db.refresh(db_bill)
    return db_bill


@router.get("/accounts/", response_model=List[AccountResponse])
def get_accounts(
    current_user: User = Depends(PermissionChecker("account:read")),
    db: Session = Depends(get_db)
):
    """
    获取银行账户列表
    
    返回所有银行账户信息
    """
    from app.models import Account
    accounts = db.query(Account).all()
    return accounts


@router.post("/accounts/", response_model=AccountResponse)
def create_account(
    account: AccountCreate,
    current_user: User = Depends(PermissionChecker("account:create")),
    db: Session = Depends(get_db)
):
    """
    创建新银行账户
    
    接收账户数据，检查编码是否已存在
    """
    from app.models import Account
    
    existing = db.query(Account).filter(Account.code == account.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Account code already exists")
    
    db_account = Account(**account.model_dump())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


@router.put("/accounts/{account_id}", response_model=AccountResponse)
def update_account(
    account_id: int,
    account_update: AccountUpdate,
    current_user: User = Depends(PermissionChecker("account:update")),
    db: Session = Depends(get_db)
):
    """
    更新银行账户信息
    
    根据账户ID更新数据
    只更新提供的字段
    """
    from app.models import Account
    
    db_account = db.query(Account).filter(Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for field, value in account_update.model_dump(exclude_unset=True).items():
        setattr(db_account, field, value)
    
    db.commit()
    db.refresh(db_account)
    return db_account


@router.get("/cost-centers/", response_model=List[CostCenterResponse])
def get_cost_centers(
    current_user: User = Depends(PermissionChecker("costcenter:read")),
    db: Session = Depends(get_db)
):
    """
    获取成本中心列表
    
    返回所有成本中心信息
    """
    from app.models import CostCenter
    cost_centers = db.query(CostCenter).all()
    return cost_centers


@router.post("/cost-centers/", response_model=CostCenterResponse)
def create_cost_center(
    cost_center: CostCenterCreate,
    current_user: User = Depends(PermissionChecker("costcenter:create")),
    db: Session = Depends(get_db)
):
    """
    创建新成本中心
    
    接收成本中心数据，检查编码是否已存在
    """
    from app.models import CostCenter
    
    existing = db.query(CostCenter).filter(CostCenter.code == cost_center.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Cost center code already exists")
    
    db_cost_center = CostCenter(**cost_center.model_dump())
    db.add(db_cost_center)
    db.commit()
    db.refresh(db_cost_center)
    return db_cost_center


@router.put("/cost-centers/{center_id}", response_model=CostCenterResponse)
def update_cost_center(
    center_id: int,
    cost_center_update: CostCenterUpdate,
    current_user: User = Depends(PermissionChecker("costcenter:update")),
    db: Session = Depends(get_db)
):
    """
    更新成本中心信息
    
    根据成本中心ID更新数据
    只更新提供的字段
    """
    from app.models import CostCenter
    
    db_cost_center = db.query(CostCenter).filter(CostCenter.id == center_id).first()
    if not db_cost_center:
        raise HTTPException(status_code=404, detail="Cost center not found")
    
    for field, value in cost_center_update.model_dump(exclude_unset=True).items():
        setattr(db_cost_center, field, value)
    
    db.commit()
    db.refresh(db_cost_center)
    return db_cost_center
