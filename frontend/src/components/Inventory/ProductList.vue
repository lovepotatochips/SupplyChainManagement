<template>
  <el-card>
    <!-- 查询表单：提供产品搜索和新增功能 -->
    <el-form :inline="true" :model="queryForm">
      <el-form-item label="关键词">
        <!-- v-model: 双向绑定搜索关键词 -->
        <!-- clearable: 显示清除按钮，可快速清空输入 -->
        <el-input v-model="queryForm.keyword" placeholder="请输入名称或编码" clearable />
      </el-form-item>
      <el-form-item>
        <!-- 查询按钮：触发搜索，将页码重置为第一页 -->
        <el-button type="primary" @click="handleQuery">查询</el-button>
        <!-- 重置按钮：清空搜索条件，重新加载全部数据 -->
        <el-button @click="handleReset">重置</el-button>
        <!-- 新增产品按钮：打开新增产品对话框 -->
        <el-button type="primary" @click="handleAdd">新增产品</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 产品表格：展示产品数据列表 -->
    <!-- stripe: 斑马纹样式，隔行变色提升可读性 -->
    <!-- v-loading: 数据加载时显示加载动画 -->
    <el-table :data="tableData" stripe v-loading="loading">
      <!-- 表格列定义：展示产品的各项信息 -->
      <el-table-column prop="code" label="产品编码" width="120" />
      <el-table-column prop="name" label="产品名称" />
      <el-table-column prop="specification" label="规格" />
      <el-table-column prop="unit" label="单位" width="80" />
      <el-table-column prop="purchase_price" label="采购价" align="right" width="100" />
      <el-table-column prop="sale_price" label="销售价" align="right" width="100" />
      <!-- 当前库存列：当库存低于最小库存时，用红色显示 -->
      <el-table-column prop="current_stock" label="当前库存" align="right" width="100">
        <template #default="{ row }">
          <span :style="{ color: row.current_stock < row.min_stock ? 'red' : '' }">
            {{ row.current_stock }}
          </span>
        </template>
      </el-table-column>
      <el-table-column prop="min_stock" label="最小库存" align="right" width="100" />
      <el-table-column prop="max_stock" label="最大库存" align="right" width="100" />
      <!-- 状态列：用不同颜色的标签显示启用/禁用状态 -->
      <el-table-column label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
            {{ row.status === 'active' ? '启用' : '禁用' }}
          </el-tag>
        </template>
      </el-table-column>
      <!-- 操作列：提供编辑、删除等操作按钮 -->
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    
    <!-- 分页组件：控制表格数据的分页显示 -->
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
  
  <!-- 新增/编辑产品对话框 -->
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="600px"
    @close="handleDialogClose"
  >
    <!-- 产品表单：输入或编辑产品信息 -->
    <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="产品编码" prop="code">
            <!-- 新增时可输入，编辑时禁用，避免修改产品编码 -->
            <el-input v-model="formData.code" placeholder="请输入编码" :disabled="!!formData.id" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="产品名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入名称" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="规格型号" prop="specification">
        <el-input v-model="formData.specification" placeholder="请输入规格型号" />
      </el-form-item>
      
      <el-form-item label="单位" prop="unit">
        <el-input v-model="formData.unit" placeholder="请输入单位" />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="采购价" prop="purchase_price">
            <!-- 数字输入组件：限制最小值为0，保留2位小数 -->
            <el-input-number v-model="formData.purchase_price" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="销售价" prop="sale_price">
            <el-input-number v-model="formData.sale_price" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="最小库存" prop="min_stock">
            <el-input-number v-model="formData.min_stock" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="最大库存" prop="max_stock">
            <el-input-number v-model="formData.max_stock" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="当前库存" prop="current_stock">
            <el-input-number v-model="formData.current_stock" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="状态" prop="status">
        <!-- 开关组件：切换产品的启用/禁用状态 -->
        <el-switch v-model="formData.status" active-value="active" inactive-value="inactive" />
      </el-form-item>
      
      <el-form-item label="备注" prop="remark">
        <!-- 多行文本输入：用于输入较长的备注信息 -->
        <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
      </el-form-item>
    </el-form>
    
    <!-- 对话框底部按钮 -->
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { productApi } from '@/api/business'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<any[]>([])
const formRef = ref()

const queryForm = reactive({
  keyword: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const formData = reactive({
  id: undefined as number | undefined,
  code: '',
  name: '',
  specification: '',
  unit: '',
  purchase_price: 0,
  sale_price: 0,
  min_stock: 0,
  max_stock: 0,
  current_stock: 0,
  status: 'active',
  remark: ''
})

const formRules = {
  code: [{ required: true, message: '请输入产品编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入产品名称', trigger: 'blur' }]
}

async function loadData() {
  loading.value = true
  try {
    const res = await productApi.getProducts({
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      keyword: queryForm.keyword || undefined
    })
    tableData.value = res.items
    pagination.total = res.total
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

function handleQuery() {
  pagination.page = 1
  loadData()
}

function handleReset() {
  queryForm.keyword = ''
  handleQuery()
}

function handleAdd() {
  dialogTitle.value = '新增产品'
  Object.assign(formData, {
    id: undefined,
    code: '',
    name: '',
    specification: '',
    unit: '',
    purchase_price: 0,
    sale_price: 0,
    min_stock: 0,
    max_stock: 0,
    current_stock: 0,
    status: 'active',
    remark: ''
  })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑产品'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该产品吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await productApi.deleteProduct(row.id)
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
          await productApi.updateProduct(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await productApi.createProduct(formData)
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
:deep(.el-pagination) {
  display: flex;
}
</style>
