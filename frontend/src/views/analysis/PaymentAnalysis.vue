<template>
  <div class="payment-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>付款分析</span>
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
          <div ref="typeChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="recentPayments" stripe>
            <el-table-column prop="code" label="付款编号" />
            <el-table-column prop="supplier" label="供应商" />
            <el-table-column prop="amount" label="金额" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.amount) }}
              </template>
            </el-table-column>
            <el-table-column prop="paymentMethod" label="付款方式" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="date" label="付款日期" />
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
const typeChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '本月付款笔数', value: 0 },
  { label: '本月付款总额', value: 0 },
  { label: '待审批付款', value: 0 },
  { label: '平均付款周期', value: '0天' }
])

const recentPayments = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function getStatusType(status: string) {
  const map: Record<string, string> = {
    '已完成': 'success',
    '待审批': 'warning',
    '已拒绝': 'danger'
  }
  return map[status] || 'info'
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    title: { text: '付款趋势' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [{ name: '付款额', type: 'line', data: [520, 632, 701, 734, 890, 930] }]
  })
}

function initTypeChart() {
  if (!typeChartRef.value) return
  const chart = echarts.init(typeChartRef.value)
  chart.setOption({
    title: { text: '付款方式占比' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      data: [
        { value: 735, name: '银行转账' },
        { value: 310, name: '支票' },
        { value: 234, name: '现金' }
      ]
    }]
  })
}

async function loadData() {
  stats.value = [
    { label: '本月付款笔数', value: 28 },
    { label: '本月付款总额', value: '¥1,850,000' },
    { label: '待审批付款', value: 6 },
    { label: '平均付款周期', value: '15天' }
  ]
  
  recentPayments.value = [
    { code: 'PAY20260214001', supplier: '宝山钢铁股份有限公司', amount: 120000, paymentMethod: '银行转账', status: '已完成', date: '2026-02-14' },
    { code: 'PAY20260214002', supplier: '玖龙纸业(控股)有限公司', amount: 65000, paymentMethod: '银行转账', status: '待审批', date: '2026-02-14' },
    { code: 'PAY20260213001', supplier: '河钢集团有限公司', amount: 85000, paymentMethod: '支票', status: '已完成', date: '2026-02-13' },
    { code: 'PAY20260213002', supplier: '中粮集团有限公司', amount: 45000, paymentMethod: '银行转账', status: '已完成', date: '2026-02-13' },
    { code: 'PAY20260212001', supplier: '丰田汽车(中国)投资有限公司', amount: 95000, paymentMethod: '银行转账', status: '已完成', date: '2026-02-12' }
  ]
}

onMounted(() => {
  initTrendChart()
  initTypeChart()
  loadData()
})
</script>

<style scoped>
.payment-analysis {
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
