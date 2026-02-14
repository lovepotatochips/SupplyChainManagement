from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import decode_access_token
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    """
    获取当前用户
    
    从JWT令牌中解析用户信息
    验证令牌有效性并返回用户对象
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    user_id: int = payload.get("sub")
    if user_id is None:
        raise credentials_exception
    
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    if not user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户
    
    确保用户状态为活跃
    如果用户未激活，返回错误
    """
    if not current_user.status:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前超级用户
    
    确保用户具有超级管理员权限
    如果不是超级用户，返回权限不足错误
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


class PermissionChecker:
    """
    权限检查器
    
    用于检查用户是否具有特定权限
    可以作为FastAPI的依赖项使用
    """
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        """
        检查用户权限
        
        超级用户拥有所有权限
        普通用户需要通过角色获得权限
        如果没有所需权限，返回权限不足错误
        """
        if current_user.is_superuser:
            return current_user
        
        user_permissions = []
        for role in current_user.roles:
            for perm in role.role.permissions:
                user_permissions.append(perm.permission.code)
        
        if self.required_permission not in user_permissions:
            raise HTTPException(
                status_code=403, 
                detail=f"Permission denied: {self.required_permission} required"
            )
        return current_user
