from pydantic import BaseModel, Field  # 导入Pydantic的基类和字段定义
from typing import Optional  # 导入可选类型
from datetime import datetime  # 导入日期时间类型


class DepartmentBase(BaseModel):
    """
    部门基础Schema
    
    定义部门的基本字段，被其他Schema继承
    """
    name: str = Field(..., max_length=100)
    # 部门名称，必填字段，最大长度100
    
    code: str = Field(..., max_length=50)
    # 部门编码，必填字段，最大长度50，全局唯一
    
    parent_id: Optional[int] = None
    # 父部门ID，可选字段，用于构建多级部门结构
    # 如果为None，表示这是顶级部门
    
    sort_order: int = 0
    # 排序字段，默认值为0，用于控制同级部门的显示顺序
    
    leader: Optional[str] = Field(None, max_length=50)
    # 负责人姓名，可选字段，最大长度50
    
    phone: Optional[str] = Field(None, max_length=20)
    # 联系电话，可选字段，最大长度20
    
    address: Optional[str] = Field(None, max_length=255)
    # 地址，可选字段，最大长度255
    
    description: Optional[str] = None
    # 部门描述，可选字段
    
    status: int = 1
    # 部门状态，默认值为1（启用）
    # 1表示启用，0表示禁用


class DepartmentCreate(DepartmentBase):
    """
    创建部门的Schema
    
    继承DepartmentBase，用于接收前端传来的创建部门数据
    """
    pass


class DepartmentUpdate(BaseModel):
    """
    更新部门的Schema
    
    所有字段都是可选的，用于接收前端传来的更新部门数据
    不包含code字段，因为部门编码通常不允许修改
    """
    name: Optional[str] = Field(None, max_length=100)
    # 部门名称，可选
    
    parent_id: Optional[int] = None
    # 父部门ID，可选
    
    sort_order: Optional[int] = None
    # 排序，可选
    
    leader: Optional[str] = Field(None, max_length=50)
    # 负责人，可选
    
    phone: Optional[str] = Field(None, max_length=20)
    # 联系电话，可选
    
    address: Optional[str] = Field(None, max_length=255)
    # 地址，可选
    
    description: Optional[str] = None
    # 描述，可选
    
    status: Optional[int] = None
    # 状态，可选


class DepartmentResponse(DepartmentBase):
    """
    部门响应Schema
    
    继承DepartmentBase，新增只读字段
    用于返回给前端的部门数据
    """
    id: int
    # 部门ID
    
    created_at: datetime
    # 创建时间
    
    updated_at: datetime
    # 更新时间
    
    class Config:
        from_attributes = True
        # 允许从ORM对象创建Pydantic模型


class DepartmentTree(DepartmentResponse):
    """
    部门树形结构Schema
    
    继承DepartmentResponse，新增树形结构相关字段
    用于返回包含子部门的树形数据
    """
    children: Optional[list] = None
    # 子部门列表，可选字段
    # 递归包含子部门，构建完整的部门树
    
    user_count: int = 0
    # 部门用户数量，默认值为0
    # 用于统计该部门及子部门的用户总数
