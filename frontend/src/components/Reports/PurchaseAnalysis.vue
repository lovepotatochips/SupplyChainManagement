<template>
  <div class="purchase-analysis">
    <el-form :inline="true">
      <el-form-item label="日期范围">
        <el-date-picker
          v-model="dateRange"
          type="daterange"
          range-separator="-"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          @change="handleDateChange"
        />
      </el-form-item>
    </el-form>
    
    <el-row :gutter="20" style="margin-top: 20px">
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
    
    <el-card style="margin-top: 20px" v-loading="loading">
      <template #header>采购趋势</template>
      <div ref="chartRef" style="height: 400px"></div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, onUnmounted } from 'vue'
import * as echarts from 'echarts'
import { reportApi } from '@/api/business'
import dayjs from 'dayjs'

const chartRef = ref<HTMLElement>()
const endDateValue = dayjs().format('YYYY-MM-DD')
const startDateValue = dayjs().subtract(1, 'month').format('YYYY-MM-DD')
const dateRange = ref<[string, string]>([startDateValue, endDateValue])
const startDate = ref<string>(startDateValue)
const endDate = ref<string>(endDateValue)
let chartInstance: echarts.ECharts | null = null
let dataCache: any[] = []
const loading = ref(false)

const stats = ref([
  { label: '采购总额', value: '¥0', icon: 'Money', color: '#409eff' },
  { label: '采购单数', value: '0', icon: 'List', color: '#67c23a' },
  { label: '平均单价', value: '¥0', icon: 'TrendCharts', color: '#e6a23c' },
  { label: '供应商数', value: '0', icon: 'Shop', color: '#f56c6c' }
])

function handleDateChange() {
  if (dateRange.value) {
    startDate.value = dateRange.value[0]
    endDate.value = dateRange.value[1]
  }
  loadData()
}

async function loadData() {
  loading.value = true
  try {
    const params: { start_date?: string; end_date?: string } = {}
    if (startDate.value) {
      params.start_date = startDate.value
    }
    if (endDate.value) {
      params.end_date = endDate.value
    }
    
    const res = await reportApi.getPurchaseSummary(params)
    
    const data = res.data || []
    dataCache = data
    
    const totalAmount = data.reduce((sum: number, d: any) => sum + (d.total_amount || 0), 0)
    const totalCount = data.reduce((sum: number, d: any) => sum + (d.count || 0), 0)
    const avgAmount = totalCount > 0 ? totalAmount / totalCount : 0
    
    stats.value[0].value = formatCurrency(totalAmount)
    stats.value[1].value = totalCount.toString()
    stats.value[2].value = formatCurrency(avgAmount)
    stats.value[3].value = new Set(data.map((d: any) => d.supplier_id)).size.toString()
    
    setTimeout(() => {
      renderChart()
    }, 100)
  } catch (error) {
    console.error(error)
  } finally {
    setTimeout(() => {
      loading.value = false
    }, 100)
  }
}

function renderChart() {
  if (!chartRef.value) {
    setTimeout(renderChart, 100)
    return
  }
  
  if (chartInstance) {
    chartInstance.dispose()
  }
  
  chartInstance = echarts.init(chartRef.value)
  
  if (dataCache.length === 0) {
    chartInstance.setOption({
      title: {
        text: '暂无采购数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#909399', fontSize: 14 }
      }
    })
    return
  }
  
  chartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['采购金额', '采购单数'] },
    xAxis: {
      type: 'category',
      data: dataCache.map((d: any) => d.date),
      axisLabel: { rotate: 30 }
    },
    yAxis: [
      { type: 'value', name: '金额(元)' },
      { type: 'value', name: '单数', position: 'right' }
    ],
    series: [
      {
        name: '采购金额',
        type: 'bar',
        data: dataCache.map((d: any) => d.total_amount),
        itemStyle: { color: '#409eff' }
      },
      {
        name: '采购单数',
        type: 'line',
        yAxisIndex: 1,
        data: dataCache.map((d: any) => d.count),
        itemStyle: { color: '#67c23a' }
      }
    ]
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
.purchase-analysis {
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
