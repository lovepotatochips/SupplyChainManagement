<template>
  <div class="bills-page">
    <el-card>
      <el-form :inline="true" :model="queryForm">
        <el-form-item label="类型">
          <el-select v-model="queryForm.type" placeholder="请选择" clearable>
            <el-option label="应收账款" value="receivable" />
            <el-option label="应付账款" value="payable" />
          </el-select>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="queryForm.status" placeholder="请选择" clearable>
            <el-option label="未付款" value="unpaid" />
            <el-option label="部分付款" value="partial" />
            <el-option label="已付清" value="paid" />
            <el-option label="逾期" value="overdue" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery">查询</el-button>
          <el-button @click="handleReset">重置</el-button>
          <el-button type="primary" @click="handleAdd">新增账单</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" stripe v-loading="loading">
        <el-table-column prop="code" label="单据号" width="150" />
        <el-table-column prop="type" label="类型" width="120">
          <template #default="{ row }">
            <el-tag :type="row.type === 'receivable' ? 'success' : 'danger'">
              {{ row.type === 'receivable' ? '应收' : '应付' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="amount" label="金额" align="right" width="120">
          <template #default="{ row }">
            ¥{{ row.amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="paid_amount" label="已付金额" align="right" width="120">
          <template #default="{ row }">
            ¥{{ row.paid_amount.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="remaining_amount" label="剩余金额" align="right" width="120">
          <template #default="{ row }">
            <span :style="{ color: row.remaining_amount > 0 ? 'red' : 'green' }">
              ¥{{ row.remaining_amount.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="due_date" label="到期日期" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">{{ getStatusLabel(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
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
    
    <el-dialog v-model="dialogVisible" title="新增账单" width="600px">
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="类型" prop="type">
          <el-radio-group v-model="formData.type">
            <el-radio value="receivable">应收账款</el-radio>
            <el-radio value="payable">应付账款</el-radio>
          </el-radio-group>
        </el-form-item>
        
        <el-form-item label="金额" prop="amount">
          <el-input-number v-model="formData.amount" :min="0" :precision="2" style="width: 100%" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="账单日期" prop="bill_date">
              <el-date-picker v-model="formData.bill_date" type="date" placeholder="选择日期" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="到期日期" prop="due_date">
              <el-date-picker v-model="formData.due_date" type="date" placeholder="选择日期" style="width: 100%" />
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
  code: '',
  type: 'receivable',
  amount: 0,
  bill_date: undefined as Date | undefined,
  due_date: undefined as Date | undefined,
  reference_code: '',
  remark: ''
})

const formRules = {
  type: [{ required: true, message: '请选择类型', trigger: 'blur' }],
  amount: [{ required: true, message: '请输入金额', trigger: 'blur' }]
}

function getStatusType(status: string) {
  const map: Record<string, any> = {
    unpaid: 'danger',
    partial: 'warning',
    paid: 'success',
    overdue: 'danger'
  }
  return map[status] || 'info'
}

function getStatusLabel(status: string) {
  const map: Record<string, string> = {
    unpaid: '未付款',
    partial: '部分付款',
    paid: '已付清',
    overdue: '逾期'
  }
  return map[status] || status
}

async function loadData() {
  loading.value = true
  try {
    const res = await financeApi.getBills({
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
  pagination.page =1
  loadData()
}

function handleReset() {
  queryForm.type = ''
  queryForm.status = ''
  handleQuery()
}

function handleAdd() {
  Object.assign(formData, {
    code: '',
    type: 'receivable',
    amount: 0,
    bill_date: undefined,
    due_date: undefined,
    reference_code: '',
    remark: ''
  })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该账单吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await financeApi.updateBill(row.id, { status: 'paid' })
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
        await financeApi.createBill(formData)
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
.bills-page {
  height: 100%;
}

:deep(.el-pagination) {
  display: flex;
}
</style>
