from datetime import datetime, timedelta  # 导入日期时间相关模块
from typing import Optional  # 导入Optional类型提示
from jose import JWTError, jwt  # 导入JWT相关的错误和编码解码函数
import bcrypt  # 导入bcrypt库，用于密码哈希加密
from app.core.config import get_settings  # 导入配置获取函数

settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    验证明文密码是否与哈希密码匹配
    
    参数:
        plain_password: 用户输入的明文密码
        hashed_password: 数据库中存储的哈希密码
    
    返回:
        bool: 密码匹配返回True，否则返回False
    """
    try:
        # 使用bcrypt.checkpw验证密码
        # 将字符串转换为bytes进行比对
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    except:
        # 如果验证过程出现异常，返回False
        return False


def get_password_hash(password: str) -> str:
    """
    对密码进行哈希加密
    
    参数:
        password: 明文密码
    
    返回:
        str: 加密后的哈希密码（字符串格式）
    
    说明:
        bcrypt会自动生成随机盐值(salt)，增加密码破解难度
        相同的密码每次生成的哈希值都不同
    """
    salt = bcrypt.gensalt()  # 生成随机盐值
    # 对密码进行哈希加密，并转换为字符串返回
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建JWT访问令牌
    
    参数:
        data: 要编码到令牌中的数据，通常包含用户ID等信息
        expires_delta: 可选的过期时间增量，如果不指定则使用默认值
    
    返回:
        str: JWT令牌字符串
    
    说明:
        JWT(JSON Web Token)是一种用于身份验证的令牌格式
        包含三部分：头部、载荷、签名，用点号分隔
    """
    to_encode = data.copy()  # 复制原始数据，避免修改原数据
    if expires_delta:
        # 如果指定了过期时间增量，计算过期时间
        expire = datetime.utcnow() + expires_delta
    else:
        # 否则使用配置文件中的默认过期时间
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # 将过期时间添加到要编码的数据中
    to_encode.update({"exp": expire})
    # 使用配置的密钥和算法进行JWT编码
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    解码JWT访问令牌
    
    参数:
        token: JWT令牌字符串
    
    返回:
        Optional[dict]: 解码成功返回载荷数据字典，失败返回None
    
    说明:
        解码时会验证令牌的签名和过期时间
        如果令牌无效或已过期，会返回None
    """
    try:
        # 使用密钥和算法解码JWT令牌
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        # 如果解码失败（令牌无效或过期），返回None
        return None
