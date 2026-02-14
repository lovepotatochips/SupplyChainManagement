<template>
  <div class="reports-page">
    <el-card>
      <el-tabs v-model="activeTab" class="tabs">
        <el-tab-pane label="财务汇总" name="finance">
          <FinanceSummary />
        </el-tab-pane>
        <el-tab-pane label="采购分析" name="purchase">
          <PurchaseAnalysis />
        </el-tab-pane>
        <el-tab-pane label="销售分析" name="sales">
          <SalesAnalysis />
        </el-tab-pane>
        <el-tab-pane label="库存状态" name="inventory">
          <InventoryStatus />
        </el-tab-pane>
        <el-tab-pane label="供应商分析" name="supplier">
          <SupplierAnalysis />
        </el-tab-pane>
        <el-tab-pane label="客户分析" name="customer">
          <CustomerAnalysis />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import FinanceSummary from '@/components/Reports/FinanceSummary.vue'
import PurchaseAnalysis from '@/components/Reports/PurchaseAnalysis.vue'
import SalesAnalysis from '@/components/Reports/SalesAnalysis.vue'
import InventoryStatus from '@/components/Reports/InventoryStatus.vue'
import SupplierAnalysis from '@/components/Reports/SupplierAnalysis.vue'
import CustomerAnalysis from '@/components/Reports/CustomerAnalysis.vue'

const activeTab = ref('finance')
</script>

<style scoped>
.reports-page {
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
