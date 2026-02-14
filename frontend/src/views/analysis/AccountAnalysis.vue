<template>
  <div class="account-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账户分析</span>
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
          <div ref="balanceChartRef" style="height: 400px"></div>
        </el-col>
        <el-col :span="12">
          <div ref="flowChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="accounts" stripe>
            <el-table-column prop="name" label="账户名称" />
            <el-table-column prop="bank" label="开户银行" />
            <el-table-column prop="accountNo" label="账号" />
            <el-table-column prop="balance" label="余额" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.balance) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="row.status === '正常' ? 'success' : 'danger'">{{ row.status }}</el-tag>
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

const balanceChartRef = ref<HTMLElement>()
const flowChartRef = ref<HTMLElement>()

const stats = ref([
  { label: '账户总数', value: 0 },
  { label: '账户总余额', value: 0 },
  { label: '本月收入', value: 0 },
  { label: '本月支出', value: 0 }
])

const accounts = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function initBalanceChart() {
  if (!balanceChartRef.value) return
  const chart = echarts.init(balanceChartRef.value)
  chart.setOption({
    title: { text: '账户余额分布' },
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      data: [
        { value: 3350, name: '基本户' },
        { value: 3100, name: '一般户' },
        { value: 2340, name: '专用户' }
      ]
    }]
  })
}

function initFlowChart() {
  if (!flowChartRef.value) return
  const chart = echarts.init(flowChartRef.value)
  chart.setOption({
    title: { text: '资金流向' },
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出'] },
    xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
    yAxis: { type: 'value' },
    series: [
      { name: '收入', type: 'bar', data: [1820, 1932, 1901, 1934, 2290, 2330] },
      { name: '支出', type: 'bar', data: [1520, 1632, 1701, 1734, 1990, 2030] }
    ]
  })
}

async function loadData() {
  stats.value = [
    { label: '账户总数', value: 8 },
    { label: '账户总余额', value: '¥8,790,000' },
    { label: '本月收入', value: '¥2,330,000' },
    { label: '本月支出', value: '¥2,030,000' }
  ]
  
  accounts.value = [
    { name: '基本户', bank: '中国工商银行厦门分行', accountNo: '4100XXXXXXXXXX0001', balance: 3350000, status: '正常' },
    { name: '一般户1', bank: '中国银行厦门分行', accountNo: '4126XXXXXXXXXX0002', balance: 2100000, status: '正常' },
    { name: '一般户2', bank: '中国建设银行厦门分行', accountNo: '3510XXXXXXXXXX0003', balance: 1540000, status: '正常' },
    { name: '专用户', bank: '中国农业银行厦门分行', accountNo: '1343XXXXXXXXXX0004', balance: 1800000, status: '正常' }
  ]
}

onMounted(() => {
  initBalanceChart()
  initFlowChart()
  loadData()
})
</script>

<style scoped>
.account-analysis {
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
