<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6" v-for="(stat, index) in stats" :key="index">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon" :style="{ background: stat.color }">
              <el-icon :size="24" color="#fff">
                <component :is="stat.icon" />
              </el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>采购趋势</span>
          </template>
          <div ref="purchaseChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>销售趋势</span>
          </template>
          <div ref="salesChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>库存预警</span>
          </template>
          <el-table :data="lowStockProducts" stripe>
            <el-table-column prop="code" label="产品编码" />
            <el-table-column prop="name" label="产品名称" />
            <el-table-column prop="current_stock" label="当前库存" align="right" />
            <el-table-column prop="min_stock" label="最小库存" align="right" />
            <el-table-column label="状态" align="center">
              <template #default="{ row }">
                <el-tag type="danger">库存不足</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/business'

const purchaseChartRef = ref<HTMLElement>()
const salesChartRef = ref<HTMLElement>()
const lowStockProducts = ref<any[]>([])

const stats = ref([
  { label: '产品总数', value: 0, icon: 'Goods', color: '#409eff' },
  { label: '供应商数', value: 0, icon: 'Shop', color: '#67c23a' },
  { label: '客户数', value: 0, icon: 'User', color: '#e6a23c' },
  { label: '待处理订单', value: 0, icon: 'List', color: '#f56c6c' }
])

async function loadDashboardData() {
  try {
    const [dashboard, inventory, purchase, sales] = await Promise.all([
      reportApi.getDashboardStats(),
      reportApi.getInventoryStatus(),
      reportApi.getPurchaseSummary(),
      reportApi.getSalesSummary()
    ])
    
    stats.value[0].value = dashboard.products.total
    stats.value[1].value = dashboard.partners.suppliers
    stats.value[2].value = dashboard.partners.customers
    stats.value[3].value = dashboard.orders.pending_purchase + dashboard.orders.pending_sales
    
    lowStockProducts.value = inventory.low_stock_products || []
    
    if (purchaseChartRef.value && purchase && purchase.data && purchase.data.length > 0) {
      const chart = echarts.init(purchaseChartRef.value)
      chart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: purchase.data.map((d: any) => d.date) },
        yAxis: { type: 'value' },
        series: [{
          data: purchase.data.map((d: any) => d.total_amount),
          type: 'line',
          smooth: true,
          areaStyle: { opacity: 0.3 }
        }]
      })
    }
    
    if (salesChartRef.value && sales && sales.data && sales.data.length > 0) {
      const chart = echarts.init(salesChartRef.value)
      chart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: sales.data.map((d: any) => d.date) },
        yAxis: { type: 'value' },
        series: [{
          data: sales.data.map((d: any) => d.total_amount),
          type: 'line',
          smooth: true,
          areaStyle: { opacity: 0.3 }
        }]
      })
    }
  } catch (error) {
    console.error('Failed to load dashboard data:', error)
  }
}

onMounted(() => {
  loadDashboardData()
})
</script>

<style scoped>
.dashboard {
  height: 100%;
}

.stat-card {
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-content {
  display: flex;
  align-items: center;
  gap: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
