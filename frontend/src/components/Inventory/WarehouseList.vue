<template>
  <el-card>
    <!-- 操作栏：提供新增仓库按钮 -->
    <el-form :inline="true">
      <el-form-item>
        <el-button type="primary" @click="handleAdd">新增仓库</el-button>
      </el-form-item>
    </el-form>
    
    <!-- 仓库表格：展示仓库数据列表 -->
    <el-table :data="tableData" stripe v-loading="loading">
      <el-table-column prop="code" label="仓库编码" width="120" />
      <el-table-column prop="name" label="仓库名称" />
      <el-table-column prop="type" label="类型" width="100">
        <template #default="{ row }">
          {{ getTypeLabel(row.type) }}
        </template>
      </el-table-column>
      <el-table-column prop="address" label="地址" />
      <el-table-column prop="manager" label="负责人" width="100" />
      <el-table-column prop="phone" label="联系电话" width="130" />
      <el-table-column prop="capacity" label="容量" align="right" width="100" />
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
  
  <!-- 新增/编辑仓库对话框 -->
  <el-dialog
    v-model="dialogVisible"
    :title="dialogTitle"
    width="600px"
    @close="handleDialogClose"
  >
    <!-- 仓库表单：输入或编辑仓库信息 -->
    <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="仓库编码" prop="code">
            <el-input v-model="formData.code" placeholder="请输入编码" :disabled="!!formData.id" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="仓库名称" prop="name">
            <el-input v-model="formData.name" placeholder="请输入名称" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="仓库类型" prop="type">
        <el-select v-model="formData.type" placeholder="请选择类型">
          <el-option label="普通仓库" value="normal" />
          <el-option label="原料仓库" value="raw" />
          <el-option label="成品仓库" value="finished" />
          <el-option label="退货仓库" value="return" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="地址" prop="address">
        <el-input v-model="formData.address" placeholder="请输入地址" />
      </el-form-item>
      
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="负责人" prop="manager">
            <el-input v-model="formData.manager" placeholder="请输入负责人" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="formData.phone" placeholder="请输入联系电话" />
          </el-form-item>
        </el-col>
      </el-row>
      
      <el-form-item label="容量" prop="capacity">
        <el-input-number v-model="formData.capacity" :min="0" :precision="2" style="width: 100%" />
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
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { warehouseApi } from '@/api/business'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<any[]>([])
const formRef = ref()

const formData = reactive({
  id: undefined as number | undefined,
  code: '',
  name: '',
  type: 'normal',
  address: '',
  manager: '',
  phone: '',
  capacity: 0,
  status: 1,
  remark: ''
})

const formRules = {
  code: [{ required: true, message: '请输入仓库编码', trigger: 'blur' }],
  name: [{ required: true, message: '请输入仓库名称', trigger: 'blur' }]
}

function getTypeLabel(type: string) {
  const map: Record<string, string> = {
    normal: '普通仓库',
    raw: '原料仓库',
    finished: '成品仓库',
    return: '退货仓库'
  }
  return map[type] || type
}

async function loadData() {
  loading.value = true
  try {
    tableData.value = await warehouseApi.getWarehouses()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

function handleAdd() {
  dialogTitle.value = '新增仓库'
  Object.assign(formData, {
    id: undefined,
    code: '',
    name: '',
    type: 'normal',
    address: '',
    manager: '',
    phone: '',
    capacity: 0,
    status: 1,
    remark: ''
  })
  dialogVisible.value = true
}

function handleEdit(row: any) {
  dialogTitle.value = '编辑仓库'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: any) {
  ElMessageBox.confirm('确定要删除该仓库吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await warehouseApi.deleteWarehouse(row.id)
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
          await warehouseApi.updateWarehouse(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await warehouseApi.createWarehouse(formData)
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
