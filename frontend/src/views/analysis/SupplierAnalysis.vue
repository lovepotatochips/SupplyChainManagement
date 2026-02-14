<template>
  <div class="supplier-analysis">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>供应商分析</span>
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
          <div ref="purchaseChartRef" style="height: 400px"></div>
        </el-col>
        <el-col :span="12">
          <div ref="qualityChartRef" style="height: 400px"></div>
        </el-col>
      </el-row>
      
      <el-row :gutter="20" style="margin-top: 30px">
        <el-col :span="24">
          <el-table :data="topSuppliers" stripe>
            <el-table-column prop="name" label="供应商名称" />
            <el-table-column prop="orderCount" label="订单数" align="right" />
            <el-table-column prop="totalAmount" label="采购总额" align="right">
              <template #default="{ row }">
                {{ formatCurrency(row.totalAmount) }}
              </template>
            </el-table-column>
            <el-table-column prop="onTimeRate" label="准时交货率" align="right">
              <template #default="{ row }">
                {{ (row.onTimeRate * 100).toFixed(2) }}%
              </template>
            </el-table-column>
            <el-table-column prop="qualityRate" label="质量合格率" align="right">
              <template #default="{ row }">
                {{ (row.qualityRate * 100).toFixed(2) }}%
              </template>
            </el-table-column>
          </el-table>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import * as echarts from 'echarts'

const purchaseChartRef = ref<HTMLElement>()
const qualityChartRef = ref<HTMLElement>()

let purchaseChart: any = null
let qualityChart: any = null

const stats = ref([
  { label: '供应商总数', value: 0 },
  { label: '本月订单数', value: 0 },
  { label: '本月采购额', value: 0 },
  { label: '平均准时交货率', value: '0%' }
])

const topSuppliers = ref<any[]>([])

function formatCurrency(value: number) {
  return new Intl.NumberFormat('zh-CN', { style: 'currency', currency: 'CNY' }).format(value)
}

function initPurchaseChart() {
  if (!purchaseChartRef.value) return
  purchaseChart = echarts.init(purchaseChartRef.value)
}

function initQualityChart() {
  if (!qualityChartRef.value) return
  qualityChart = echarts.init(qualityChartRef.value)
}

function updateCharts() {
  if (purchaseChart && topSuppliers.value.length > 0) {
    purchaseChart.setOption({
      title: { text: '供应商采购额TOP10' },
      tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
      grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
      xAxis: { 
        type: 'category', 
        data: topSuppliers.value.map(s => s.name.length > 8 ? s.name.substring(0, 8) + '...' : s.name),
        axisLabel: { rotate: 30 }
      },
      yAxis: { type: 'value', name: '金额(元)' },
      series: [{ 
        type: 'bar', 
        data: topSuppliers.value.map(s => s.totalAmount),
        itemStyle: { color: '#409eff' },
        label: { show: true, position: 'top', formatter: (params: any) => formatCurrency(params.value) }
      }]
    })
  }
  
  if (qualityChart && topSuppliers.value.length > 0) {
    const pieData = topSuppliers.value.slice(0, 6).map((s, index) => ({
      value: s.qualityRate * 100,
      name: s.name.length > 6 ? s.name.substring(0, 6) + '...' : s.name,
      itemStyle: { 
        color: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272'][index % 6]
      }
    }))
    
    qualityChart.setOption({
      title: { text: '供应商质量合格率', top: '5%' },
      tooltip: { 
        trigger: 'item',
        formatter: '{b}<br/>合格率: {c}%<br/>占比: {d}%'
      },
      legend: { 
        orient: 'horizontal', 
        top: 'bottom',
        type: 'scroll'
      },
      series: [{
        name: '合格率',
        type: 'pie',
        radius: ['40%', '65%'],
        center: ['50%', '50%'],
        avoidLabelOverlap: true,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold',
            formatter: '{b}\n{c}%'
          }
        },
        labelLine: {
          show: false
        },
        data: pieData
      }]
    })
  }
}

async function loadData() {
  stats.value = [
    { label: '供应商总数', value: 15 },
    { label: '本月订单数', value: 42 },
    { label: '本月采购额', value: '¥2,580,000' },
    { label: '平均准时交货率', value: '96.5%' }
  ]
  
  topSuppliers.value = [
    { name: '宝山钢铁股份有限公司', orderCount: 12, totalAmount: 856000, onTimeRate: 0.98, qualityRate: 0.99 },
    { name: '河钢集团有限公司', orderCount: 8, totalAmount: 645000, onTimeRate: 0.95, qualityRate: 0.97 },
    { name: '玖龙纸业(控股)有限公司', orderCount: 10, totalAmount: 423000, onTimeRate: 0.96, qualityRate: 0.98 },
    { name: '丰田汽车(中国)投资有限公司', orderCount: 6, totalAmount: 380000, onTimeRate: 0.99, qualityRate: 1.0 },
    { name: '中粮集团有限公司', orderCount: 6, totalAmount: 276000, onTimeRate: 0.94, qualityRate: 0.96 },
    { name: '山东晨鸣纸业集团股份有限公司', orderCount: 5, totalAmount: 238000, onTimeRate: 0.93, qualityRate: 0.95 },
    { name: '太阳纸业股份有限公司', orderCount: 4, totalAmount: 195000, onTimeRate: 0.96, qualityRate: 0.97 },
    { name: '华泰纸业股份有限公司', orderCount: 3, totalAmount: 168000, onTimeRate: 0.92, qualityRate: 0.94 },
    { name: '首钢集团有限公司', orderCount: 4, totalAmount: 142000, onTimeRate: 0.97, qualityRate: 0.98 },
    { name: '鞍钢集团有限公司', orderCount: 3, totalAmount: 125000, onTimeRate: 0.95, qualityRate: 0.96 }
  ]
  
  await nextTick()
  updateCharts()
}

onMounted(() => {
  initPurchaseChart()
  initQualityChart()
  loadData()
  
  window.addEventListener('resize', () => {
    purchaseChart?.resize()
    qualityChart?.resize()
  })
})
</script>

<style scoped>
.supplier-analysis {
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
