# 供应链管理系统 (SCM)

一个功能完善的供应链管理系统，采用前后端分离架构，前端使用Vue3+Element Plus，后端使用Python3+FastAPI。

## 项目简介

供应链管理系统(SCM)是一套完整的企业级供应链管理解决方案，涵盖供应商管理、采购管理、库存管理、销售管理、财务管理等核心业务功能，帮助企业实现供应链数字化管理，提高运营效率。

## 技术栈

### 前端技术

- **框架**: Vue 3.4+
- **UI组件库**: Element Plus 2.4+
- **状态管理**: Pinia 2.1+
- **路由管理**: Vue Router 4.2+
- **HTTP客户端**: Axios 1.6+
- **图表库**: ECharts 5.4+
- **构建工具**: Vite 5.0+
- **语言**: TypeScript 5.0+

### 后端技术

- **框架**: FastAPI 0.104+
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0+
- **数据验证**: Pydantic 2.5+
- **认证授权**: JWT (python-jose)
- **密码加密**: passlib
- **Web服务器**: Uvicorn
- **语言**: Python 3.13+

## 功能模块

### 系统管理
- 用户管理：用户增删改查、密码管理
- 角色管理：角色配置、权限分配
- 部门管理：部门层级管理
- 菜单管理：菜单配置、权限控制

### 供应链管理
- 供应商管理：供应商信息维护、供应商评估
- 采购管理：采购订单管理、采购审批流程
- 库存管理：产品管理、仓库管理、出入库管理、库存盘点
- 销售管理：客户管理、销售订单管理

### 财务管理
- 付款管理：供应商付款、客户退款
- 收款管理：客户收款、供应商退款
- 账单管理：应收账款、应付账款
- 账户管理：银行账户、现金账户
- 报表分析：财务汇总、采购分析、销售分析、库存分析

### 报表分析
- 仪表盘：关键业务指标展示
- 财务报表：收支统计、应收应付分析
- 采购报表：采购趋势、供应商分析
- 销售报表：销售趋势、客户分析
- 库存报表：库存状态、库存预警

## 项目结构

```
SCM/
├── backend/                 # 后端项目
│   ├── app/
│   │   ├── api/            # API接口
│   │   ├── core/           # 核心配置
│   │   ├── db/             # 数据库
│   │   ├── models/         # 数据模型
│   │   ├── schemas/        # 数据验证
│   │   └── utils/          # 工具函数
│   ├── main.py             # 应用入口
│   └── requirements.txt    # 依赖包
├── frontend/               # 前端项目
│   ├── src/
│   │   ├── api/            # API接口
│   │   ├── assets/         # 静态资源
│   │   ├── components/     # 组件
│   │   ├── layouts/        # 布局
│   │   ├── router/         # 路由
│   │   ├── store/          # 状态管理
│   │   ├── types/          # 类型定义
│   │   ├── utils/          # 工具函数
│   │   └── views/          # 页面
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
├── docs/                   # 文档
│   ├── 需求说明书.md
│   ├── 数据库说明书.md
│   ├── 前端页面说明书.md
│   ├── 后端接口说明书.md
│   ├── 操作手册.md
│   ├── 功能清单.md
│   └── 建设方案.md
├── .gitignore
├── README.md
└── start.bat              # 启动脚本
```

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.13+
- MySQL 8.0+
- npm 或 yarn

### 安装步骤

#### 1. 克隆项目

```bash
git clone https://github.com/your-repo/SCM.git
cd SCM
```

#### 2. 配置数据库

创建MySQL数据库：

```sql
CREATE DATABASE scm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 3. 配置后端

进入后端目录：

```bash
cd backend
```

创建虚拟环境并安装依赖：

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

配置数据库连接（编辑 `.env` 文件）：

```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/scm_db
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

初始化数据库：

```bash
python init_db.py
```

创建管理员账户：

```bash
python create_admin.py
```

启动后端服务：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 4. 配置前端

进入前端目录：

```bash
cd frontend
```

安装依赖：

```bash
npm install
```

配置API地址（编辑 `.env` 文件）：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=供应链管理系统
```

启动前端服务：

```bash
npm run dev
```

#### 5. 访问系统

打开浏览器访问：http://localhost:5173

默认管理员账号：
- 用户名: `admin`
- 密码: `admin123`

### 使用启动脚本

Windows系统可以直接运行：

```bash
start.bat
```

这将同时启动前后端服务。

## 开发指南

### 后端开发

#### 添加新的API接口

1. 在 `app/api/v1/` 下创建或编辑模块
2. 在 `app/schemas/` 下定义数据模型
3. 在 `app/models/` 下定义数据库模型
4. 在 `app/api/v1/__init__.py` 中注册路由

#### 数据库迁移

项目使用SQLAlchemy ORM，表结构由代码自动创建。如需手动管理迁移，可以使用Alembic工具。

### 前端开发

#### 添加新页面

1. 在 `src/views/` 下创建页面组件
2. 在 `src/router/index.ts` 中添加路由配置
3. 在 `src/api/` 下添加API接口方法
4. 在侧边栏菜单中添加菜单项

#### 状态管理

使用Pinia进行状态管理，store文件位于 `src/store/` 目录。

## 部署指南

### 生产环境部署

#### 后端部署

1. 使用Gunicorn或Uvicorn作为ASGI服务器
2. 配置Nginx作为反向代理
3. 使用Supervisor管理进程

示例Nginx配置：

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location /api {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }
}
```

#### 前端部署

1. 构建生产版本：

```bash
npm run build
```

2. 将 `dist` 目录部署到Web服务器

### Docker部署

#### 后端Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### 前端Dockerfile

```dockerfile
FROM node:18-alpine as builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 常见问题

### 数据库连接失败

检查：
- MySQL服务是否启动
- 数据库配置是否正确
- 用户名密码是否正确

### 前端无法访问后端

检查：
- 后端服务是否启动
- 跨域配置是否正确
- API地址配置是否正确

### 登录失败

检查：
- 用户名密码是否正确
- 用户状态是否启用
- JWT配置是否正确

## 测试

### 后端测试

```bash
cd backend
pytest
```

### 前端测试

```bash
cd frontend
npm run test
```

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 许可证

本项目采用MIT许可证。

## 联系方式

- 项目主页: https://github.com/your-repo/SCM
- 问题反馈: https://github.com/your-repo/SCM/issues
- 邮箱: support@example.com

## 更新日志

### v1.0.0 (2026-02-13)

- 初始版本发布
- 实现核心业务功能
- 完成基础文档

## 致谢

感谢所有为本项目做出贡献的开发者！

## 技术支持

如需技术支持，请通过以下方式联系我们：

- 提交Issue到GitHub仓库
- 发送邮件至support@example.com
- 加入我们的Discord社区

---

**祝使用愉快！**
