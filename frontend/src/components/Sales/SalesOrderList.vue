<template>
  <el-card>
    <!-- 查询表单：按状态筛选销售订单 -->
    <el-form :inline="true" :model="queryForm">
      <el-form-item label="状态">
        <el-select v-model="queryForm.status" placeholder="请选择" clearable>
          <el-option label="待处理" value="pending" />
          <el-option label="已批准" value="approved" />
          <el-option label="已发货" value="shipped" />
          <el-option label="已交付" value="delivered" />
          <el-option label="已完成" value="completed" />
          <el-option label="已取消" value="cancelled" />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="handleQuery">查询</el-button>
        <el-button @click="handleReset">重置</el-button>
        <el-button type="primary" @click="handleAdd">新增销售单</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 销售订单表格：展示订单数据列表 -->
    <el-table :data="tableData" stripe v-loading="loading">
      <el-table-column prop="code" label="销售单号" width="150" />
      <el-table-column prop="customer_id" label="客户ID" width="100" />
      <el-table-column prop="sale_date" label="销售日期" width="120" />
      <el-table-column prop="delivery_date" label="交货日期" width="120" />
      <el-table-column prop="total_amount" label="总金额" align="right" width="120">
        <template #default="{ row }">
          ¥{{ row.total_amount.toFixed(2) }}
        </template>
      </el-table-column>
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="approval_status" label="审批状态" width="100">
        <template #default="{ row }">
          <el-tag :type="getApprovalStatusType(row.approval_status)">
            {{ getApprovalStatusLabel(row.approval_status) }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="handleView(row)">查看</el-button>
          <el-button v-if="row.approval_status === 'pending'" link type="success" @click="handleApprove(row)">审批</el-button>
          <el-button v-if="row.status === 'pending'" link type="primary" @click="handleEdit(row)">编辑</el-button>
          <el-button v-if="row.status === 'pending'" link type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
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
  
  <!-- 新增/编辑销售订单对话框 -->
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="900px"
    @close="handleDialogClose"
  >
    <!-- 销售订单表单：输入或编辑订单信息 -->
    <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="客户" prop="customer_id">
            <el-input-number v-model="formData.customer_id" :min="1" style="width: 100%" placeholder="请输入客户ID" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="销售日期" prop="sale_date">
            <el-date-picker v-model="formData.sale_date" type="date" placeholder="选择日期" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="交货日期" prop="delivery_date">
            <el-date-picker v-model="formData.delivery_date" type="date" placeholder="选择日期" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="销售明细">
        <!-- 订单明细表格：可以添加多个产品 -->
        <el-table :data="formData.items" border style="width: 100%">
          <el-table-column label="产品编码" width="150">
            <template #default="{ row }">
              <el-input v-model="row.product_code" placeholder="编码" />
            </template>
          </el-table-column>
          <el-table-column label="产品名称" width="200">
            <template #default="{ row }">
              <el-input v-model="row.product_name" placeholder="名称" />
            </template>
          </el-table-column>
          <el-table-column label="规格" width="120">
            <template #default="{ row }">
              <el-input v-model="row.specification" placeholder="规格" />
            </template>
          </el-table-column>
          <el-table-column label="单位" width="80">
            <template #default="{ row }">
              <el-input v-model="row.unit" placeholder="单位" />
            </template>
          </el-table-column>
          <el-table-column label="数量" width="120">
            <template #default="{ row }">
              <el-input-number v-model="row.quantity" :min="0" :precision="2" style="width: 100%" />
            </template>
          </el-table-column>
          <el-table-column label="单价" width="120">
            <template #default="{ row }">
              <el-input-number v-model="row.unit_price" :min="0" :precision="2" style="width: 100%" />
            </template>
          </el-table-column>
          <el-table-column label="操作" width="60">
            <template #default="{ $index }">
              <el-button link type="danger" @click="formData.items.splice($index, 1)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
        <el-button @click="addItem" style="margin-top: 10px">添加明细</el-button>
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
  
  <!-- 审批销售订单对话框 -->
  <el-dialog v-model="approveDialogVisible" title="审批销售单" width="500px">
    <el-form :model="approveForm" label-width="100px">
      <el-form-item label="审批结果">
        <el-radio-group v-model="approveForm.approval_status">
          <el-radio value="approved">批准</el-radio>
          <el-radio value="rejected">拒绝</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="审批意见">
        <el-input v-model="approveForm.remark" type="textarea" :rows="3" placeholder="请输入审批意见" />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="approveDialogVisible = false">取消</el-button>
      <el-button type="primary" @click="handleApproveSubmit">确定</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { salesApi } from '@/api/business'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const approveDialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<any[]>([])
const currentOrderId = ref<number>()
const formRef = ref()

const queryForm = reactive({
  status: ''
})

const pagination = reactive({
  page: 1,
  size: 10,
  total: 0
})

const formData = reactive({
  id: undefined as number | undefined,
  customer_id: undefined as number | undefined,
  sale_date: undefined as Date | undefined,
  delivery_date: undefined as Date | undefined,
  remark: '',
  items: [] as any[]
})

const approveForm = reactive({
  approval_status: 'approved',
  remark: ''
})

const formRules = {
  customer_id: [{ required: true, message: '请选择客户', trigger: 'blur' }]
}

function getStatusType(status: string) {
  const map: Record<string, any> = {
    pending: 'info',
    approved: 'warning',
    shipped: 'primary',
    delivered: 'success',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    pending: '待处理',
    approved: '已批准',
    shipped: '已发货',
    delivered: '已交付',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

function getApprovalStatusType(status: string) {
  const map: Record<string, any> = {
    pending: 'info',
    approved: 'success',
    rejected: 'danger'
  }
  return map[status] || 'info'
}

function getApprovalStatusLabel(status: string) {
  const map: Record<string, string> = {
    pending: '待审批',
    approved: '已批准',
    rejected: '已拒绝'
  }
  return map[status] || status
}

async function loadData() {
  loading.value = true
  try {
    const res = await salesApi.getSalesOrders({
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      status: queryForm.status || undefined
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
  queryForm.status = ''
  handleQuery()
}

function handleAdd() {
  dialogTitle.value = '新增销售单'
  Object.assign(formData, {
    id: undefined,
    customer_id: undefined,
    sale_date: undefined,
    delivery_date: undefined,
    remark: '',
    items: []
  })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑销售单'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleView(row: any) {
  ElMessage.info('查看详情功能开发中')
}

function handleApprove(row: any) {
  currentOrderId.value = row.id
  approveForm.approval_status = 'approved'
  approveForm.remark = ''
  approveDialogVisible.value = true
}

async function handleApproveSubmit() {
  try {
    await salesApi.approveSalesOrder(currentOrderId.value!, approveForm)
    ElMessage.success('审批成功')
    approveDialogVisible.value = false
    loadData()
  } catch (error) {
    console.error(error)
  }
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该销售单吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await salesApi.deleteSalesOrder(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error(error)
    }
  })
}

function addItem() {
  formData.items.push({
    product_code: '',
    product_name: '',
    specification: '',
    unit: '',
    quantity: 1,
    unit_price: 0
  })
}

async function handleSubmit() {
  if (!formRef.value) return
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      if (formData.items.length === 0) {
        ElMessage.warning('请添加销售明细')
        return
      }
      submitLoading.value = true
      try {
        if (formData.id) {
          await salesApi.updateSalesOrder(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await salesApi.createSalesOrder(formData)
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
