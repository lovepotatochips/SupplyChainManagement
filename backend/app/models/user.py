from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text  # 导入SQLAlchemy的列类型
from sqlalchemy.orm import relationship  # 导入关系映射功能
from app.db.base import BaseModel  # 导入模型基类


class Menu(BaseModel):
    """
    菜单模型类
    
    用于存储系统菜单信息，支持多级菜单结构
    菜单用于构建前端导航栏和权限控制
    """
    __tablename__ = "menus"  # 对应的数据库表名
    
    name = Column(String(50), unique=False, index=True, nullable=False, comment="菜单名称")
    code = Column(String(50), unique=True, index=True, nullable=False, comment="菜单编码，用于权限判断")
    path = Column(String(255), comment="路由路径，前端跳转的URL")
    component = Column(String(255), comment="组件路径，Vue组件的文件路径")
    icon = Column(String(50), comment="图标，Element Plus的图标名称")
    parent_id = Column(Integer, ForeignKey("menus.id"), comment="父菜单ID，用于构建多级菜单")
    sort_order = Column(Integer, default=0, comment="排序，数字越小越靠前")
    status = Column(Boolean, default=True, comment="状态：True-显示，False-隐藏")
    
    children = relationship("Menu", backref="parent", remote_side="Menu.id")
    # 建立自引用关系，实现菜单树结构
    # backref="parent": 创建反向引用，可以通过menu.parent获取父菜单
    # remote_side="Menu.id": 指定父级端的字段是Menu.id
    
    def to_dict(self):
        """
        将模型对象转换为字典
        
        返回:
            dict: 包含菜单信息的字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "path": self.path,
            "component": self.component,
            "icon": self.icon,
            "parent_id": self.parent_id,
            "sort_order": self.sort_order,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class User(BaseModel):
    """
    用户模型类
    
    存储系统用户的基本信息和认证信息
    用户与角色是多对多关系，通过UserRole关联表实现
    用户与部门是多对一关系，一个用户属于一个部门
    """
    __tablename__ = "users"  # 对应的数据库表名
    
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名，登录账号")
    password = Column(String(255), nullable=False, comment="密码，加密存储")
    real_name = Column(String(50), comment="真实姓名")
    email = Column(String(100), comment="邮箱地址")
    phone = Column(String(20), comment="手机号码")
    avatar = Column(String(255), comment="头像URL")
    status = Column(Boolean, default=True, comment="状态：True-启用，False-禁用")
    department_id = Column(Integer, ForeignKey("departments.id"), comment="所属部门ID")
    is_superuser = Column(Boolean, default=False, comment="是否超级管理员，拥有所有权限")
    
    roles = relationship("UserRole", back_populates="user", cascade="all, delete-orphan")
    # 建立用户与用户角色关联表的关系
    # cascade="all, delete-orphan": 删除用户时，级联删除关联的用户角色记录
    
    department = relationship("Department", backref="users")
    # 建立用户与部门的关系
    # backref="users": 可以通过department.users获取该部门的所有用户
    
    def to_dict(self):
        """
        将模型对象转换为字典，包含关联的部门名称
        
        返回:
            dict: 包含用户信息和部门名称的字典
        """
        return {
            "id": self.id,
            "username": self.username,
            "real_name": self.real_name,
            "email": self.email,
            "phone": self.phone,
            "avatar": self.avatar,
            "status": self.status,
            "department_id": self.department_id,
            "department_name": self.department.name if self.department else None,
            "is_superuser": self.is_superuser,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Role(BaseModel):
    """
    角色模型类
    
    角色用于权限管理，一个角色可以拥有多个权限
    用户与角色是多对多关系，通过UserRole关联表实现
    角色与权限是多对多关系，通过RolePermission关联表实现
    """
    __tablename__ = "roles"  # 对应的数据库表名
    
    name = Column(String(50), unique=True, index=True, nullable=False, comment="角色名称")
    code = Column(String(50), unique=True, index=True, nullable=False, comment="角色编码，用于程序判断")
    description = Column(Text, comment="角色描述")
    status = Column(Boolean, default=True, comment="状态：True-启用，False-禁用")
    
    users = relationship("UserRole", back_populates="role", cascade="all, delete-orphan")
    # 建立角色与用户角色关联表的关系
    # cascade="all, delete-orphan": 删除角色时，级联删除关联的用户角色记录
    
    permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")
    # 建立角色与角色权限关联表的关系
    # cascade="all, delete-orphan": 删除角色时，级联删除关联的角色权限记录
    
    def to_dict(self):
        """
        将模型对象转换为字典
        
        返回:
            dict: 包含角色信息的字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class Permission(BaseModel):
    """
    权限模型类
    
    权限是系统的最小访问控制单元
    权限类型包括：menu（菜单访问权限）、button（按钮操作权限）、api（接口访问权限）
    """
    __tablename__ = "permissions"  # 对应的数据库表名
    
    name = Column(String(50), unique=True, index=True, nullable=False, comment="权限名称")
    code = Column(String(100), unique=True, index=True, nullable=False, comment="权限编码，用于程序判断")
    type = Column(String(20), nullable=False, comment="权限类型：menu-菜单权限，button-按钮权限，api-接口权限")
    description = Column(Text, comment="权限描述")
    
    roles = relationship("RolePermission", back_populates="permission", cascade="all, delete-orphan")
    # 建立权限与角色权限关联表的关系
    # cascade="all, delete-orphan": 删除权限时，级联删除关联的角色权限记录
    
    def to_dict(self):
        """
        将模型对象转换为字典
        
        返回:
            dict: 包含权限信息的字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "type": self.type,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }


class UserRole(BaseModel):
    """
    用户角色关联表模型
    
    用于实现用户与角色的多对多关系
    这是一个中间表，不直接存储业务数据
    """
    __tablename__ = "user_roles"  # 对应的数据库表名
    
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # 用户ID，外键关联到users表
    # ondelete="CASCADE": 用户删除时，级联删除此记录
    
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    # 角色ID，外键关联到roles表
    # ondelete="CASCADE": 角色删除时，级联删除此记录
    
    user = relationship("User", back_populates="roles")
    # 建立与User模型的关系，back_populates与User中的roles字段对应
    
    role = relationship("Role", back_populates="users")
    # 建立与Role模型的关系，back_populates与Role中的users字段对应


class RolePermission(BaseModel):
    """
    角色权限关联表模型
    
    用于实现角色与权限的多对多关系
    这是一个中间表，不直接存储业务数据
    """
    __tablename__ = "role_permissions"  # 对应的数据库表名
    
    role_id = Column(Integer, ForeignKey("roles.id", ondelete="CASCADE"), nullable=False)
    # 角色ID，外键关联到roles表
    # ondelete="CASCADE": 角色删除时，级联删除此记录
    
    permission_id = Column(Integer, ForeignKey("permissions.id", ondelete="CASCADE"), nullable=False)
    # 权限ID，外键关联到permissions表
    # ondelete="CASCADE": 权限删除时，级联删除此记录
    
    role = relationship("Role", back_populates="permissions")
    # 建立与Role模型的关系，back_populates与Role中的permissions字段对应
    
    permission = relationship("Permission", back_populates="roles")
    # 建立与Permission模型的关系，back_populates与Permission中的roles字段对应
