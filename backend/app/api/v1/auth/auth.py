from datetime import timedelta  # 导入时间增量，用于设置token过期时间
from fastapi import APIRouter, Depends, HTTPException, status  # 导入FastAPI的核心组件
from fastapi.security import OAuth2PasswordRequestForm  # 导入OAuth2密码请求表单
from sqlalchemy.orm import Session  # 导入数据库会话
from app.db.session import get_db  # 导入数据库会话依赖注入函数
from app.core.security import verify_password, create_access_token, get_password_hash  # 导入安全相关函数
from app.core.config import get_settings  # 导入配置获取函数
from app.core.deps import get_current_active_user  # 导入当前活跃用户依赖
from app.models import User  # 导入用户模型
from app.schemas.user import UserCreate, UserResponse, Token, UserUpdate  # 导入用户相关的Schema
from app.utils.helpers import generate_code  # 导入辅助函数

router = APIRouter()
# 创建API路由器实例
# 用于定义所有的认证相关路由

settings = get_settings()
# 获取应用配置


@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    
    参数:
        user: 用户创建数据，包含用户名、密码等信息
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        UserResponse: 创建成功的用户信息
    
    异常:
        HTTPException: 当用户名已存在时抛出400错误
    
    说明:
        - 验证用户名是否已存在
        - 对密码进行哈希加密
        - 创建用户并保存到数据库
    """
    db_user = db.query(User).filter(User.username == user.username).first()
    # 查询数据库，检查用户名是否已存在
    # first()返回第一条记录，如果没有则返回None
    
    if db_user:
        # 如果用户名已存在，抛出异常
        raise HTTPException(
            status_code=400,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    # 使用bcrypt对密码进行哈希加密
    # 这样即使数据库泄露，攻击者也无法获得原始密码
    
    db_user = User(
        **user.model_dump(exclude={"password"}),
        password=hashed_password
    )
    # 创建用户对象
    # **user.model_dump(exclude={"password"}): 将UserCreate对象转换为字典，排除password字段
    # password=hashed_password: 使用加密后的密码
    
    db.add(db_user)
    # 将用户对象添加到数据库会话
    
    db.commit()
    # 提交事务，将数据保存到数据库
    
    db.refresh(db_user)
    # 刷新对象，获取数据库自动生成的字段（如id、created_at等）
    
    return db_user


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    用户登录接口
    
    参数:
        form_data: OAuth2密码请求表单，包含username和password字段
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        Token: 包含访问令牌的响应
    
    异常:
        HTTPException: 当用户名或密码错误时抛出401错误
        HTTPException: 当用户被禁用时抛出400错误
    
    说明:
        - 验证用户名和密码
        - 检查用户状态是否启用
        - 生成JWT访问令牌
    """
    user = db.query(User).filter(User.username == form_data.username).first()
    # 根据用户名查询用户
    
    if not user or not verify_password(form_data.password, user.password):
        # 如果用户不存在或密码错误
        # verify_password: 验证明文密码是否与哈希密码匹配
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.status:
        # 检查用户状态，如果被禁用则拒绝登录
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 计算访问令牌的过期时间
    
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    # 创建JWT访问令牌
    # data={"sub": str(user.id)}: 将用户ID编码到令牌中
    # expires_delta: 设置令牌过期时间
    
    return {"access_token": access_token, "token_type": "bearer"}
    # 返回访问令牌和令牌类型


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    获取当前登录用户信息接口
    
    参数:
        current_user: 当前登录的用户对象，通过依赖注入自动获取
                   get_current_active_user会验证JWT令牌并返回用户信息
    
    返回:
        UserResponse: 当前用户的信息
    
    说明:
        - 需要提供有效的JWT令牌
        - 自动从令牌中解析用户信息
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    更新当前登录用户信息接口
    
    参数:
        user_update: 用户更新数据，包含要更新的字段
        current_user: 当前登录的用户对象
        db: 数据库会话
    
    返回:
        UserResponse: 更新后的用户信息
    
    说明:
        - 只能更新自己的信息
        - 只更新传入的字段，其他字段保持不变
        - 用户名和密码不能通过此接口修改
    """
    for field, value in user_update.model_dump(exclude_unset=True).items():
        # 遍历所有要更新的字段
        # exclude_unset=True: 只包含实际设置了值的字段
        setattr(current_user, field, value)
        # 动态设置对象的属性值
    
    db.commit()
    # 提交事务，保存更改
    
    db.refresh(current_user)
    # 刷新对象，获取更新后的数据
    
    return current_user
