from typing import List  # 导入List类型，用于类型提示
from fastapi import APIRouter, Depends, HTTPException, Query  # 导入FastAPI的核心组件
from sqlalchemy.orm import Session  # 导入数据库会话
from app.db.session import get_db  # 导入数据库会话依赖注入函数
from app.core.deps import get_current_active_user, get_current_superuser, PermissionChecker  # 导入用户和权限相关的依赖
from app.models import User  # 导入用户模型
from app.schemas.user import UserCreate, UserResponse, UserUpdate, UserRoleCreate, RoleCreate, RoleResponse, RoleUpdate, PermissionCreate, PermissionResponse, RolePermissionCreate  # 导入所有用户相关的Schema

router = APIRouter()
# 创建API路由器实例
# 用于定义所有的用户、角色、权限相关路由


@router.get("/", response_model=List[UserResponse])
def get_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    department_id: int = Query(None, description="部门ID"),
    keyword: str = Query(None, description="搜索关键词"),
    current_user: User = Depends(PermissionChecker("user:read")),
    db: Session = Depends(get_db)
):
    """
    获取用户列表接口
    
    参数:
        skip: 跳过的记录数，用于分页，默认为0，最小值为0
        limit: 每页的记录数，默认为100，最小为1，最大为100
        department_id: 部门ID，用于按部门筛选用户，可选
        keyword: 搜索关键词，支持按用户名和真实姓名搜索，可选
        current_user: 当前登录的用户，通过依赖注入自动获取，需要user:read权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        List[UserResponse]: 用户列表
    
    说明:
        - 支持分页查询
        - 支持按部门筛选
        - 支持关键词搜索
        - 需要user:read权限
    """
    query = db.query(User)
    # 创建用户查询对象
    
    if department_id:
        # 如果指定了部门ID，添加部门筛选条件
        query = query.filter(User.department_id == department_id)
    
    if keyword:
        # 如果指定了搜索关键词，添加搜索条件
        # 使用contains方法进行模糊匹配
        # | 表示或逻辑，匹配用户名或真实姓名
        query = query.filter(
            User.username.contains(keyword) | 
            User.real_name.contains(keyword)
        )
    
    users = query.offset(skip).limit(limit).all()
    # 执行查询
    # offset(skip): 跳过前skip条记录
    # limit(limit): 最多返回limit条记录
    # all(): 获取所有结果
    
    return users


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int,
    current_user: User = Depends(PermissionChecker("user:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个用户信息接口
    
    参数:
        user_id: 用户ID，路径参数
        current_user: 当前登录的用户，需要user:read权限
        db: 数据库会话
    
    返回:
        UserResponse: 用户详细信息
    
    异常:
        HTTPException: 当用户不存在时抛出404错误
    
    说明:
        - 根据用户ID查询用户信息
        - 需要user:read权限
    """
    user = db.query(User).filter(User.id == user_id).first()
    # 根据用户ID查询用户
    # first(): 返回第一条匹配的记录，如果没有则返回None
    
    if not user:
        # 如果用户不存在，抛出404异常
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate,
    current_user: User = Depends(PermissionChecker("user:create")),
    db: Session = Depends(get_db)
):
    """
    创建用户接口
    
    参数:
        user: 用户创建数据，包含用户名、密码等信息
        current_user: 当前登录的用户，需要user:create权限
        db: 数据库会话
    
    返回:
        UserResponse: 创建成功的用户信息
    
    异常:
        HTTPException: 当用户名已存在时抛出400错误
    
    说明:
        - 验证用户名是否已存在
        - 对密码进行哈希加密
        - 创建用户并保存到数据库
        - 需要user:create权限
    """
    from app.core.security import get_password_hash
    from app.utils.helpers import generate_code
    # 导入密码哈希和辅助函数
    
    existing_user = db.query(User).filter(User.username == user.username).first()
    # 检查用户名是否已存在
    
    if existing_user:
        # 如果用户名已存在，抛出异常
        raise HTTPException(status_code=400, detail="Username already exists")
    
    hashed_password = get_password_hash(user.password)
    # 对密码进行哈希加密
    
    db_user = User(
        **user.model_dump(exclude={"password"}),
        password=hashed_password
    )
    # 创建用户对象
    # exclude={"password"}: 排除原始密码字段
    # password=hashed_password: 使用加密后的密码
    
    db.add(db_user)
    # 添加到数据库会话
    
    db.commit()
    # 提交事务
    
    db.refresh(db_user)
    # 刷新对象，获取生成的id等字段
    
    return db_user


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(PermissionChecker("user:update")),
    db: Session = Depends(get_db)
):
    """
    更新用户信息接口
    
    参数:
        user_id: 用户ID，路径参数
        user_update: 用户更新数据，包含要更新的字段
        current_user: 当前登录的用户，需要user:update权限
        db: 数据库会话
    
    返回:
        UserResponse: 更新后的用户信息
    
    异常:
        HTTPException: 当用户不存在时抛出404错误
    
    说明:
        - 只更新传入的字段，其他字段保持不变
        - 用户名和密码不能通过此接口修改
        - 需要user:update权限
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    # 根据ID查询用户
    
    if not db_user:
        # 如果用户不存在，抛出异常
        raise HTTPException(status_code=404, detail="User not found")
    
    for field, value in user_update.model_dump(exclude_unset=True).items():
        # 遍历所有要更新的字段
        # exclude_unset=True: 只包含实际设置了值的字段
        setattr(db_user, field, value)
        # 动态设置对象的属性值
    
    db.commit()
    # 提交事务
    
    db.refresh(db_user)
    # 刷新对象
    
    return db_user


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user: User = Depends(PermissionChecker("user:delete")),
    db: Session = Depends(get_db)
):
    """
    删除用户接口
    
    参数:
        user_id: 用户ID，路径参数
        current_user: 当前登录的用户，需要user:delete权限
        db: 数据库会话
    
    返回:
        dict: 包含成功消息的字典
    
    异常:
        HTTPException: 当用户不存在时抛出404错误
    
    说明:
        - 根据用户ID删除用户
        - 会级联删除相关的用户角色关联
        - 需要user:delete权限
    """
    db_user = db.query(User).filter(User.id == user_id).first()
    # 根据ID查询用户
    
    if not db_user:
        # 如果用户不存在，抛出异常
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    # 删除用户对象
    
    db.commit()
    # 提交事务
    
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/roles")
def assign_roles(
    user_id: int,
    role_data: UserRoleCreate,
    current_user: User = Depends(PermissionChecker("user:update")),
    db: Session = Depends(get_db)
):
    """
    为用户分配角色接口
    
    参数:
        user_id: 用户ID，路径参数
        role_data: 角色分配数据，包含角色ID列表
        current_user: 当前登录的用户，需要user:update权限
        db: 数据库会话
    
    返回:
        dict: 包含成功消息的字典
    
    异常:
        HTTPException: 当用户不存在时抛出404错误
    
    说明:
        - 先删除用户的所有角色
        - 然后添加新的角色
        - 支持批量分配多个角色
        - 需要user:update权限
    """
    from app.models import UserRole, Role
    # 导入用户角色和角色模型
    
    user = db.query(User).filter(User.id == user_id).first()
    # 查询用户
    
    if not user:
        # 如果用户不存在，抛出异常
        raise HTTPException(status_code=404, detail="User not found")
    
    db.query(UserRole).filter(UserRole.user_id == user_id).delete()
    # 删除用户的所有角色关联
    # 这样可以重新分配角色
    
    for role_id in role_data.role_ids:
        # 遍历要分配的角色ID列表
        role = db.query(Role).filter(Role.id == role_id).first()
        # 查询角色是否存在
        if role:
            # 如果角色存在，创建用户角色关联
            user_role = UserRole(user_id=user_id, role_id=role_id)
            db.add(user_role)
    
    db.commit()
    # 提交事务
    
    return {"message": "Roles assigned successfully"}


@router.get("/roles/", response_model=List[RoleResponse])
def get_roles(
    current_user: User = Depends(PermissionChecker("role:read")),
    db: Session = Depends(get_db)
):
    """
    获取角色列表接口
    
    参数:
        current_user: 当前登录的用户，需要role:read权限
        db: 数据库会话
    
    返回:
        List[RoleResponse]: 角色列表
    
    说明:
        - 获取系统中的所有角色
        - 需要role:read权限
    """
    from app.models import Role
    # 导入角色模型
    
    roles = db.query(Role).all()
    # 查询所有角色
    
    return roles


@router.post("/roles/", response_model=RoleResponse)
def create_role(
    role: RoleCreate,
    current_user: User = Depends(PermissionChecker("role:create")),
    db: Session = Depends(get_db)
):
    """
    创建角色接口
    
    参数:
        role: 角色创建数据，包含角色名称、编码等信息
        current_user: 当前登录的用户，需要role:create权限
        db: 数据库会话
    
    返回:
        RoleResponse: 创建成功的角色信息
    
    说明:
        - 创建新角色
        - 需要role:create权限
    """
    from app.models import Role
    # 导入角色模型
    
    db_role = Role(**role.model_dump())
    # 创建角色对象
    # **role.model_dump(): 将Schema对象转换为字典
    
    db.add(db_role)
    # 添加到数据库会话
    
    db.commit()
    # 提交事务
    
    db.refresh(db_role)
    # 刷新对象
    
    return db_role


@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int,
    role_update: RoleUpdate,
    current_user: User = Depends(PermissionChecker("role:update")),
    db: Session = Depends(get_db)
):
    """
    更新角色接口
    
    参数:
        role_id: 角色ID，路径参数
        role_update: 角色更新数据
        current_user: 当前登录的用户，需要role:update权限
        db: 数据库会话
    
    返回:
        RoleResponse: 更新后的角色信息
    
    异常:
        HTTPException: 当角色不存在时抛出404错误
    
    说明:
        - 只更新传入的字段
        - 需要role:update权限
    """
    from app.models import Role
    # 导入角色模型
    
    db_role = db.query(Role).filter(Role.id == role_id).first()
    # 查询角色
    
    if not db_role:
        # 如果角色不存在，抛出异常
        raise HTTPException(status_code=404, detail="Role not found")
    
    for field, value in role_update.model_dump(exclude_unset=True).items():
        # 遍历要更新的字段
        setattr(db_role, field, value)
        # 动态设置属性值
    
    db.commit()
    # 提交事务
    
    db.refresh(db_role)
    # 刷新对象
    
    return db_role


@router.delete("/roles/{role_id}")
def delete_role(
    role_id: int,
    current_user: User = Depends(PermissionChecker("role:delete")),
    db: Session = Depends(get_db)
):
    """
    删除角色接口
    
    参数:
        role_id: 角色ID，路径参数
        current_user: 当前登录的用户，需要role:delete权限
        db: 数据库会话
    
    返回:
        dict: 包含成功消息的字典
    
    异常:
        HTTPException: 当角色不存在时抛出404错误
    
    说明:
        - 根据角色ID删除角色
        - 会级联删除相关的用户角色和角色权限关联
        - 需要role:delete权限
    """
    from app.models import Role
    # 导入角色模型
    
    db_role = db.query(Role).filter(Role.id == role_id).first()
    # 查询角色
    
    if not db_role:
        # 如果角色不存在，抛出异常
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.delete(db_role)
    # 删除角色
    
    db.commit()
    # 提交事务
    
    return {"message": "Role deleted successfully"}


@router.post("/roles/{role_id}/permissions")
def assign_permissions(
    role_id: int,
    perm_data: RolePermissionCreate,
    current_user: User = Depends(PermissionChecker("role:update")),
    db: Session = Depends(get_db)
):
    """
    为角色分配权限接口
    
    参数:
        role_id: 角色ID，路径参数
        perm_data: 权限分配数据，包含权限ID列表
        current_user: 当前登录的用户，需要role:update权限
        db: 数据库会话
    
    返回:
        dict: 包含成功消息的字典
    
    异常:
        HTTPException: 当角色不存在时抛出404错误
    
    说明:
        - 先删除角色的所有权限
        - 然后添加新的权限
        - 支持批量分配多个权限
        - 需要role:update权限
    """
    from app.models import RolePermission, Permission
    # 导入角色权限和权限模型
    
    role = db.query(Role).filter(Role.id == role_id).first()
    # 查询角色
    
    if not role:
        # 如果角色不存在，抛出异常
        raise HTTPException(status_code=404, detail="Role not found")
    
    db.query(RolePermission).filter(RolePermission.role_id == role_id).delete()
    # 删除角色的所有权限关联
    # 这样可以重新分配权限
    
    for perm_id in perm_data.permission_ids:
        # 遍历要分配的权限ID列表
        perm = db.query(Permission).filter(Permission.id == perm_id).first()
        # 查询权限是否存在
        if perm:
            # 如果权限存在，创建角色权限关联
            role_perm = RolePermission(role_id=role_id, permission_id=perm_id)
            db.add(role_perm)
    
    db.commit()
    # 提交事务
    
    return {"message": "Permissions assigned successfully"}


@router.get("/permissions/", response_model=List[PermissionResponse])
def get_permissions(
    current_user: User = Depends(PermissionChecker("permission:read")),
    db: Session = Depends(get_db)
):
    """
    获取权限列表接口
    
    参数:
        current_user: 当前登录的用户，需要permission:read权限
        db: 数据库会话
    
    返回:
        List[PermissionResponse]: 权限列表
    
    说明:
        - 获取系统中的所有权限
        - 需要permission:read权限
    """
    from app.models import Permission
    # 导入权限模型
    
    permissions = db.query(Permission).all()
    # 查询所有权限
    
    return permissions


@router.post("/permissions/", response_model=PermissionResponse)
def create_permission(
    permission: PermissionCreate,
    current_user: User = Depends(PermissionChecker("permission:create")),
    db: Session = Depends(get_db)
):
    """
    创建权限接口
    
    参数:
        permission: 权限创建数据，包含权限名称、编码等信息
        current_user: 当前登录的用户，需要permission:create权限
        db: 数据库会话
    
    返回:
        PermissionResponse: 创建成功的权限信息
    
    说明:
        - 创建新的权限
        - 需要permission:create权限
    """
    from app.models import Permission
    # 导入权限模型
    
    db_permission = Permission(**permission.model_dump())
    # 创建权限对象
    # **permission.model_dump(): 将Schema对象转换为字典
    
    db.add(db_permission)
    # 添加到数据库会话
    
    db.commit()
    # 提交事务
    
    db.refresh(db_permission)
    # 刷新对象
    
    return db_permission
