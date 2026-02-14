from typing import List  # 导入List类型，用于类型提示
from fastapi import APIRouter, Depends, HTTPException, Query  # 导入FastAPI的核心组件
from sqlalchemy.orm import Session  # 导入数据库会话
from app.db.session import get_db  # 导入数据库会话依赖注入函数
from app.core.deps import PermissionChecker  # 导入权限检查依赖
from app.models import User  # 导入用户模型
from app.schemas.department import DepartmentCreate, DepartmentResponse, DepartmentUpdate, DepartmentTree  # 导入部门相关的Schema

router = APIRouter()
# 创建API路由器实例
# 用于定义所有的部门相关路由


@router.get("/", response_model=List[DepartmentResponse])
def get_departments(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: User = Depends(PermissionChecker("department:read")),
    db: Session = Depends(get_db)
):
    """
    获取部门列表接口
    
    参数:
        skip: 跳过的记录数，用于分页，默认为0，最小值为0
        limit: 每页的记录数，默认为100，最小为1，最大为100
        current_user: 当前登录的用户，需要department:read权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        List[DepartmentResponse]: 部门列表
    
    说明:
        - 支持分页查询
        - 返回扁平的部门列表
        - 需要department:read权限
    """
    from app.models import Department
    # 导入部门模型
    
    departments = db.query(Department).offset(skip).limit(limit).all()
    # 查询部门列表
    # offset(skip): 跳过前skip条记录
    # limit(limit): 最多返回limit条记录
    # all(): 获取所有结果
    
    return departments


@router.get("/tree", response_model=List[DepartmentTree])
def get_department_tree(
    current_user: User = Depends(PermissionChecker("department:read")),
    db: Session = Depends(get_db)
):
    """
    获取部门树形结构接口
    
    参数:
        current_user: 当前登录的用户，需要department:read权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        List[DepartmentTree]: 部门树形结构，包含子部门和用户数量
    
    说明:
        - 返回完整的部门树形结构
        - 每个部门包含其用户数量
        - 需要department:read权限
    """
    from app.models import Department
    # 导入部门模型
    
    departments = db.query(Department).all()
    # 查询所有部门
    
    user_counts = {}
    # 创建字典，存储每个部门的用户数量
    # 键：部门ID，值：用户数量
    
    for dept in departments:
        # 遍历所有部门
        user_count = db.query(User).filter(User.department_id == dept.id).count()
        # 查询该部门的用户数量
        # filter(User.department_id == dept.id): 筛选该部门的用户
        # count(): 统计符合条件的记录数
        
        user_counts[dept.id] = user_count
        # 将用户数量存入字典
    
    def build_tree(parent_id=None):
        """
        递归构建部门树形结构
        
        参数:
            parent_id: 父部门ID，None表示顶级部门
        
        返回:
            list: 包含所有子部门的列表
        
        说明:
            使用递归算法构建树形结构
            先找到所有顶级部门，然后递归查找每个部门的子部门
        """
        result = []
        # 存储当前层级的部门列表
        
        for dept in departments:
            # 遍历所有部门
            if dept.parent_id == parent_id:
                # 如果部门的parent_id等于当前parent_id，说明它是子部门
                dept_dict = {
                    **dept.to_dict(),
                    # 将部门对象转换为字典
                    # **展开字典，将所有字段添加到新字典中
                    
                    "children": build_tree(dept.id),
                    # 递归调用，构建子部门树
                    # 传入当前部门的ID作为parent_id
                    # 返回该部门的所有子部门
                    
                    "user_count": user_counts.get(dept.id, 0)
                    # 添加用户数量
                    # get(dept.id, 0): 从字典中获取，如果不存在则返回0
                }
                # 构建部门字典，包含部门信息和子部门
                
                result.append(dept_dict)
                # 将部门添加到结果列表
        
        return result
        # 返回当前层级的部门列表
    
    return build_tree()
    # 调用build_tree函数，从顶级部门开始构建树
    # 不传parent_id参数，默认为None，查找所有顶级部门


@router.get("/{dept_id}", response_model=DepartmentResponse)
def get_department(
    dept_id: int,
    current_user: User = Depends(PermissionChecker("department:read")),
    db: Session = Depends(get_db)
):
    """
    获取单个部门信息接口
    
    参数:
        dept_id: 部门ID，路径参数
        current_user: 当前登录的用户，需要department:read权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        DepartmentResponse: 部门详细信息
    
    异常:
        HTTPException: 当部门不存在时抛出404错误
    
    说明:
        - 根据部门ID查询部门信息
        - 需要department:read权限
    """
    from app.models import Department
    # 导入部门模型
    
    dept = db.query(Department).filter(Department.id == dept_id).first()
    # 根据ID查询部门
    # first(): 返回第一条匹配的记录，如果没有则返回None
    
    if not dept:
        # 如果部门不存在，抛出404异常
        raise HTTPException(status_code=404, detail="Department not found")
    
    return dept


@router.post("/", response_model=DepartmentResponse)
def create_department(
    dept: DepartmentCreate,
    current_user: User = Depends(PermissionChecker("department:create")),
    db: Session = Depends(get_db)
):
    """
    创建部门接口
    
    参数:
        dept: 部门创建数据，包含部门名称、编码等信息
        current_user: 当前登录的用户，需要department:create权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        DepartmentResponse: 创建成功的部门信息
    
    说明:
        - 创建新部门
        - 支持设置父部门，构建多级结构
        - 需要department:create权限
    """
    from app.models import Department
    from app.utils.helpers import generate_code
    # 导入部门模型和辅助函数
    
    db_dept = Department(**dept.model_dump())
    # 创建部门对象
    # **dept.model_dump(): 将Schema对象转换为字典
    
    db.add(db_dept)
    # 添加到数据库会话
    
    db.commit()
    # 提交事务
    
    db.refresh(db_dept)
    # 刷新对象，获取生成的id等字段
    
    return db_dept


@router.put("/{dept_id}", response_model=DepartmentResponse)
def update_department(
    dept_id: int,
    dept_update: DepartmentUpdate,
    current_user: User = Depends(PermissionChecker("department:update")),
    db: Session = Depends(get_db)
):
    """
    更新部门信息接口
    
    参数:
        dept_id: 部门ID，路径参数
        dept_update: 部门更新数据，包含要更新的字段
        current_user: 当前登录的用户，需要department:update权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        DepartmentResponse: 更新后的部门信息
    
    异常:
        HTTPException: 当部门不存在时抛出404错误
    
    说明:
        - 只更新传入的字段，其他字段保持不变
        - 部门编码通常不允许修改
        - 需要department:update权限
    """
    from app.models import Department
    # 导入部门模型
    
    db_dept = db.query(Department).filter(Department.id == dept_id).first()
    # 根据ID查询部门
    
    if not db_dept:
        # 如果部门不存在，抛出异常
        raise HTTPException(status_code=404, detail="Department not found")
    
    for field, value in dept_update.model_dump(exclude_unset=True).items():
        # 遍历所有要更新的字段
        # exclude_unset=True: 只包含实际设置了值的字段
        setattr(db_dept, field, value)
        # 动态设置对象的属性值
    
    db.commit()
    # 提交事务
    
    db.refresh(db_dept)
    # 刷新对象
    
    return db_dept


@router.delete("/{dept_id}")
def delete_department(
    dept_id: int,
    current_user: User = Depends(PermissionChecker("department:delete")),
    db: Session = Depends(get_db)
):
    """
    删除部门接口
    
    参数:
        dept_id: 部门ID，路径参数
        current_user: 当前登录的用户，需要department:delete权限
        db: 数据库会话，通过依赖注入自动获取
    
    返回:
        dict: 包含成功消息的字典
    
    异常:
        HTTPException: 当部门不存在时抛出404错误
    
    说明:
        - 根据部门ID删除部门
        - 需要确保部门下没有子部门和用户
        - 需要department:delete权限
    """
    from app.models import Department
    # 导入部门模型
    
    db_dept = db.query(Department).filter(Department.id == dept_id).first()
    # 根据ID查询部门
    
    if not db_dept:
        # 如果部门不存在，抛出异常
        raise HTTPException(status_code=404, detail="Department not found")
    
    db.delete(db_dept)
    # 删除部门对象
    
    db.commit()
    # 提交事务
    
    return {"message": "Department deleted successfully"}
