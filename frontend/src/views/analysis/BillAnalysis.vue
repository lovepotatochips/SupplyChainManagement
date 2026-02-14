<template>
  <div class="bill-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账单分析</span>
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
          <div ref="statusChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="recentBills" stripe>
            <el-table-column prop="code" label="账单编号" />
            <el-table-column prop="customer" label="客户/供应商" />
            <el-table-column prop="type" label="类型" />
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
            <el-table-column prop="dueDate" label="到期日" />
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
const statusChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '应收账款笔数', value: 0 },
  { label: '应收账款总额', value: 0 },
  { label: '应付账款笔数', value: 0 },
  { label: '应付账款总额', value: 0 }
])

const recentBills = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function getStatusType(status: string) {
  const map: Record<string, string> = {
    '已收款': 'success',
    '待收款': 'warning',
    '逾期': 'danger',
    '已付款': 'success',
    '待付款': 'info'
  }
  return map[status] || 'info'
}

function initTrendChart() {
  if (!trendChartRef.value) return
  const chart = echarts.init(trendChartRef.value)
  chart.setOption({
    title: { text: '账单趋势' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['应收', '应付'] },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [
      { name: '应收', type: 'line', data: [820, 932, 901, 934, 1290, 1330] },
      { name: '应付', type: 'line', data: [520, 632, 701, 734, 890, 930] }
    ]
  })
}

function initStatusChart() {
  if (!statusChartRef.value) return
  const chart = echarts.init(statusChartRef.value)
  chart.setOption({
    title: { text: '账单状态分布' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      data: [
        { value: 735, name: '已收款' },
        { value: 310, name: '待收款' },
        { value: 58, name: '逾期' }
      ]
    }]
  })
}

async function loadData() {
  stats.value = [
    { label: '应收账款笔数', value: 42 },
    { label: '应收账款总额', value: '¥2,580,000' },
    { label: '应付账款笔数', value: 35 },
    { label: '应付账款总额', value: '¥1,850,000' }
  ]
  
  recentBills.value = [
    { code: 'BILL20260214001', customer: '福建三钢(集团)有限责任公司', type: '应收', amount: 120000, status: '待收款', dueDate: '2026-03-14' },
    { code: 'BILL20260214002', customer: '宝山钢铁股份有限公司', type: '应付', amount: 85000, status: '待付款', dueDate: '2026-03-14' },
    { code: 'BILL20260213001', customer: '宁德时代新能源科技股份有限公司', type: '应收', amount: 68000, status: '已收款', dueDate: '2026-02-13' },
    { code: 'BILL20260213002', customer: '河钢集团有限公司', type: '应付', amount: 95000, status: '已付款', dueDate: '2026-02-13' },
    { code: 'BILL20260212001', customer: '福建省汽车工业集团有限公司', type: '应收', amount: 110000, status: '逾期', dueDate: '2026-02-05' }
  ]
}

onMounted(() => {
  initTrendChart()
  initStatusChart()
  loadData()
})
</script>

<style scoped>
.bill-analysis {
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
