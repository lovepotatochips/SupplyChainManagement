<template>
  <el-card>
    <!-- 查询表单：按类型筛选库存记录 -->
    <el-form :inline="true" :model="queryForm">
      <el-form-item label="类型">
        <el-select v-model="queryForm.type" placeholder="请选择" clearable>
          <el-option label="入库" value="in" />
          <el-option label="出库" value="out" />
          <el-option label="调拨" value="transfer" />
          <el-option label="盘点" value="check" />
          <el-option label="调整" value="adjust" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleQuery">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleAdd">新增记录</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 库存记录表格：展示库存变动历史 -->
    <el-table :data="tableData" stripe v-loading="loading">
      <el-table-column prop="code" label="单据号" width="150" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }">
          {{ getTypeLabel(row.type) }}
        </template>
      </el-table-column>
      <el-table-column prop="warehouse_id" label="仓库ID" width="100" />
      <el-table-column prop="product_id" label="产品ID" width="100" />
      <el-table-column prop="quantity" label="数量" align="right" width="100" />
      <el-table-column prop="unit_price" label="单价" align="right" width="100" />
      <el-table-column prop="amount" label="金额" align="right" width="120">
        <template #default="{ row }">
          ¥{{ row.amount?.toFixed(2) || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="reference_code" label="关联单号" width="150" />
      <el-table-column prop="created_at" label="创建时间" width="180" />
    </el-table>
    
    <!-- 分页组件 -->
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
  
  <!-- 新增库存记录对话框 -->
  <el-dialog
    v-model="dialogVisible"
    title="新增库存记录"
    width="600px"
    @close="handleDialogClose"
  >
    <!-- 库存记录表单：输入库存变动信息 -->
    <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="类型" prop="type">
            <el-select v-model="formData.type" placeholder="请选择类型">
              <el-option label="入库" value="in" />
              <el-option label="出库" value="out" />
              <el-option label="调拨" value="transfer" />
              <el-option label="调整" value="adjust" />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="仓库" prop="warehouse_id">
            <el-input-number v-model="formData.warehouse_id" :min="1" style="width: 100%" placeholder="仓库ID" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="产品" prop="product_id">
            <el-input-number v-model="formData.product_id" :min="1" style="width: 100%" placeholder="产品ID" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="数量" prop="quantity">
            <el-input-number v-model="formData.quantity" :min="0" :precision="2" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="单价" prop="unit_price">
        <el-input-number v-model="formData.unit_price" :min="0" :precision="2" style="width: 100%" />
      </el-form-item>
      
      <el-form-item label="关联单号" prop="reference_code">
        <el-input v-model="formData.reference_code" placeholder="请输入关联单号" />
      </el-form-item>
      
      <el-form-item label="备注" prop="remark">
        <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入备注" />
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="dialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { stockApi } from '@/api/business'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const tableData = ref<any[]>([])
const formRef = ref()

const queryForm = reactive({
  type: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const formData = reactive({
  type: 'in',
  warehouse_id: undefined as number | undefined,
  product_id: undefined as number | undefined,
  quantity: 1,
  unit_price: 0,
  reference_code: '',
  remark: ''
})

const formRules = {
  type: [{ required: true, message: '请选择类型', trigger: 'blur' }],
  warehouse_id: [{ required: true, message: '请输入仓库ID', trigger: 'blur' }],
  product_id: [{ required: true, message: '请输入产品ID', trigger: 'blur' }],
  quantity: [{ required: true, message: '请输入数量', trigger: 'blur' }]
}

function getTypeLabel(type: string) {
  const map: Record<string, string> = {
    in: '入库',
    out: '出库',
    transfer: '调拨',
    check: '盘点',
    adjust: '调整'
  }
  return map[type] || type
}

async function loadData() {
  loading.value = true
  try {
    const res = await stockApi.getStockRecords({
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      type: queryForm.type || undefined
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
  queryForm.type = ''
  handleQuery()
}

function handleAdd() {
  Object.assign(formData, {
    type: 'in',
    warehouse_id: undefined,
    product_id: undefined,
    quantity: 1,
    unit_price: 0,
    reference_code: '',
    remark: ''
  })
  dialogVisible.value = true
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      submitLoading.value = true
      try {
        await stockApi.createStockRecord(formData)
        ElMessage.success('创建成功')
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
