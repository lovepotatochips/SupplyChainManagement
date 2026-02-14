from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MenuBase(BaseModel):
    """
    菜单基础模型
    
    用于定义菜单的基本字段，供创建和更新操作使用
    菜单是系统的导航结构，用于组织和管理各个功能模块
    """
    name: str = Field(..., description="菜单名称")
    code: str = Field(..., description="菜单编码")
    path: Optional[str] = Field(None, description="路由路径")
    component: Optional[str] = Field(None, description="组件路径")
    icon: Optional[str] = Field(None, description="图标")
    parent_id: Optional[int] = Field(None, description="父菜单ID")
    sort_order: Optional[int] = Field(0, description="排序")
    status: Optional[bool] = Field(True, description="状态")


class MenuCreate(MenuBase):
    """
    菜单创建模型
    
    继承自MenuBase，用于创建新菜单时的数据验证
    """
    pass


class MenuUpdate(MenuBase):
    """
    菜单更新模型
    
    继承自MenuBase，用于更新菜单信息时的数据验证
    所有字段都是可选的，可以只更新部分字段
    """
    pass


class MenuResponse(MenuBase):
    """
    菜单响应模型
    
    继承自MenuBase，并添加了id和时间戳字段
    用于API响应返回菜单数据
    """
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
