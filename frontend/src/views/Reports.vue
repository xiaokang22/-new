<template>
  <div class="reports">
    <el-card class="filter-card">
      <div class="filter-row">
        <el-radio-group v-model="reportType" @change="onTypeChange">
          <el-radio-button value="daily">日报</el-radio-button>
          <el-radio-button value="monthly">月报</el-radio-button>
          <el-radio-button value="yearly">年报</el-radio-button>
        </el-radio-group>

        <el-date-picker
          v-if="reportType === 'daily'"
          v-model="dailyDate"
          type="date"
          placeholder="选择日期"
          format="YYYY年MM月DD日"
          value-format="YYYY-MM-DD"
          @change="loadReport"
        />

        <div v-if="reportType === 'monthly'" class="month-picker">
          <el-date-picker
            v-model="monthlyDate"
            type="month"
            placeholder="选择月份"
            format="YYYY年MM月"
            value-format="YYYY-MM"
            @change="loadReport"
          />
        </div>

        <div v-if="reportType === 'yearly'" class="year-picker">
          <el-date-picker
            v-model="selectYear"
            type="year"
            placeholder="选择年份"
            format="YYYY年"
            value-format="YYYY"
            @change="loadReport"
          />
        </div>

        <el-button type="success" @click="exportExcel">
          <el-icon><Download /></el-icon>
          导出 Excel
        </el-button>
      </div>
    </el-card>

    <!-- 汇总卡片 -->
    <div v-if="summary" class="summary-cards">
      <el-card class="summary-card">
        <div class="card-value">¥{{ summary.total_amount.toFixed(2) }}</div>
        <div class="card-label">总业绩</div>
      </el-card>
      <el-card class="summary-card store">
        <div class="card-value">¥{{ summary.store_amount.toFixed(2) }}</div>
        <div class="card-label">到店购买</div>
      </el-card>
      <el-card class="summary-card salesperson">
        <div class="card-value">¥{{ summary.salesperson_amount.toFixed(2) }}</div>
        <div class="card-label">业务员推销</div>
      </el-card>
      <el-card class="summary-card">
        <div class="card-value">{{ summary.total_count }}</div>
        <div class="card-label">总笔数</div>
      </el-card>
    </div>

    <!-- 月报/年报：业务员业绩表 -->
    <el-card v-if="(reportType === 'monthly' || reportType === 'yearly') && salespersonData.length > 0" class="detail-card" style="margin-bottom: 20px">
      <template #header>
        <span class="card-title">{{ reportType === 'monthly' ? '业务员月度业绩' : '业务员年度业绩' }}</span>
      </template>
      <el-table :data="salespersonData" stripe>
        <el-table-column prop="salesperson_name" label="业务员" width="120" />
        <el-table-column label="业绩">
          <template #default="{ row }">
            <span class="amount">¥{{ row.total_amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="笔数" width="80" />
      </el-table>
    </el-card>

    <!-- 日报：业务员业绩 -->
    <el-card v-if="reportType === 'daily' && salespersonData.length > 0" class="detail-card" style="margin-bottom: 20px">
      <template #header>
        <span class="card-title">业务员业绩</span>
      </template>
      <el-table :data="salespersonData" stripe>
        <el-table-column prop="salesperson_name" label="业务员" width="120" />
        <el-table-column label="业绩">
          <template #default="{ row }">
            <span class="amount">¥{{ row.total_amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="count" label="笔数" width="80" />
      </el-table>
    </el-card>

    <!-- 日报：销售明细列表 -->
    <el-card v-if="reportType === 'daily' && dailyDetails.length > 0" class="detail-card">
      <template #header>
        <span class="card-title">销售明细</span>
      </template>
      <el-table :data="dailyDetails" stripe>
        <el-table-column label="渠道" width="100">
          <template #default="{ row }">
            <el-tag :type="row.channel === 'store' ? 'success' : 'warning'" size="small">
              {{ row.channel === 'store' ? '到店' : '推销' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="salesperson_name" label="业务员" width="120">
          <template #default="{ row }">{{ row.salesperson_name || '-' }}</template>
        </el-table-column>
        <el-table-column label="金额" width="120">
          <template #default="{ row }">
            <span class="amount">¥{{ row.amount.toFixed(2) }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="note" label="备注" />
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button type="danger" size="small" circle @click="deleteRecord(row.id)">
              <el-icon><Delete /></el-icon>
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { reportsApi, salesApi } from '../api'

const reportType = ref('daily')
const dailyDate = ref(new Date().toISOString().split('T')[0])
const monthlyDate = ref(new Date().toISOString().slice(0, 7))
const selectYear = ref(new Date().getFullYear().toString())

const summary = ref(null)
const salespersonData = ref([])
const dailyDetails = ref([])

const onTypeChange = () => {
  loadReport()
}

const loadReport = async () => {
  try {
    summary.value = null
    salespersonData.value = []
    dailyDetails.value = []

    if (reportType.value === 'daily') {
      const res = await reportsApi.getDaily(dailyDate.value)
      summary.value = res.data.summary
      dailyDetails.value = res.data.details
      const spMap = {}
      for (const d of res.data.details) {
        if (d.salesperson_name) {
          if (!spMap[d.salesperson_name]) spMap[d.salesperson_name] = { total_amount: 0, count: 0 }
          spMap[d.salesperson_name].total_amount += d.amount
          spMap[d.salesperson_name].count++
        }
      }
      salespersonData.value = Object.entries(spMap).map(([name, v]) => ({
        salesperson_name: name, ...v
      }))
    } else if (reportType.value === 'monthly') {
      const [year, month] = monthlyDate.value.split('-')
      const res = await reportsApi.getMonthly(parseInt(year), parseInt(month))
      summary.value = res.data.summary
      salespersonData.value = res.data.salesperson_data
    } else if (reportType.value === 'yearly') {
      const year = parseInt(selectYear.value)
      const res = await reportsApi.getYearly(year)
      summary.value = res.data.summary
      salespersonData.value = res.data.salesperson_data
    }
  } catch (e) {
    ElMessage.error('加载报表失败')
  }
}

const deleteRecord = async (id) => {
  try {
    await ElMessageBox.confirm('确定要删除这条记录吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await salesApi.delete(id)
    ElMessage.success('删除成功')
    await loadReport()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const exportExcel = async () => {
  try {
    let year, month
    if (reportType.value === 'daily') {
      year = dailyDate.value.substring(0, 4)
      month = parseInt(dailyDate.value.substring(5, 7))
    } else if (reportType.value === 'monthly') {
      const parts = monthlyDate.value.split('-')
      year = parts[0]
      month = parseInt(parts[1])
    } else {
      year = selectYear.value
    }
    await reportsApi.exportExcel(parseInt(year), month)
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  loadReport()
})
</script>

<style scoped>
.reports {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.month-picker,
.year-picker {
  display: flex;
  gap: 8px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 20px;
}

.summary-card {
  text-align: center;
}

.summary-card .card-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.summary-card .card-label {
  color: #909399;
  font-size: 14px;
}

.summary-card.store .card-value {
  color: #67c23a;
}

.summary-card.salesperson .card-value {
  color: #e6a23c;
}

.card-title {
  font-weight: bold;
  font-size: 16px;
}

.amount {
  font-weight: bold;
  color: #303133;
}
</style>
