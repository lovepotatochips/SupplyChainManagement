<template>
  <div class="roles-page">
    <el-card>
      <el-form :inline="true">
        <el-form-item>
          <el-button type="primary" @click="handleAdd">新增角色</el-button>
        </el-form-item>
      </el-form>
      
      <el-table :data="tableData" stripe v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="角色名称" />
        <el-table-column prop="code" label="角色编码" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status ? 'success' : 'danger'">
              {{ row.status ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" @click="handleEdit(row)">编辑</el-button>
            <el-button link type="primary" @click="handleAssignPermissions(row)">分配权限</el-button>
            <el-button link type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <el-dialog
      v-model="dialogVisible"
      :title="dialogTitle"
      width="600px"
      @close="handleDialogClose"
    >
      <el-form :model="formData" :rules="formRules" ref="formRef" label-width="100px">
        <el-form-item label="角色名称" prop="name">
          <el-input v-model="formData.name" placeholder="请输入角色名称" />
        </el-form-item>
        <el-form-item label="角色编码" prop="code">
          <el-input v-model="formData.code" placeholder="请输入角色编码" :disabled="!!formData.id" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-switch v-model="formData.status" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </template>
    </el-dialog>
    
    <el-dialog v-model="permDialogVisible" title="分配权限" width="600px">
      <el-checkbox-group v-model="selectedPerms">
        <el-checkbox v-for="perm in allPerms" :key="perm.id" :label="perm.id">
          {{ perm.name }} ({{ perm.code }})
        </el-checkbox>
      </el-checkbox-group>
      <template #footer>
        <el-button @click="permDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSavePerms">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { userApi } from '@/api/user'
import type { Role, Permission } from '@/types'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const permDialogVisible = ref(false)
const dialogTitle = ref('')
const tableData = ref<Role[]>([])
const allPerms = ref<Permission[]>([])
const selectedPerms = ref<number[]>([])
const currentRoleId = ref<number>()
const formRef = ref()

const formData = reactive({
  id: undefined as number | undefined,
  name: '',
  code: '',
  description: '',
  status: true
})

const formRules = {
  name: [{ required: true, message: '请输入角色名称', trigger: 'blur' }],
  code: [{ required: true, message: '请输入角色编码', trigger: 'blur' }]
}

async function loadData() {
  loading.value = true
  try {
    tableData.value = await userApi.getRoles()
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

async function loadPerms() {
  try {
    allPerms.value = await userApi.getPermissions()
  } catch (error) {
    console.error(error)
  }
}

function handleAdd() {
  dialogTitle.value = '新增角色'
  Object.assign(formData, {
    id: undefined,
    name: '',
    code: '',
    description: '',
    status: true
  })
  dialogVisible.value = true
}

function handleEdit(row: Role) {
  dialogTitle.value = '编辑角色'
  Object.assign(formData, row)
  dialogVisible.value = true
}

function handleDelete(row: Role) {
  ElMessageBox.confirm('确定要删除该角色吗？', '提示', { type: 'warning' }).then(async () => {
    try {
      await userApi.deleteRole(row.id)
      ElMessage.success('删除成功')
      loadData()
    } catch (error) {
      console.error(error)
    }
  })
}

function handleAssignPermissions(row: Role) {
  currentRoleId.value = row.id
  selectedPerms.value = []
  permDialogVisible.value = true
}

async function handleSavePerms() {
  try {
    await userApi.assignPermissions(currentRoleId.value!, { permission_ids: selectedPerms.value })
    ElMessage.success('权限分配成功')
    permDialogVisible.value = false
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
          await userApi.updateRole(formData.id, formData)
          ElMessage.success('更新成功')
        } else {
          await userApi.createRole(formData)
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
  loadPerms()
})
</script>

<style scoped>
.roles-page {
  height: 100%;
}
</style>
