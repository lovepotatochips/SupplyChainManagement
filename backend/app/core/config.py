from pydantic_settings import BaseSettings  # 导入Pydantic的设置基类，用于读取配置
from functools import lru_cache  # 导入LRU缓存装饰器，用于缓存配置对象


class Settings(BaseSettings):
    """应用配置类，定义所有配置项"""
    
    PROJECT_NAME: str = "SCM供应链管理系统"  # 项目名称
    VERSION: str = "1.0.0"  # 项目版本号
    
    API_V1_STR: str = "/api/v1"  # API v1版本的前缀路径
    
    SECRET_KEY: str = "your-secret-key-change-in-production"  # JWT加密密钥，生产环境必须修改
    ALGORITHM: str = "HS256"  # JWT加密算法，使用HMAC SHA-256
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 访问令牌过期时间，单位为分钟，这里设置为7天
    
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/scm_db?charset=utf8mb4"  # 数据库连接字符串
    
    MYSQL_HOST: str = "localhost"  # MySQL服务器地址
    MYSQL_PORT: int = 3306  # MySQL服务器端口
    MYSQL_USER: str = "root"  # MySQL用户名
    MYSQL_PASSWORD: str = "123456"  # MySQL密码
    MYSQL_DATABASE: str = "scm_db"  # 数据库名称
    
    REDIS_URL: str = "redis://localhost:6379/0"  # Redis连接字符串，用于缓存（可选）
    
    CORS_ORIGINS: list = ["http://localhost:5173", "http://localhost:3000"]  # 允许跨域访问的来源列表
    
    class Config:
        """Pydantic配置类"""
        env_file = ".env"  # 指定环境变量文件路径，从.env文件读取配置

    @property
    def get_database_url(self) -> str:
        """动态生成数据库连接URL"""
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"


@lru_cache()
def get_settings():
    """
    获取配置实例（使用缓存优化）
    
    使用LRU缓存装饰器，确保配置对象只创建一次
    多次调用get_settings()会返回同一个对象，提高性能
    """
    return Settings()
