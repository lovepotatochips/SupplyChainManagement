<template>
  <div class="accounts-page">
    <el-card>
      <el-form :inline="true">
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增账户</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" stripe v-loading="loading">
        <el-table-column prop="code" label="账户编码" width="150" />
        <el-table-column prop="name" label="账户名称" />
        <el-table-column prop="type" label="账户类型" width="120">
          <template #default="{ row }">
            {{ getTypeLabel(row.type) }}
          </template>
        </el-table-column>
        <el-table-column prop="bank_name" label="开户银行" />
        <el-table-column prop="account_number" label="银行账号" />
        <el-table-column prop="balance" label="余额" align="right" width="120">
          <template #default="{ row }">
            <span :style="{ color: row.balance >= 0 ? 'green' : 'red' }">
              ¥{{ row.balance.toFixed(2) }}
            </span>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 1 ? 'success' : 'danger'">
              {{ row.status === 1 ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="600px">
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="账户名称" prop="name">
              <el-input v-model="formData.name" placeholder="请输入账户名称" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="账户编码" prop="code">
              <el-input v-model="formData.code" placeholder="请输入编码" :disabled="!!formData.id" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="账户类型" prop="type">
          <el-select v-model="formData.type" placeholder="请选择类型">
            <el-option label="银行账户" value="bank" />
            <el-option label="现金账户" value="cash" />
            <el-option label="在线支付" value="online" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="开户银行" prop="bank_name">
          <el-input v-model="formData.bank_name" placeholder="请输入开户银行" />
        </el-form-item>
        
        <el-form-item label="银行账号" prop="account_number">
          <el-input v-model="formData.account_number" placeholder="请输入银行账号" />
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-switch v-model="formData.status" :active-value="1" :inactive-value="0" />
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
const dialogTitle = ref('')
const tableData = ref<any[]>([])
const formRef = ref()

const formData = reactive({
  id: undefined as number | undefined,
  name: '',
  code: '',
  type: 'bank',
  bank_name: '',
  account_number: '',
  status:1,
  remark: ''
})

const formRules = {
  name: [{ required: true, message: '请输入账户名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入账户编码', trigger: 'blur' }]
}

function getTypeLabel(type: string) {
  const map: Record<string, string> = {
    bank: '银行账户',
    cash: '现金账户',
    online: '在线支付'
  }
  return map[type] || type
}

async function loadData() {
  loading.value = true
  try {
    tableData.value = await financeApi.getAccounts()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  dialogTitle.value = '新增账户'
  Object.assign(formData, {
    id: undefined,
    name: '',
    code: '',
    type: 'bank',
    bank_name: '',
    account_number: '',
    status:1,
    remark: ''
  })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑账户'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该账户吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await financeApi.updateAccount(row.id, { status: 0 })
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
          await financeApi.updateAccount(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await financeApi.createAccount(formData)
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

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.accounts-page {
  height: 100%;
}
</style>
