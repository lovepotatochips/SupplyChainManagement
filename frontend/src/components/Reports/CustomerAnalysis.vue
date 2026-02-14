<template>
  <div class="customer-analysis">
    <el-row :gutter="20">
      <el-col :span="8" v-for="(stat, index) in stats" :key="index">
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

    <el-card style="margin-top: 20px" v-loading="loading">
      <template #header>客户销售金额分布</template>
      <div ref="chartRef" style="height: 400px"></div>
    </el-card>
    
    <el-card style="margin-top: 20px">
      <template #header>客户排行榜</template>
      <el-table :data="tableData" stripe>
        <el-table-column type="index" label="排名" width="80" />
        <el-table-column prop="name" label="客户名称" />
        <el-table-column prop="code" label="客户编码" width="150" />
        <el-table-column prop="order_count" label="销售单数" align="right" width="120" />
        <el-table-column prop="total_amount" label="销售金额" align="right" width="150">
          <template #default="{ row }">
            ¥{{ formatAmount(row.total_amount) }}
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/business'

const chartRef = ref<HTMLElement>()
const tableData = ref<any[]>([])
let chartInstance: echarts.ECharts | null = null
const loading = ref(false)

const stats = ref([
  { label: '客户总数', value: '0', icon: 'User', color: '#67c23a' },
  { label: '活跃客户', value: '0', icon: 'CircleCheck', color: '#409eff' },
  { label: '销售总额', value: '¥0', icon: 'Money', color: '#e6a23c' }
])

async function loadData() {
  loading.value = true
  try {
    const res = await reportApi.getCustomerAnalysis()
    const data = res.data || []
    tableData.value = data
    
    stats.value[0].value = data.length.toString()
    stats.value[1].value = data.filter((d: any) => d.order_count > 0).length.toString()
    const totalAmount = data.reduce((sum: number, d: any) => sum + (d.total_amount || 0), 0)
    stats.value[2].value = formatCurrency(totalAmount)
    
    setTimeout(() => {
      initChart(data)
    }, 100)
  } catch (error) {
    console.error(error)
  } finally {
    setTimeout(() => {
      loading.value = false
    }, 100)
  }
}

function initChart(data: any[]) {
  if (!chartRef.value) return
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  if (data.length === 0) {
    chartInstance.setOption({
      title: {
        text: '暂无客户数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#909399', fontSize: 14 }
      }
    })
    return
  }
  
  chartInstance.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    xAxis: {
      type: 'category',
      data: data.slice(0, 10).map((d: any) => d.name?.substring(0, 8) || ''),
      axisLabel: { rotate: 30, interval: 0 }
    },
    yAxis: { type: 'value', name: '销售金额(元)' },
    series: [{
      name: '销售金额',
      type: 'bar',
      data: data.slice(0, 10).map((d: any) => d.total_amount),
      itemStyle: { color: '#67c23a' },
      label: { show: true, position: 'top', formatter: (params: any) => formatAmount(params.value) }
    }]
  })
}

function formatCurrency(value: number) {
  if (value >= 100000000) {
    return `¥${(value / 100000000).toFixed(2)}亿`
  } else if (value >= 10000) {
    return `¥${(value / 10000).toFixed(2)}万`
  }
  return `¥${value.toFixed(2)}`
}

function formatAmount(value: number) {
  if (!value) return '0'
  if (value >= 10000) {
    return `${(value / 10000).toFixed(1)}万`
  }
  return value.toFixed(0)
}

onMounted(() => {
  loadData()
})

onUnmounted(() => {
  if (chartInstance) {
    chartInstance.dispose()
  }
})
</script>

<style scoped>
.customer-analysis {
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
  width: 50px;
  height: 50px;
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
