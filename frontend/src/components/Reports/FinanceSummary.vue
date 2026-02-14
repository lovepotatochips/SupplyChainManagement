<template>
  <div class="finance-summary">
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
              <div class="stat-value">{{ formatCurrency(stat.value) }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>收支趋势</template>
          <div ref="chartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>账款概览</template>
          <div ref="pieChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>近期付款记录</template>
          <el-table :data="recentPayments" stripe>
            <el-table-column prop="code" label="付款单号" width="180" />
            <el-table-column prop="type" label="类型" width="100">
              <template #default="{ row }">
                <el-tag :type="row.type === 'receive' ? 'success' : 'danger'">
                  {{ row.type === 'receive' ? '收款' : '付款' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="amount" label="金额" align="right">
              <template #default="{ row }">
                ¥{{ row.amount.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="payment_date" label="日期" width="180">
              <template #default="{ row }">
                {{ formatDate(row.payment_date) }}
              </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">{{ getStatusText(row.status) }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/business'
import request from '@/utils/request'

const chartRef = ref<HTMLElement>()
const pieChartRef = ref<HTMLElement>()
let chartInstance: echarts.ECharts | null = null
let pieChartInstance: echarts.ECharts | null = null
const recentPayments = ref<any[]>([])

const stats = ref([
  { label: '总收入', value: 0, icon: 'Money', color: '#67c23a' },
  { label: '总支出', value: 0, icon: 'Wallet', color: '#f56c6c' },
  { label: '净收入', value: 0, icon: 'TrendCharts', color: '#409eff' },
  { label: '应收账款', value: 0, icon: 'Warning', color: '#e6a23c' }
])

function formatCurrency(value: number) {
  if (value >= 100000000) {
    return `¥${(value / 100000000).toFixed(2)}亿`
  } else if (value >= 10000) {
    return `¥${(value / 10000).toFixed(2)}万`
  }
  return `¥${value.toFixed(2)}`
}

function formatDate(date: string) {
  if (!date) return ''
  return new Date(date).toLocaleDateString('zh-CN')
}

function getStatusType(status: string) {
  const map: Record<string, string> = {
    completed: 'success',
    pending: 'warning',
    approved: 'primary',
    cancelled: 'danger'
  }
  return map[status] || 'info'
}

function getStatusText(status: string) {
  const map: Record<string, string> = {
    completed: '已完成',
    pending: '待处理',
    approved: '已审批',
    cancelled: '已取消'
  }
  return map[status] || status
}

async function loadData() {
  try {
    const res = await reportApi.getFinancialSummary()
    stats.value[0].value = res.total_in || 0
    stats.value[1].value = res.total_out || 0
    stats.value[2].value = res.net || 0
    stats.value[3].value = res.total_receivable || 0

    await nextTick()
    initLineChart()
    initPieChart(res)
  } catch (error) {
    console.error(error)
  }
}

function initLineChart() {
  if (!chartRef.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['收入', '支出'] },
    xAxis: {
      type: 'category',
      data: ['1月', '2月', '3月', '4月', '5月', '6月']
    },
    yAxis: { type: 'value' },
    series: [
      {
        name: '收入',
        type: 'line',
        smooth: true,
        data: generateRandomData(6, 1000000, 5000000),
        itemStyle: { color: '#67c23a' },
        areaStyle: { opacity: 0.3 }
      },
      {
        name: '支出',
        type: 'line',
        smooth: true,
        data: generateRandomData(6, 800000, 4000000),
        itemStyle: { color: '#f56c6c' },
        areaStyle: { opacity: 0.3 }
      }
    ]
  })
}

function initPieChart(res: any) {
  if (!pieChartRef.value) return
  
  if (pieChartInstance) {
    pieChartInstance.dispose()
  }
  
  pieChartInstance = echarts.init(pieChartRef.value)
  pieChartInstance.setOption({
    tooltip: { trigger: 'item' },
    legend: { orient: 'vertical', left: 'left' },
    series: [{
      name: '账款',
      type: 'pie',
      radius: '50%',
      data: [
        { value: res.total_receivable || 0, name: '应收账款', itemStyle: { color: '#67c23a' } },
        { value: res.total_payable || 0, name: '应付账款', itemStyle: { color: '#f56c6c' } }
      ]
    }]
  })
}

async function loadRecentPayments() {
  try {
    const res = await request.get('/finance/payments/', { params: { limit: 10 } })
    recentPayments.value = res.items || res || []
  } catch (error) {
    console.error(error)
  }
}

function generateRandomData(count: number, min: number, max: number) {
  return Array.from({ length: count }, () => Math.floor(Math.random() * (max - min) + min))
}

onMounted(() => {
  loadData()
  loadRecentPayments()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
  if (pieChartInstance) {
    pieChartInstance.dispose()
  }
})
</script>

<style scoped>
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
  font-size: 20px;
  font-weight: bold;
  color: #303133;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}
</style>
