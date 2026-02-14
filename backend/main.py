from fastapi import FastAPI  # 导入FastAPI主应用类
from fastapi.middleware.cors import CORSMiddleware  # 导入CORS中间件，用于处理跨域请求
from app.core.config import get_settings  # 导入配置获取函数
from app.db.session import engine  # 导入数据库引擎
from app.api.v1 import api_router  # 导入API路由器

# 获取应用配置
settings = get_settings()

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.PROJECT_NAME,  # 项目名称
    version=settings.VERSION,  # API版本号
    description="供应链管理系统API"  # API描述信息
)

# 配置CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # 允许的源地址列表
    allow_credentials=True,  # 允许携带凭证
    allow_methods=["*"],  # 允许所有HTTP方法
    allow_headers=["*"],  # 允许所有请求头
)

# 包含API v1路由，设置前缀
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")  # 定义根路径路由
def read_root():
    """返回欢迎信息和基本API信息"""
    return {
        "message": "欢迎使用SCM供应链管理系统API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")  # 定义健康检查路由
def health_check():
    """健康检查接口，用于监控服务状态"""
    return {"status": "healthy"}


if __name__ == "__main__":  # 当脚本直接运行时
    import uvicorn  # 导入uvicorn服务器
    # 启动ASGI服务器，监听所有网络接口，端口8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
