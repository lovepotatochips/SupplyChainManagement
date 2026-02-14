<template>
  <div class="inventory-status">
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
              <div class="stat-value">{{ stat.value }}</div>
              <div class="stat-label">{{ stat.label }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card v-loading="loading">
          <template #header>库存分布</template>
          <div ref="pieChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card v-loading="loading">
          <template #header>库存价值TOP10</template>
          <div ref="barChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-card style="margin-top: 20px">
      <template #header>库存预警产品</template>
      <el-table :data="lowStockProducts" stripe>
        <el-table-column prop="code" label="产品编码" width="150" />
        <el-table-column prop="name" label="产品名称" />
        <el-table-column prop="current_stock" label="当前库存" align="right" width="120">
          <template #default="{ row }">
            <span :class="{ 'low-stock': row.current_stock < row.min_stock }">
              {{ row.current_stock }}
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="min_stock" label="最小库存" align="right" width="120" />
        <el-table-column prop="max_stock" label="最大库存" align="right" width="120" />
        <el-table-column label="缺口" align="right" width="120">
          <template #default="{ row }">
            <span class="shortage">{{ row.min_stock - row.current_stock }}</span>
          </template>
        </el-table-column>
        <el-table-column label="状态" align="center" width="100">
          <template #default>
            <el-tag type="danger">库存不足</el-tag>
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
import request from '@/utils/request'

const pieChartRef = ref<HTMLElement>()
const barChartRef = ref<HTMLElement>()
let pieChartInstance: echarts.ECharts | null = null
let barChartInstance: echarts.ECharts | null = null
const loading = ref(false)

const stats = ref([
  { label: '产品总数', value: '0', icon: 'Box', color: '#409eff' },
  { label: '库存正常', value: '0', icon: 'CircleCheck', color: '#67c23a' },
  { label: '库存不足', value: '0', icon: 'Warning', color: '#f56c6c' },
  { label: '库存过剩', value: '0', icon: 'CircleClose', color: '#e6a23c' }
])

const lowStockProducts = ref<any[]>([])

async function loadData() {
  loading.value = true
  try {
    const res = await reportApi.getInventoryStatus()
    stats.value[0].value = res.total || 0
    stats.value[1].value = res.normal || 0
    stats.value[2].value = res.low_stock || 0
    stats.value[3].value = res.overstock || 0
    lowStockProducts.value = res.low_stock_products || []

    setTimeout(() => {
      initPieChart(res)
    }, 100)
    
    const productsRes = await request.get('/inventory/products/', { params: { limit: 10 } })
    const products = productsRes.items || []
    
    setTimeout(() => {
      initBarChart(products)
    }, 100)
  } catch (error) {
    console.error(error)
  } finally {
    setTimeout(() => {
      loading.value = false
    }, 200)
  }
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
      name: '库存状态',
      type: 'pie',
      radius: '50%',
      data: [
        { value: res.normal || 0, name: '正常', itemStyle: { color: '#67c23a' } },
        { value: res.low_stock || 0, name: '不足', itemStyle: { color: '#f56c6c' } },
        { value: res.overstock || 0, name: '过剩', itemStyle: { color: '#e6a23c' } }
      ]
    }]
  })
}

function initBarChart(products: any[]) {
  if (!barChartRef.value) return
  
  if (barChartInstance) {
    barChartInstance.dispose()
  }
  
  barChartInstance = echarts.init(barChartRef.value)
  
  if (products.length === 0) {
    barChartInstance.setOption({
      title: {
        text: '暂无库存数据',
        left: 'center',
        top: 'center',
        textStyle: { color: '#909399', fontSize: 14 }
      }
    })
    return
  }
  
  barChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: products.map((p: any) => p.name?.substring(0, 6) || ''),
      axisLabel: { rotate: 30 }
    },
    yAxis: { type: 'value', name: '库存价值(元)' },
    series: [{
      name: '库存价值',
      type: 'bar',
      data: products.map((p: any) => (p.current_stock || 0) * (p.unit_price || 0)),
      itemStyle: { color: '#409eff' }
    }]
  })
}

onMounted(() => {
  loadData()
})

onUnmounted(() => {
  if (pieChartInstance) {
    pieChartInstance.dispose()
  }
  if (barChartInstance) {
    barChartInstance.dispose()
  }
})
</script>

<style scoped>
.inventory-status {
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

.low-stock {
  color: #f56c6c;
  font-weight: bold;
}

.shortage {
  color: #f56c6c;
  font-weight: bold;
}
</style>
