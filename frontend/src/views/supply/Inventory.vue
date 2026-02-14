<template>
  <div class="inventory-page">
    <el-tabs v-model="activeTab" class="tabs">
      <el-tab-pane label="产品管理" name="products">
        <ProductList />
      </el-tab-pane>
      <el-tab-pane label="仓库管理" name="warehouses">
        <WarehouseList />
      </el-tab-pane>
      <el-tab-pane label="库存记录" name="records">
        <StockRecordList />
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import ProductList from '@/components/Inventory/ProductList.vue'
import WarehouseList from '@/components/Inventory/WarehouseList.vue'
import StockRecordList from '@/components/Inventory/StockRecordList.vue'

const activeTab = ref('products')
</script>

<style scoped>
.inventory-page {
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
