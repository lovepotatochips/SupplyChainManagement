<template>
  <div class="payments-page">
    <el-card>
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="类型">
          <el-select v-model="queryForm.type" placeholder="请选择" clearable>
            <el-option label="付款" value="pay" />
            <el-option label="收款" value="receive" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="请选择" clearable>
            <el-option label="待处理" value="pending" />
            <el-option label="已完成" value="completed" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="handleAdd">新增付款</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" stripe v-loading="loading">
        <el-table-column prop="code" label="单据号" width="150" />
        <el-table-column prop="type" label="类型" width="100">
          <template #default="{ row }">
            <el-tag :type="row.type === 'pay' ? 'danger' : 'success'">
              {{ row.type === 'pay' ? '付款' : '收款' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" align="right" width="120">
          <template #default="{ row }">
            <span :style="{ color: row.type === 'pay' ? 'red' : 'green' }">
              {{ row.type === 'pay' ? '-' : '+' }}¥{{ row.amount.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="payment_method" label="付款方式" width="100">
          <template #default="{ row }">
            {{ getMethodLabel(row.payment_method) }}
          </template>
        </el-table-column>
        <el-table-column prop="payment_date" label="付款日期" width="120" />
        <el-table-column prop="reference_code" label="关联单号" width="150" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button v-if="row.approval_status === 'pending'" link type="success" @click="handleApprove(row)">审批</el-button>
            <el-button v-if="row.status === 'pending'" link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
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
    
    <el-dialog v-model="dialogVisible" title="新增付款" width="600px">
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="类型" prop="type">
              <el-radio-group v-model="formData.type">
                <el-radio value="pay">付款</el-radio>
                <el-radio value="receive">收款</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="formData.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="付款方式" prop="payment_method">
              <el-select v-model="formData.payment_method" placeholder="请选择">
                <el-option label="现金" value="cash" />
                <el-option label="转账" value="transfer" />
                <el-option label="支票" value="check" />
                <el-option label="在线支付" value="online" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="付款日期" prop="payment_date">
              <el-date-picker v-model="formData.payment_date" type="date" placeholder="选择日期" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
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
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { financeApi } from '@/api/business'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const tableData = ref<any[]>([])
const formRef = ref()

const queryForm = reactive({
  type: '',
  status: ''
})

const pagination = reactive({
  page:1,
  size: 10,
  total: 0
})

const formData = reactive({
  type: 'pay',
  amount: 0,
  payment_method: 'transfer',
  payment_date: undefined as Date | undefined,
  reference_code: '',
  remark: ''
})

const formRules = {
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }],
  payment_method: [{ required: true, message: '请选择付款方式', trigger: 'blur' }]
}

function getMethodLabel(method: string) {
  const map: Record<string, string> = {
    cash: '现金',
    transfer: '转账',
    check: '支票',
    online: '在线支付'
  }
  return map[method] || method
}

function getStatusType(status: string) {
  const map: Record<string, any> = {
    pending: 'info',
    completed: 'success',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    pending: '待处理',
    completed: '已完成',
    cancelled: '已取消'
  }
  return map[status] || status
}

async function loadData() {
  loading.value = true
  try {
    const res = await financeApi.getPayments({
      skip: (pagination.page - 1) * pagination.size,
      limit: pagination.size,
      type: queryForm.type || undefined,
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
  queryForm.type = ''
  queryForm.status = ''
  handleQuery()
}

function handleAdd() {
  Object.assign(formData, {
    type: 'pay',
    amount: 0,
    payment_method: 'transfer',
    payment_date: undefined,
    reference_code: '',
    remark: ''
  })
  dialogVisible.value = true
}

function handleApprove(row: any) {
  ElMessageBox.confirm('确定要批准该付款吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await financeApi.approvePayment(row.id, { approval_status: 'approved' })
      ElMessage.success('审批成功')
      loadData()
    } catch (error) {
      console.error(error)
    }
  })
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该付款吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await financeApi.updatePayment(row.id, { status: 'cancelled' })
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
        await financeApi.createPayment(formData)
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

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.payments-page {
  height: 100%;
}

:deep(.el-pagination) {
  display: flex;
}
</style>
