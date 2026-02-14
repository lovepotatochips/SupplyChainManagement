from pydantic import BaseModel, EmailStr, Field  # 导入Pydantic的基类、邮箱验证和字段定义
from typing import Optional, List  # 导入可选类型和列表类型
from datetime import datetime  # 导入日期时间类型


class UserBase(BaseModel):
    """
    用户基础Schema
    
    定义用户的基本字段，被其他Schema继承
    """
    username: str = Field(..., max_length=50)
    # 用户名，必填字段，最大长度50
    # Field(...): ...表示必填
    
    real_name: Optional[str] = Field(None, max_length=50)
    # 真实姓名，可选字段，最大长度50
    
    email: Optional[EmailStr] = None
    # 邮箱，可选字段，EmailStr会自动验证邮箱格式
    
    phone: Optional[str] = Field(None, max_length=20)
    # 手机号，可选字段，最大长度20
    
    avatar: Optional[str] = None
    # 头像URL，可选字段
    
    department_id: Optional[int] = None
    # 部门ID，可选字段


class UserCreate(UserBase):
    """
    创建用户的Schema
    
    继承UserBase，新增密码字段
    用于接收前端传来的创建用户数据
    """
    password: str = Field(..., min_length=6)
    # 密码，必填字段，最小长度6


class UserUpdate(BaseModel):
    """
    更新用户的Schema
    
    所有字段都是可选的，用于接收前端传来的更新数据
    不包含username，因为用户名通常不允许修改
    """
    real_name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar: Optional[str] = None
    department_id: Optional[int] = None
    status: Optional[bool] = None


class UserResponse(UserBase):
    """
    用户响应Schema
    
    继承UserBase，新增只读字段
    用于返回给前端的用户数据
    """
    id: int
    # 用户ID
    
    status: bool
    # 用户状态
    
    is_superuser: bool
    # 是否超级管理员
    
    created_at: datetime
    # 创建时间
    
    updated_at: datetime
    # 更新时间
    
    class Config:
        from_attributes = True
        # 允许从ORM对象创建Pydantic模型


class UserLogin(BaseModel):
    """
    用户登录Schema
    
    用于接收前端传来的登录数据
    """
    username: str
    # 用户名
    
    password: str
    # 密码


class Token(BaseModel):
    """
    Token响应Schema
    
    用于返回登录成功后的令牌信息
    """
    access_token: str
    # 访问令牌，JWT格式的字符串
    
    token_type: str
    # 令牌类型，通常是"bearer"


class TokenData(BaseModel):
    """
    Token数据Schema
    
    用于解码JWT令牌后存储数据
    """
    username: Optional[str] = None
    # 用户名，解码后从令牌中获取


class RoleBase(BaseModel):
    """
    角色基础Schema
    
    定义角色的基本字段
    """
    name: str = Field(..., max_length=50)
    # 角色名称，必填字段
    
    code: str = Field(..., max_length=50)
    # 角色编码，必填字段，用于程序判断
    
    description: Optional[str] = None
    # 角色描述，可选字段


class RoleCreate(RoleBase):
    """
    创建角色的Schema
    
    继承RoleBase，用于接收创建角色的数据
    """
    pass


class RoleUpdate(BaseModel):
    """
    更新角色的Schema
    
    所有字段都是可选的，用于接收更新角色的数据
    """
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None
    status: Optional[bool] = None


class RoleResponse(RoleBase):
    """
    角色响应Schema
    
    继承RoleBase，新增只读字段
    用于返回给前端的角色数据
    """
    id: int
    # 角色ID
    
    status: bool
    # 角色状态
    
    created_at: datetime
    # 创建时间
    
    updated_at: datetime
    # 更新时间
    
    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    """
    权限基础Schema
    
    定义权限的基本字段
    """
    name: str = Field(..., max_length=50)
    # 权限名称，必填字段
    
    code: str = Field(..., max_length=100)
    # 权限编码，必填字段，用于程序判断
    
    type: str = Field(..., max_length=20)
    # 权限类型，必填字段，如：menu/button/api
    
    description: Optional[str] = None
    # 权限描述，可选字段


class PermissionCreate(PermissionBase):
    """
    创建权限的Schema
    
    继承PermissionBase，用于接收创建权限的数据
    """
    pass


class PermissionUpdate(BaseModel):
    """
    更新权限的Schema
    
    所有字段都是可选的，用于接收更新权限的数据
    """
    name: Optional[str] = Field(None, max_length=50)
    description: Optional[str] = None


class PermissionResponse(PermissionBase):
    """
    权限响应Schema
    
    继承PermissionBase，新增只读字段
    用于返回给前端的权限数据
    """
    id: int
    # 权限ID
    
    created_at: datetime
    # 创建时间
    
    updated_at: datetime
    # 更新时间
    
    class Config:
        from_attributes = True


class UserRoleCreate(BaseModel):
    """
    用户角色关联Schema
    
    用于给用户分配角色
    """
    user_id: int
    # 用户ID
    
    role_ids: List[int]
    # 角色ID列表，支持批量分配


class RolePermissionCreate(BaseModel):
    """
    角色权限关联Schema
    
    用于给角色分配权限
    """
    role_id: int
    # 角色ID
    
    permission_ids: List[int]
    # 权限ID列表，支持批量分配
