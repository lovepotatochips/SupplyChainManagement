import random
import string
from datetime import datetime


def generate_code(prefix: str) -> str:
    """
    生成业务编码
    
    编码格式：前缀 + 日期(YYYYMMDD) + 4位随机数字
    例如：PO202602140123
    """
    timestamp = datetime.now().strftime("%Y%m%d")
    random_str = ''.join(random.choices(string.digits, k=4))
    return f"{prefix}{timestamp}{random_str}"


def generate_code_with_date(prefix: str) -> str:
    """
    生成带日期的业务编码
    
    调用generate_code函数生成编码
    保持接口兼容性
    """
    return generate_code(prefix)


def paginate(query, skip: int = 0, limit: int = 100):
    """
    分页查询
    
    对SQLAlchemy查询进行分页处理
    返回总数和分页后的数据列表
    """
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return total, items
