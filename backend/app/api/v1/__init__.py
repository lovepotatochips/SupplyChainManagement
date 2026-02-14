from fastapi import APIRouter
from app.api.v1.auth import auth as auth_router
from app.api.v1.system import users as users_router, departments as departments_router, menus as menus_router
from app.api.v1.supply import suppliers as suppliers_router, purchase as purchase_router, inventory as inventory_router, sales as sales_router
from app.api.v1.finance import finance as finance_router, reports as reports_router
from app.api.v1.analysis import analysis as analysis_router

api_router = APIRouter()

api_router.include_router(auth_router.router, prefix="/auth", tags=["认证"])

api_router.include_router(users_router.router, prefix="/users", tags=["用户管理"])
api_router.include_router(departments_router.router, prefix="/departments", tags=["部门管理"])
api_router.include_router(menus_router.router, prefix="/menus", tags=["菜单管理"])

api_router.include_router(suppliers_router.router, prefix="/suppliers", tags=["供应商管理"])
api_router.include_router(purchase_router.router, prefix="/purchase", tags=["采购管理"])
api_router.include_router(inventory_router.router, prefix="/inventory", tags=["库存管理"])
api_router.include_router(sales_router.router, prefix="/sales", tags=["销售管理"])

api_router.include_router(finance_router.router, prefix="/finance", tags=["财务管理"])
api_router.include_router(reports_router.router, prefix="/reports", tags=["报表分析"])

api_router.include_router(analysis_router.api_router, prefix="/analysis", tags=["数据分析"])
