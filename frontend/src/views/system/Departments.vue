<template>
  <div class="departments-page">
    <el-card>
      <!-- 操作按钮区域 -->
      <el-form :inline="true">
        <el-form-item>
          <!-- 新增部门按钮：点击打开新增部门对话框 -->
          <el-button type="primary" @click="handleAdd">新增部门</el-button>
        </el-form-item>
      </el-form>
      
      <!-- 部门表格：以树形结构展示部门列表 -->
      <!-- stripe: 斑马纹样式，隔行变色提升可读性 -->
      <!-- v-loading: 数据加载时显示加载动画 -->
      <!-- row-key: 行数据的唯一标识字段，用于树形展开/折叠 -->
      <!-- :tree-props: 配置树形结构的子节点字段 -->
      <!-- default-expand-all: 默认展开所有树节点 -->
      <el-table :data="tableData" stripe v-loading="loading" row-key="id" :tree-props="{ children: 'children' }" default-expand-all>
        <!-- 表格列定义：展示部门的各项信息 -->
        <el-table-column prop="name" label="部门名称" width="200" />
        <el-table-column prop="code" label="部门编码" />
        <el-table-column prop="leader" label="负责人" />
        <el-table-column prop="phone" label="联系电话" />
        <el-table-column prop="address" label="地址" />
        <!-- 状态列：用不同颜色的标签显示启用/禁用状态 -->
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <!-- 操作列：提供添加子部门、编辑、删除等操作按钮 -->
        <!-- fixed="right": 固定在表格右侧，滚动时可见 -->
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <!-- 添加子部门：在当前部门下创建子部门 -->
            <el-button link type="primary" @click="handleAddChild(row)">添加子部门</el-button>
            <!-- 编辑：修改当前部门信息 -->
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <!-- 删除：删除当前部门 -->
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 新增/编辑部门对话框 -->
    <!-- v-model: 控制对话框的显示/隐藏 -->
    <!-- :title: 对话框标题，根据操作动态变化 -->
    <!-- @close: 对话框关闭时触发，重置表单 -->
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <!-- 部门表单：输入或编辑部门信息 -->
      <!-- :model: 表单数据对象 -->
      <!-- :rules: 表单验证规则 -->
      <!-- ref: 表单引用，用于调用验证和重置方法 -->
      <!-- label-width: 标签宽度，保持对齐美观 -->
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="部门名称" prop="name">
          <!-- v-model: 双向绑定部门名称 -->
          <el-input v-model="formData.name" placeholder="请输入部门名称" />
        </el-form-item>
        <el-form-item label="部门编码" prop="code">
          <!-- 新增时可输入，编辑时禁用，避免修改部门编码 -->
          <el-input v-model="formData.code" placeholder="请输入部门编码" :disabled="!!formData.id" />
        </el-form-item>
        <el-form-item label="上级部门" prop="parent_id">
          <!-- 级联选择器：选择部门的上级部门，支持多级选择 -->
          <!-- :options: 级联数据源，部门树结构 -->
          <!-- :props: 级联选择器配置 -->
          <!-- checkStrictly: 可以选择任意层级，不强制选择最深层 -->
          <!-- clearable: 显示清除按钮，可快速清空选择 -->
          <el-cascader
            v-model="parentPath"
            :options="deptTreeOptions"
            :props="{ value: 'id', label: 'name', children: 'children', checkStrictly: true }"
            clearable
            placeholder="请选择上级部门"
            @change="handleParentChange"
          />
        </el-form-item>
        <el-form-item label="负责人" prop="leader">
          <el-input v-model="formData.leader" placeholder="请输入负责人" />
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="formData.phone" placeholder="请输入联系电话" />
        </el-form-item>
        <el-form-item label="地址" prop="address">
          <el-input v-model="formData.address" placeholder="请输入地址" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <!-- 多行文本输入：用于输入较长的描述信息 -->
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <!-- 开关组件：切换部门的启用/禁用状态 -->
          <!-- :active-value: 启用状态的值（数字1） -->
          <!-- :inactive-value: 禁用状态的值（数字0） -->
          <el-switch v-model="formData.status" :active-value="1" :inactive-value="0" />
        </el-form-item>
      </el-form>
      
      <!-- 对话框底部按钮 -->
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { departmentApi } from '@/api/user'
import type { Department } from '@/types'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<Department[]>([])
const deptTreeOptions = ref<Department[]>([])
const parentPath = ref<number[]>([])
const formRef = ref()

const formData = reactive({
  id: undefined as number | undefined,
  name: '',
  code: '',
  parent_id: undefined as number | undefined,
  leader: '',
  phone: '',
  address: '',
  description: '',
  status: 1
})

const formRules = {
  name: [{ required: true, message: '请输入部门名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入部门编码', trigger: 'blur' }]
}

function flattenTree(tree: Department[]): Department[] {
  const result: Department[] = []
  function traverse(nodes: Department[]) {
    nodes.forEach(node => {
      result.push(node)
      if (node.children && node.children.length > 0) {
        traverse(node.children)
      }
    })
  }
  traverse(tree)
  return result
}

function buildTree(list: Department[], parentId: number | null = null): Department[] {
  return list
    .filter(item => item.parent_id === parentId)
    .map(item => ({
      ...item,
      children: buildTree(list, item.id)
    }))
}

async function loadData() {
  loading.value = true
  try {
    const tree = await departmentApi.getDepartmentTree()
    tableData.value = tree
    deptTreeOptions.value = [{ id: 0, name: '无', code: 'ROOT', parent_id: null, sort_order: 0, status: 1, created_at: '', updated_at: '', children: [] }, ...tree]
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  dialogTitle.value = '新增部门'
  Object.assign(formData, {
    id: undefined,
    name: '',
    code: '',
    parent_id: undefined,
    leader: '',
    phone: '',
    address: '',
    description: '',
    status: 1
  })
  parentPath.value = []
  dialogVisible.value = true
}

function handleAddChild(row: Department) {
  handleAdd()
  formData.parent_id = row.id
  parentPath.value = [row.id]
  dialogTitle.value = '添加子部门'
}

function handleEdit(row: Department) {
  dialogTitle.value = '编辑部门'
  Object.assign(formData, row)
  parentPath.value = row.parent_id ? [row.parent_id] : []
  dialogVisible.value = true
}

function handleParentChange(value: number[]) {
  formData.parent_id = value.length > 0 ? value[value.length - 1] : undefined
}

function handleDelete(row: Department) {
  if (row.children && row.children.length > 0) {
    ElMessage.warning('该部门下有子部门，无法删除')
    return
  }
  ElMessageBox.confirm('确定要删除该部门吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await departmentApi.deleteDepartment(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error(error)
    }
  })
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        if (formData.id) {
          await departmentApi.updateDepartment(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await departmentApi.createDepartment(formData)
          ElMessage.success('创建成功')
        }
        dialogVisible.value = false
        loadData()
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
})
</script>

<style scoped>
.departments-page {
  height: 100%;
}
</style>
