<template>
  <div class="sales-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>销售分析</span>
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
          <div ref="customerChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="topCustomers" stripe>
            <el-table-column prop="name" label="客户名称" />
            <el-table-column prop="orderCount" label="订单数" align="right" />
            <el-table-column prop="totalAmount" label="销售总额" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.totalAmount) }}
              </template>
            </el-table-column>
            <el-table-column prop="growth" label="同比增长" align="right">
              <template #default="{ row }">
                <span :style="{ color: row.growth >= 0 ? '#67c23a' : '#f56c6c' }">
                  {{ row.growth >= 0 ? '+' : '' }}{{ row.growth }}%
                </span>
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
const customerChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '本月订单数', value: 0 },
  { label: '本月销售额', value: 0 },
  { label: '待发货订单', value: 0 },
  { label: '销售增长率', value: '0%' }
])

const topCustomers = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    title: { text: '销售趋势' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ name: '销售额', type: 'line', data: [820, 932, 901, 934, 1290, 1330] }]
  })
}

function initCustomerChart() {
  if (!customerChartRef.value) return
  const chart = echarts.init(customerChartRef.value)
  chart.setOption({
    title: { text: '客户贡献占比' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      data: [
        { value: 1048, name: 'VIP客户' },
        { value: 735, name: '批发客户' },
        { value: 580, name: '普通客户' }
      ]
    }]
  })
}

async function loadData() {
  stats.value = [
    { label: '本月订单数', value: 56 },
    { label: '本月销售额', value: '¥3,850,000' },
    { label: '待发货订单', value: 12 },
    { label: '销售增长率', value: '+12.5%' }
  ]
  
  topCustomers.value = [
    { name: '福建三钢(集团)有限责任公司', orderCount: 15, totalAmount: 856000, growth: 15.2 },
    { name: '福建省汽车工业集团有限公司', orderCount: 12, totalAmount: 723000, growth: 8.5 },
    { name: '宁德时代新能源科技股份有限公司', orderCount: 10, totalAmount: 680000, growth: 22.3 },
    { name: '紫金矿业集团股份有限公司', orderCount: 8, totalAmount: 540000, growth: -3.2 },
    { name: '金龙汽车集团股份有限公司', orderCount: 11, totalAmount: 510000, growth: 6.8 }
  ]
}

onMounted(() => {
  initTrendChart()
  initCustomerChart()
  loadData()
})
</script>

<style scoped>
.sales-analysis {
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
