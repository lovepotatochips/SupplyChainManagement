<template>
  <div class="inventory-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>库存分析</span>
          <el-button type="primary" @click="loadData">刷新</el-button>
        </div>
      </template>
      
      <el-row :gutter="20">
        <el-col :span="6" v-for="(stat, index) in stats" :key="index">
          <div class="stat-item">
            <div class="stat-value">{{ stat.value }}</div>
            <div class="stat-label">{{ stat.label }}</div>
          </div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="12">
          <div ref="trendChartRef" style="height: 400px"></div>
        </el-col>
        <el-col :span="12">
          <div ref="turnoverChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="lowStockProducts" stripe>
            <el-table-column prop="code" label="产品编码" />
            <el-table-column prop="name" label="产品名称" />
            <el-table-column prop="category" label="分类" />
            <el-table-column prop="currentStock" label="当前库存" align="right" />
            <el-table-column prop="minStock" label="最小库存" align="right" />
            <el-table-column label="状态" align="center">
              <template #default="{ row }">
                <el-tag type="danger">库存不足</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const trendChartRef = ref<HTMLElement>()
const turnoverChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '产品总数', value: 0 },
  { label: '库存总值', value: 0 },
  { label: '低库存产品', value: 0 },
  { label: '平均周转天数', value: '0天' }
])

const lowStockProducts = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    title: { text: '库存变化趋势' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ name: '库存价值', type: 'line', data: [820, 932, 901, 934, 1290, 1330] }]
  })
}

function initTurnoverChart() {
  if (!turnoverChartRef.value) return
  const chart = echarts.init(turnoverChartRef.value)
  chart.setOption({
    title: { text: '库存周转率' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['钢铁', '纸业', '汽车', '农产品'] },
    yAxis: { type: 'value' },
    series: [{ name: '周转率', type: 'bar', data: [12, 18, 8, 15] }]
  })
}

async function loadData() {
  stats.value = [
    { label: '产品总数', value: 156 },
    { label: '库存总值', value: '¥12,580,000' },
    { label: '低库存产品', value: 8 },
    { label: '平均周转天数', value: '25天' }
  ]
  
  lowStockProducts.value = [
    { code: 'P001', name: '冷轧钢板', category: '钢铁', currentStock: 15, minStock: 50 },
    { code: 'P002', name: '热轧钢板', category: '钢铁', currentStock: 25, minStock: 80 },
    { code: 'P003', name: '双胶纸', category: '纸业', currentStock: 30, minStock: 100 },
    { code: 'P004', name: '铜版纸', category: '纸业', currentStock: 45, minStock: 120 },
    { code: 'P005', name: '汽车配件A', category: '汽车', currentStock: 8, minStock: 30 }
  ]
}

onMounted(() => {
  initTrendChart()
  initTurnoverChart()
  loadData()
})
</script>

<style scoped>
.inventory-analysis {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}
</style>
