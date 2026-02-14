<<<<<<< HEAD
# 供应链管理系统 (SCM)

<div align="center">

一套现代化的企业级供应链管理系统，采用前后端分离架构设计

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.4-green.svg)](https://vuejs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-red.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

## 项目简介

SCM (Supply Chain Management) 是一个功能完善的供应链管理系统，旨在帮助企业实现采购、库存、销售等供应链环节的数字化管理。系统采用现代化的技术栈，提供友好的用户界面和强大的数据分析功能。

### 核心特性

- 前后端分离架构，易于部署和扩展
- 基于 RBAC 的权限管理系统
- 完整的供应链业务流程管理
- 丰富的数据分析和可视化报表
- 响应式设计，支持多设备访问
- 完善的 API 文档和开发规范

## 技术栈

### 前端技术
- **框架**: Vue 3.4+ (Composition API)
- **语言**: TypeScript 5.3+
- **UI组件库**: Element Plus 2.8+
- **路由管理**: Vue Router 4.2+
- **状态管理**: Pinia 2.1+
- **HTTP客户端**: Axios 1.6+
- **数据可视化**: ECharts 5.5+
- **日期处理**: Day.js 1.11+
- **构建工具**: Vite 5.0+
- **代码规范**: ESLint + Prettier

### 后端技术
- **框架**: FastAPI 0.115+
- **语言**: Python 3.12+
- **ORM**: SQLAlchemy 2.0+
- **数据验证**: Pydantic 2.10+
- **认证**: JWT (python-jose)
- **密码加密**: Passlib + Bcrypt
- **数据库**: MySQL 8.0+
- **CORS**: FastAPI CORS Middleware
- **环境配置**: python-dotenv

### 开发工具
- **API文档**: Swagger UI (FastAPI内置)
- **代码格式化**: Black (Python)
- **类型检查**: mypy
- **包管理**: pip + virtualenv / npm

## 项目结构

```
SCM/
├── backend/                          # 后端项目
│   ├── app/
│   │   ├── api/                     # API 路由
│   │   │   └── v1/                  # API v1版本
│   │   │       ├── auth/            # 认证相关接口
│   │   │       ├── finance/         # 财务管理接口
│   │   │       ├── supply/          # 供应链管理接口
│   │   │       ├── system/          # 系统管理接口
│   │   │       └── analysis/        # 数据分析接口
│   │   ├── core/                    # 核心配置
│   │   │   ├── config.py            # 配置管理
│   │   │   ├── deps.py              # 依赖注入
│   │   │   └── security.py          # 安全相关
│   │   ├── db/                      # 数据库配置
│   │   │   ├── base.py              # 数据库基类
│   │   │   └── session.py           # 数据库会话
│   │   ├── models/                  # SQLAlchemy 数据模型
│   │   │   ├── user.py              # 用户模型
│   │   │   ├── department.py        # 部门模型
│   │   │   ├── supplier.py          # 供应商模型
│   │   │   ├── purchase.py          # 采购模型
│   │   │   ├── inventory.py         # 库存模型
│   │   │   ├── sales.py             # 销售模型
│   │   │   ├── finance.py           # 财务模型
│   │   │   └── workflow.py          # 工作流模型
│   │   ├── schemas/                 # Pydantic 数据模型
│   │   │   ├── user.py              # 用户Schema
│   │   │   ├── department.py        # 部门Schema
│   │   │   ├── supplier.py          # 供应商Schema
│   │   │   ├── purchase.py          # 采购Schema
│   │   │   ├── inventory.py         # 库存Schema
│   │   │   ├── sales.py             # 销售Schema
│   │   │   ├── finance.py           # 财务Schema
│   │   │   └── menu.py              # 菜单Schema
│   │   └── utils/                   # 工具函数
│   │       └── helpers.py           # 辅助函数
│   ├── main.py                      # 应用入口
│   ├── requirements.txt             # Python依赖包
│   ├── init_db.py                   # 数据库初始化脚本
│   ├── create_admin.py              # 创建管理员脚本
│   ├── init_test_data.py            # 初始化测试数据
│   ├── .env.example                 # 环境变量示例
│   └── .gitignore                   # Git忽略文件
│
├── frontend/                        # 前端项目
│   ├── public/                      # 静态资源
│   ├── src/
│   │   ├── api/                     # API 接口定义
│   │   │   ├── auth.ts              # 认证接口
│   │   │   ├── user.ts              # 用户接口
│   │   │   ├── department.ts        # 部门接口
│   │   │   ├── supplier.ts          # 供应商接口
│   │   │   ├── purchase.ts          # 采购接口
│   │   │   ├── inventory.ts         # 库存接口
│   │   │   ├── sales.ts             # 销售接口
│   │   │   └── finance.ts           # 财务接口
│   │   ├── assets/                  # 资源文件
│   │   ├── components/              # 公共组件
│   │   ├── router/                  # 路由配置
│   │   │   └── index.ts             # 路由定义
│   │   ├── store/                   # 状态管理
│   │   │   ├── modules/            # 模块化store
│   │   │   └── index.ts            # Store入口
│   │   ├── types/                   # TypeScript类型定义
│   │   │   └── index.ts             # 类型声明
│   │   ├── utils/                   # 工具函数
│   │   │   └── request.ts           # Axios封装
│   │   └── views/                   # 页面视图
│   │       ├── Login.vue            # 登录页面
│   │       ├── Dashboard.vue        # 仪表板
│   │       ├── Layout.vue           # 布局组件
│   │       ├── system/              # 系统管理模块
│   │       │   ├── Users.vue        # 用户管理
│   │       │   ├── Roles.vue        # 角色管理
│   │       │   └── Departments.vue  # 部门管理
│   │       ├── supply/              # 供应链模块
│   │       │   ├── Suppliers.vue    # 供应商管理
│   │       │   ├── Purchase.vue     # 采购管理
│   │       │   ├── Inventory.vue    # 库存管理
│   │       │   └── Sales.vue        # 销售管理
│   │       ├── finance/             # 财务管理模块
│   │       │   ├── Payments.vue     # 付款管理
│   │       │   ├── Bills.vue        # 账单管理
│   │       │   └── Accounts.vue     # 账户管理
│   │       └── analysis/            # 数据分析模块
│   │           ├── PurchaseAnalysis.vue  # 采购分析
│   │           ├── SalesAnalysis.vue     # 销售分析
│   │           ├── InventoryAnalysis.vue # 库存分析
│   │           └── SupplierAnalysis.vue  # 供应商分析
│   ├── .env                         # 环境变量
│   ├── .eslintrc.js                 # ESLint配置
│   ├── .prettierrc                  # Prettier配置
│   ├── index.html                   # HTML模板
│   ├── package.json                 # Node.js依赖包
│   ├── tsconfig.json                # TypeScript配置
│   ├── vite.config.ts               # Vite配置
│   └── .gitignore                   # Git忽略文件
│
└── README.md                        # 项目说明文档
```

## 功能模块

### 系统管理
- **用户管理**: 用户的增删改查，支持部门关联和状态管理
- **角色管理**: 角色的创建和权限分配
- **权限管理**: 细粒度的权限控制，基于RBAC模型
- **部门管理**: 树形结构的部门组织管理，支持多层级

### 供应链管理
- **供应商管理**: 供应商信息维护，包括基本信息、联系方式、评级等
- **采购管理**: 采购订单的创建、审核、入库全流程管理
- **库存管理**: 商品库存的实时监控、入库出库、盘点管理
- **销售管理**: 销售订单管理、客户信息维护、发货跟踪

### 财务管理
- **付款管理**: 应付款项的管理和付款记录
- **账单管理**: 各类账单的生成和管理
- **账户管理**: 银行账户信息维护

### 数据分析
- **采购分析**: 采购数据统计和趋势分析
- **销售分析**: 销售业绩分析和报表生成
- **库存分析**: 库存周转率、库存预警等分析
- **供应商分析**: 供应商绩效评估

## 快速开始

### 环境要求

- **Python**: 3.12 或更高版本
- **Node.js**: 18.0 或更高版本
- **MySQL**: 8.0 或更高版本
- **npm**: 9.0 或更高版本

### 后端安装与启动

#### 1. 克隆项目

```bash
git clone <repository-url>
cd SCM
```

#### 2. 创建虚拟环境并安装依赖

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### 3. 配置数据库

复制 `.env.example` 为 `.env`，根据实际情况修改配置：

```env
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=scm_db
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/scm_db?charset=utf8mb4

# 安全配置
SECRET_KEY=your-secret-key-change-this-in-production-use-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=43200

# CORS配置
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]

# Redis配置 (可选)
REDIS_URL=redis://localhost:6379/0
```

#### 4. 创建数据库

在MySQL中创建数据库：

```sql
CREATE DATABASE scm_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

或者使用提供的初始化脚本：

```bash
python init_mysql.py
```

#### 5. 初始化数据库表结构

```bash
python init_db.py
```

#### 6. 创建管理员账户

```bash
python create_admin.py
```

默认管理员账号：
- 用户名: `admin`
- 密码: `admin123`

#### 7. 初始化测试数据（可选）

```bash
python init_test_data.py
```

#### 8. 启动后端服务

开发模式（支持热重载）：

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

生产模式：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

后端服务将在 http://localhost:8000 启动

API文档地址：http://localhost:8000/docs

健康检查：http://localhost:8000/health

### 前端安装与启动

#### 1. 进入前端目录

```bash
cd frontend
```

#### 2. 安装依赖

```bash
npm install
```

如果安装速度慢，可以使用淘宝镜像：

```bash
npm install --registry=https://registry.npmmirror.com
```

#### 3. 配置环境变量

创建 `.env` 文件（如果不存在）：

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_TITLE=SCM供应链管理系统
```

#### 4. 启动开发服务器

```bash
npm run dev
```

前端服务将在 http://localhost:5173 启动

#### 5. 构建生产版本

```bash
npm run build
```

构建产物将生成在 `dist` 目录中。

#### 6. 预览生产版本

```bash
npm run preview
```

## 默认账号

系统初始化后，可以使用以下默认账号登录：

- **用户名**: admin
- **密码**: admin123
- **权限**: 超级管理员（拥有所有权限）

登录后请立即修改默认密码以确保安全。

## 开发指南

### 后端开发

#### 添加新的 API 接口

1. **定义数据模型 (Schemas)**

在 `backend/app/schemas/` 中创建 Pydantic 模型：

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None

class ItemResponse(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

2. **创建数据库模型**

在 `backend/app/models/` 中创建 SQLAlchemy 模型：

```python
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
```

3. **创建 API 路由**

在 `backend/app/api/v1/` 中创建路由文件：

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.db.session import get_db
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse
from app.models.item import Item

router = APIRouter()

@router.post("/", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemResponse])
def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items

@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, item: ItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    for field, value in item.dict(exclude_unset=True).items():
        setattr(db_item, field, value)
    
    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}
```

4. **注册路由**

在 `backend/app/api/v1/__init__.py` 中注册路由：

```python
from fastapi import APIRouter
from app.api.v1 import auth, finance, supply, system, analysis, item

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["认证"])
api_router.include_router(finance.router, prefix="/finance", tags=["财务管理"])
api_router.include_router(supply.router, prefix="/supply", tags=["供应链"])
api_router.include_router(system.router, prefix="/system", tags=["系统管理"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["数据分析"])
api_router.include_router(item.router, prefix="/items", tags=["项目管理"])
```

#### 数据库迁移

如果需要修改数据库结构，建议使用Alembic进行版本管理：

```bash
pip install alembic
alembic init migrations
alembic revision --autogenerate -m "描述"
alembic upgrade head
```

### 前端开发

#### 添加新的前端页面

1. **创建页面组件**

在 `frontend/src/views/` 中创建 Vue 组件：

```vue
<template>
  <div class="item-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>项目管理</span>
          <el-button type="primary" @click="handleCreate">新建</el-button>
        </div>
      </template>
      
      <el-table :data="items" v-loading="loading">
        <el-table-column prop="name" label="名称" />
        <el-table-column prop="description" label="描述" />
        <el-table-column prop="price" label="价格" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="handleEdit(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" :rules="rules" ref="formRef" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="form.description" type="textarea" />
        </el-form-item>
        <el-form-item label="价格" prop="price">
          <el-input-number v-model="form.price" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getItems, createItem, updateItem, deleteItem } from '@/api/item'

interface Item {
  id: number
  name: string
  description?: string
  price: number
}

const items = ref<Item[]>([])
const loading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const formRef = ref()
const form = ref({
  id: null as number | null,
  name: '',
  description: '',
  price: 0
})

const rules = {
  name: [{ required: true, message: '请输入名称', trigger: 'blur' }],
  price: [{ required: true, message: '请输入价格', trigger: 'blur' }]
}

const fetchItems = async () => {
  loading.value = true
  try {
    items.value = await getItems()
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleCreate = () => {
  dialogTitle.value = '新建项目'
  form.value = { id: null, name: '', description: '', price: 0 }
  dialogVisible.value = true
}

const handleEdit = (row: Item) => {
  dialogTitle.value = '编辑项目'
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = async (row: Item) => {
  try {
    await ElMessageBox.confirm('确认删除该项目吗？', '提示', {
      type: 'warning'
    })
    await deleteItem(row.id)
    ElMessage.success('删除成功')
    fetchItems()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return
  
  try {
    await formRef.value.validate()
    if (form.value.id) {
      await updateItem(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createItem(form.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchItems()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchItems()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
</style>
```

2. **创建 API 接口**

在 `frontend/src/api/` 中创建 API 文件：

```typescript
import request from '@/utils/request'

export interface Item {
  id?: number
  name: string
  description?: string
  price: number
}

export const getItems = () => {
  return request<Item[]>({
    url: '/api/v1/items/',
    method: 'get'
  })
}

export const getItem = (id: number) => {
  return request<Item>({
    url: `/api/v1/items/${id}`,
    method: 'get'
  })
}

export const createItem = (data: Item) => {
  return request<Item>({
    url: '/api/v1/items/',
    method: 'post',
    data
  })
}

export const updateItem = (id: number, data: Item) => {
  return request<Item>({
    url: `/api/v1/items/${id}`,
    method: 'put',
    data
  })
}

export const deleteItem = (id: number) => {
  return request({
    url: `/api/v1/items/${id}`,
    method: 'delete'
  })
}
```

3. **添加路由配置**

在 `frontend/src/router/index.ts` 中添加路由：

```typescript
{
  path: 'items',
  name: 'Items',
  component: () => import('@/views/Items.vue'),
  meta: { title: '项目管理', icon: 'Box' }
}
```

#### 状态管理

使用 Pinia 进行状态管理：

```typescript
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useItemStore = defineStore('item', () => {
  const items = ref([])
  const loading = ref(false)

  const fetchItems = async () => {
    loading.value = true
    try {
      const data = await getItems()
      items.value = data
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    fetchItems
  }
})
```

## 部署指南

### 后端部署

#### 使用 Gunicorn (推荐)

```bash
pip install gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

#### 使用 Docker

创建 `Dockerfile`：

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

构建和运行：

```bash
docker build -t scm-backend .
docker run -p 8000:8000 scm-backend
```

### 前端部署

#### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        root /var/www/scm/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 常见问题

### 1. 数据库连接失败

确保 MySQL 服务正在运行，并且配置的连接信息正确。

### 2. CORS 错误

检查后端 `CORS_ORIGINS` 配置是否包含前端地址。

### 3. 前端接口请求失败

确认后端服务已启动，并检查 API 地址配置。

### 4. 权限不足

确保用户已登录并拥有相应权限，检查 JWT token 是否有效。

## 开发规范

### 代码风格

- **Python**: 遵循 PEP 8 规范，使用 Black 格式化代码
- **TypeScript**: 遵循 ESLint 和 Prettier 配置
- **Vue**: 使用 Composition API 和 `<script setup>` 语法

### Git 提交规范

```
feat: 新功能
fix: 修复bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具相关
```

## 许可证

MIT License

Copyright (c) 2025 SCM供应链管理系统

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


<div align="center">
Made with ❤️ by SCM Team
</div>
=======
# SupplyChainManagement
一个基于用 Vue 3 + FastAPI 的现代化供应链管理系统，提供采购、销售、库存、财务等全流程管理功能
>>>>>>> e36bdaffd82a4d30623e2e51653f04a0986fbce1
