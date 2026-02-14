<template>
  <div class="sales-page">
    <el-tabs v-model="activeTab" class="tabs">
      <el-tab-pane label="客户管理" name="customers">
        <CustomerList />
      </el-tab-pane>
      <el-tab-pane label="销售订单" name="orders">
        <SalesOrderList />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import CustomerList from '@/components/Sales/CustomerList.vue'
import SalesOrderList from '@/components/Sales/SalesOrderList.vue'

const activeTab = ref('customers')
</script>

<style scoped>
.sales-page {
  height: 100%;
}

.tabs {
  height: 100%;
}

:deep(.el-tabs__content) {
  height: calc(100% - 55px);
}

:deep(.el-tab-pane) {
  height: 100%;
}
</style>
