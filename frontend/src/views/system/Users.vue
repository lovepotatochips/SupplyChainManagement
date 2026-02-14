<template>
  <div class="users-page">
    <div class="users-layout">
      <!-- 左侧部门树区域：显示部门列表供用户筛选 -->
      <div class="department-tree">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>部门列表</span>
              <!-- 刷新按钮：点击重新加载部门树数据 -->
              <el-button text @click="handleRefreshDepartments">刷新</el-button>
            </div>
          </template>
          <!-- 部门树组件：展示部门层级结构 -->
          <!-- ref: 组件引用，用于操作树组件（如清除选中状态） -->
          <!-- :data: 树的数据源，从后端获取的部门树 -->
          <!-- :props: 树节点的属性配置，指定哪个字段显示为标签，哪个字段是子节点 -->
          <!-- :expand-on-click-node: 点击节点时不自动展开/收起 -->
          <!-- :default-expand-all: 默认展开所有节点 -->
          <!-- highlight-current: 高亮显示当前选中的节点 -->
          <!-- node-key: 节点的唯一标识字段 -->
          <!-- @node-click: 节点点击事件，点击部门后筛选该部门的用户 -->
          <el-tree
            ref="deptTreeRef"
            :data="departmentTree"
            :props="treeProps"
            :expand-on-click-node="false"
            :default-expand-all="true"
            highlight-current
            node-key="id"
            @node-click="handleNodeClick"
          />
        </el-card>
      </div>
      
      <!-- 右侧用户列表区域：显示用户信息和操作按钮 -->
      <div class="users-content">
        <el-card>
          <!-- 查询表单：提供用户名搜索功能 -->
          <el-form :inline="true" :model="queryForm">
            <el-form-item label="用户名">
              <!-- v-model: 双向绑定搜索关键词 -->
              <!-- clearable: 显示清除按钮，可快速清空输入 -->
              <el-input v-model="queryForm.keyword" placeholder="请输入用户名" clearable />
            </el-form-item>
            <el-form-item>
              <!-- 查询按钮：触发搜索，将页码重置为第一页 -->
              <el-button type="primary" @click="handleQuery">查询</el-button>
              <!-- 重置按钮：清空搜索条件和部门筛选，重新加载全部数据 -->
              <el-button @click="handleReset">重置</el-button>
              <!-- 新增按钮：打开新增用户对话框 -->
              <el-button type="primary" @click="handleAdd">新增</el-button>
            </el-form-item>
          </el-form>
          
          <!-- 用户表格：展示用户数据列表 -->
          <!-- stripe: 斑马纹样式，隔行变色提升可读性 -->
          <!-- v-loading: 数据加载时显示加载动画 -->
          <el-table :data="tableData" stripe v-loading="loading">
            <!-- 表格列定义：展示用户的各项信息 -->
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="username" label="用户名" />
            <el-table-column prop="real_name" label="真实姓名" />
            <el-table-column prop="department_name" label="部门" />
            <el-table-column prop="email" label="邮箱" />
            <el-table-column prop="phone" label="手机号" />
            <!-- 状态列：用不同颜色的标签显示启用/禁用状态 -->
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="row.status ? 'success' : 'danger'">
                  {{ row.status ? '启用' : '禁用' }}
                </el-tag>
              </template>
            </el-table-column>
            <!-- 超级管理员列：显示是否为超级管理员 -->
            <el-table-column label="超级管理员" width="120">
              <template #default="{ row }">
                <el-tag :type="row.is_superuser ? 'warning' : 'info'">
                  {{ row.is_superuser ? '是' : '否' }}
                </el-tag>
              </template>
            </el-table-column>
            <!-- 操作列：提供编辑、分配角色、删除等操作按钮 -->
            <!-- fixed="right": 固定在表格右侧，滚动时可见 -->
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
                <el-button link type="primary" @click="handleAssignRoles(row)">分配角色</el-button>
                <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <!-- 分页组件：控制表格数据的分页显示 -->
          <!-- v-model:current-page: 当前页码 -->
          <!-- v-model:page-size: 每页显示条数 -->
          <!-- :total: 数据总条数 -->
          <!-- :page-sizes: 可选的每页条数选项 -->
          <!-- layout: 分页组件布局，显示哪些元素 -->
          <!-- @size-change: 每页条数变化时触发，重新加载数据 -->
          <!-- @current-change: 页码变化时触发，重新加载数据 -->
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.size"
            :total="pagination.total"
            :page-sizes="[10, 20, 50, 100]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="loadData"
            @current-change="loadData"
            style="margin-top: 20px; justify-content: flex-end"
          />
        </el-card>
      </div>
    </div>
    
    <!-- 新增/编辑用户对话框 -->
    <!-- v-model: 控制对话框的显示/隐藏 -->
    <!-- :title: 对话框标题，根据操作动态变化 -->
    <!-- @close: 对话框关闭时触发，重置表单 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <!-- 用户表单：输入或编辑用户信息 -->
      <!-- :model: 表单数据对象 -->
      <!-- :rules: 表单验证规则 -->
      <!-- ref: 表单引用，用于调用验证和重置方法 -->
      <!-- label-width: 标签宽度，保持对齐美观 -->
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <!-- 新增时可输入，编辑时禁用，避免修改用户名 -->
          <el-input v-model="formData.username" placeholder="请输入用户名" :disabled="!!formData.id" />
        </el-form-item>
        <!-- 密码字段：仅在新增用户时显示，编辑时不显示密码输入框 -->
        <el-form-item label="密码" prop="password" v-if="!formData.id">
          <!-- type="password": 密码输入模式，显示为圆点 -->
          <!-- show-password: 显示眼睛图标，可切换显示/隐藏密码 -->
          <el-input v-model="formData.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>
        <el-form-item label="真实姓名" prop="real_name">
          <el-input v-model="formData.real_name" placeholder="请输入真实姓名" />
        </el-form-item>
        <el-form-item label="部门" prop="department_id">
          <!-- 树形选择器：选择用户所属部门 -->
          <!-- check-strictly: 可以选择任意层级，不受父子节点限制 -->
          <el-tree-select
            v-model="formData.department_id"
            :data="departmentTree"
            :props="treeProps"
            placeholder="请选择部门"
            clearable
            check-strictly
            node-key="id"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="formData.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <!-- 开关组件：切换用户的启用/禁用状态 -->
          <el-switch v-model="formData.status" />
        </el-form-item>
      </el-form>
      
      <!-- 对话框底部按钮 -->
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
    
    <!-- 分配角色对话框 -->
    <el-dialog v-model="roleDialogVisible" title="分配角色" width="500px">
      <!-- 复选框组：选择用户拥有的角色 -->
      <el-checkbox-group v-model="selectedRoles">
        <el-checkbox v-for="role in allRoles" :key="role.id" :label="role.id">
          {{ role.name }}
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <el-button @click="roleDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveRoles">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi, departmentApi } from '@/api/user'
import type { User, Role, Department } from '@/types'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const roleDialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<User[]>([])
const allRoles = ref<Role[]>([])
const departmentTree = ref<Department[]>([])
const selectedRoles = ref<number[]>([])
const currentUserId = ref<number>()
const formRef = ref()
const deptTreeRef = ref()

const queryForm = reactive({
  keyword: '',
  department_id: undefined as number | undefined
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const formData = reactive({
  id: undefined as number | undefined,
  username: '',
  password: '',
  real_name: '',
  email: '',
  phone: '',
  department_id: undefined as number | undefined,
  status: true
})

const formRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

const treeProps = {
  label: 'name',
  children: 'children'
}

async function loadData() {
  loading.value = true
  try {
    const res = await userApi.getUsers({
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      department_id: queryForm.department_id,
      keyword: queryForm.keyword || undefined
    })
    tableData.value = res
    pagination.total = res.length
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function loadRoles() {
  try {
    allRoles.value = await userApi.getRoles()
  } catch (error) {
    console.error(error)
  }
}

async function loadDepartmentTree() {
  try {
    const tree = await departmentApi.getDepartmentTree()
    departmentTree.value = tree
  } catch (error) {
    console.error(error)
  }
}

async function handleRefreshDepartments() {
  await loadDepartmentTree()
  ElMessage.success('部门列表已刷新')
}

function handleNodeClick(data: Department) {
  queryForm.department_id = data.id
  pagination.page = 1
  loadData()
}

function handleQuery() {
  pagination.page = 1
  loadData()
}

function handleReset() {
  queryForm.keyword = ''
  queryForm.department_id = undefined
  deptTreeRef.value?.setCurrentKey(null)
  handleQuery()
}

function handleAdd() {
  dialogTitle.value = '新增用户'
  Object.assign(formData, {
    id: undefined,
    username: '',
    password: '',
    real_name: '',
    email: '',
    phone: '',
    department_id: undefined,
    status: true
  })
  dialogVisible.value = true
}

function handleEdit(row: User) {
  dialogTitle.value = '编辑用户'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: User) {
  ElMessageBox.confirm('确定要删除该用户吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await userApi.deleteUser(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error(error)
    }
  })
}

function handleAssignRoles(row: User) {
  currentUserId.value = row.id
  selectedRoles.value = []
  roleDialogVisible.value = true
}

async function handleSaveRoles() {
  try {
    await userApi.assignRoles(currentUserId.value!, { role_ids: selectedRoles.value })
    ElMessage.success('角色分配成功')
    roleDialogVisible.value = false
  } catch (error) {
    console.error(error)
  }
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (formData.id) {
          await userApi.updateUser(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await userApi.createUser(formData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadData()
        await loadDepartmentTree()
      } catch (error) {
        console.error(error)
      } finally {
        submitLoading.value = false
      }
    }
  })
}

function handleDialogClose() {
  formRef.value?.resetFields()
}

onMounted(() => {
  loadData()
  loadRoles()
  loadDepartmentTree()
})
</script>

<style scoped>
.users-page {
  height: 100%;
  padding: 20px;
}

.users-layout {
  display: flex;
  gap: 20px;
  height: 100%;
}

.department-tree {
  width: 280px;
  flex-shrink: 0;
}

.users-content {
  flex: 1;
  min-width: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-tree) {
  background: transparent;
}

:deep(.el-tree-node__content:hover) {
  background-color: #f5f7fa;
}

:deep(.el-tree-node.is-current > .el-tree-node__content) {
  background-color: #ecf5ff;
}

:deep(.el-pagination) {
  display: flex;
}
</style>
