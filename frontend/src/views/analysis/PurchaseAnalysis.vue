<template>
  <div class="purchase-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>采购分析</span>
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
          <div ref="categoryChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="recentOrders" stripe>
            <el-table-column prop="code" label="订单编号" />
            <el-table-column prop="supplier" label="供应商" />
            <el-table-column prop="amount" label="金额" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.amount) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="订单日期" />
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
const categoryChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '本月订单数', value: 0 },
  { label: '本月采购额', value: 0 },
  { label: '待审批订单', value: 0 },
  { label: '平均采购周期', value: '0天' }
])

const recentOrders = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function getStatusType(status: string) {
  const map: Record<string, string> = {
    '已完成': 'success',
    '进行中': 'warning',
    '待审批': 'info',
    '已拒绝': 'danger'
  }
  return map[status] || 'info'
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    title: { text: '采购趋势' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ name: '采购额', type: 'line', data: [120, 132, 101, 134, 90, 230] }]
  })
}

function initCategoryChart() {
  if (!categoryChartRef.value) return
  const chart = echarts.init(categoryChartRef.value)
  chart.setOption({
    title: { text: '采购分类占比' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      data: [
        { value: 548, name: '钢铁' },
        { value: 735, name: '纸业' },
        { value: 580, name: '汽车' },
        { value: 484, name: '农产品' }
      ]
    }]
  })
}

async function loadData() {
  stats.value = [
    { label: '本月订单数', value: 42 },
    { label: '本月采购额', value: '¥2,580,000' },
    { label: '待审批订单', value: 5 },
    { label: '平均采购周期', value: '7天' }
  ]
  
  recentOrders.value = [
    { code: 'PO20260214001', supplier: '宝山钢铁股份有限公司', amount: 120000, status: '已完成', date: '2026-02-14' },
    { code: 'PO20260214002', supplier: '玖龙纸业(控股)有限公司', amount: 85000, status: '进行中', date: '2026-02-14' },
    { code: 'PO20260213001', supplier: '丰田汽车(中国)投资有限公司', amount: 65000, status: '待审批', date: '2026-02-13' },
    { code: 'PO20260213002', supplier: '中粮集团有限公司', amount: 45000, status: '已完成', date: '2026-02-13' },
    { code: 'PO20260212001', supplier: '河钢集团有限公司', amount: 95000, status: '已完成', date: '2026-02-12' }
  ]
}

onMounted(() => {
  initTrendChart()
  initCategoryChart()
  loadData()
})
</script>

<style scoped>
.purchase-analysis {
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
