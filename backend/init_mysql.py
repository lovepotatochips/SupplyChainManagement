# -*- coding: utf-8 -*-
"""
MySQL 数据库初始化脚本
创建数据库和表结构

本脚本用于初始化MySQL数据库，包括创建数据库和创建数据表
在首次部署系统或重置数据库时运行此脚本
"""
import sys
from sqlalchemy import create_engine, text
from app.core.config import get_settings

settings = get_settings()


def create_database():
    """
    创建MySQL数据库（如果不存在）
    
    功能说明:
        1. 连接到MySQL服务器（不指定数据库）
        2. 检查目标数据库是否已存在
        3. 如果不存在，则创建数据库
        4. 设置数据库字符集为utf8mb4，支持完整的Unicode字符
    
    技术细节:
        - 使用text()函数执行原生SQL语句
        - 使用SHOW DATABASES语句检查数据库是否存在
        - 使用CREATE DATABASE语句创建数据库
        - utf8mb4字符集支持emoji等特殊字符
    """
    mysql_url = f"mysql+pymysql://{settings.MYSQL_USER}:{settings.MYSQL_PASSWORD}@{settings.MYSQL_HOST}:{settings.MYSQL_PORT}?charset=utf8mb4"
    
    engine = create_engine(mysql_url)
    
    with engine.connect() as conn:
        result = conn.execute(text(f"SHOW DATABASES LIKE '{settings.MYSQL_DATABASE}'"))
        exists = result.fetchone()
        
        if not exists:
            conn.execute(text(f"CREATE DATABASE `{settings.MYSQL_DATABASE}` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"))
            conn.commit()
            print(f"✓ 数据库 '{settings.MYSQL_DATABASE}' 创建成功")
        else:
            print(f"✓ 数据库 '{settings.MYSQL_DATABASE}' 已存在")


def create_tables():
    """
    创建所有数据表
    
    功能说明:
        1. 调用init_db函数
        2. init_db会根据所有模型类自动创建对应的数据表
        3. 表结构由模型类的字段定义决定
    
    技术细节:
        - 使用SQLAlchemy的ORM功能
        - 自动根据模型类生成CREATE TABLE语句
        - 包含所有的字段类型、约束、索引等
    """
    from app.db.session import init_db
    init_db()
    print("✓ 数据表创建成功")


def main():
    """
    主函数 - 数据库初始化流程
    
    功能说明:
        1. 显示数据库配置信息
        2. 执行创建数据库
        3. 执行创建数据表
        4. 显示初始化结果或错误信息
    
    异常处理:
        - 捕获所有异常并打印错误信息
        - 使用traceback打印详细的错误堆栈
        - 发生错误时退出程序并返回错误码1
    """
    print("=" * 60)
    print("MySQL 数据库初始化")
    print("=" * 60)
    print(f"\n数据库配置:")
    print(f"  主机: {settings.MYSQL_HOST}")
    print(f"  端口: {settings.MYSQL_PORT}")
    print(f"  用户: {settings.MYSQL_USER}")
    print(f"  数据库: {settings.MYSQL_DATABASE}")
    print()
    
    try:
        print("步骤 1: 创建数据库...")
        create_database()
        
        print("\n步骤 2: 创建数据表...")
        create_tables()
        
        print("\n" + "=" * 60)
        print("数据库初始化完成！")
        print("=" * 60)
        print("\n下一步: 运行 'python init_test_data.py' 初始化测试数据")
        
    except Exception as e:
        print(f"\n❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
