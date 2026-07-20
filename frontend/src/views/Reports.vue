<template>
  <div class="reports">
    <el-card class="filter-card">
      <div class="filter-row">
        <el-radio-group v-model="reportType" @change="onTypeChange">
          <el-radio-button value="daily">日报</el-radio-button>
          <el-radio-button value="monthly">月报</el-radio-button>
          <el-radio-button value="quarterly">季报</el-radio-button>
          <el-radio-button value="yearly">年报</el-radio-button>
        </el-radio-group>

        <el-date-picker
          v-if="reportType === 'daily'"
          v-model="dailyDate"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          @change="loadReport"
        />

        <div v-if="reportType === 'monthly'" class="month-picker">
          <el-date-picker
            v-model="monthlyDate"
            type="month"
            placeholder="选择月份"
            format="YYYY-MM"
            value-format="YYYY-MM"
            @change="loadReport"
          />
        </div>

        <div v-if="reportType === 'quarterly'" class="quarter-picker">
          <el-date-picker
            v-model="quarterlyYear"
            type="year"
            placeholder="选择年份"
            format="YYYY"
            value-format="YYYY"
          />
          <el-select v-model="quarterlyQuarter" placeholder="季度" @change="loadReport">
            <el-option :value="1" label="Q1 (1-3月)" />
            <el-option :value="2" label="Q2 (4-6月)" />
            <el-option :value="3" label="Q3 (7-9月)" />
            <el-option :value="4" label="Q4 (10-12月)" />
          </el-select>
        </div>

        <div v-if="reportType === 'yearly'" class="year-picker">
          <el-date-picker
            v-model="yearlyYear"
            type="year"
            placeholder="选择年份"
            format="YYYY"
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

    <!-- 日报 -->
    <template v-if="reportType === 'daily' && dailyData">
      <div class="summary-cards">
        <el-card class="summary-card">
          <div class="card-value">¥{{ dailyData.summary.total_amount.toFixed(2) }}</div>
          <div class="card-label">总业绩</div>
        </el-card>
        <el-card class="summary-card store">
          <div class="card-value">¥{{ dailyData.summary.store_amount.toFixed(2) }}</div>
          <div class="card-label">到店购买</div>
          <div class="card-sub">占比 {{ dailyData.summary.store_ratio.toFixed(1) }}%</div>
        </el-card>
        <el-card class="summary-card salesperson">
          <div class="card-value">¥{{ dailyData.summary.salesperson_amount.toFixed(2) }}</div>
          <div class="card-label">业务员推销</div>
        </el-card>
        <el-card class="summary-card">
          <div class="card-value">{{ dailyData.summary.total_count }}</div>
          <div class="card-label">笔数</div>
          <div class="card-sub">笔均 ¥{{ dailyData.summary.avg_amount.toFixed(2) }}</div>
        </el-card>
      </div>

      <el-card>
        <template #header>
          <span class="card-title">销售明细</span>
        </template>
        <el-table :data="dailyData.details" stripe>
          <el-table-column label="渠道" width="100">
            <template #default="{ row }">
              <el-tag :type="row.channel === 'store' ? 'success' : 'warning'" size="small">
                {{ row.channel === 'store' ? '到店' : '推销' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="salesperson_name" label="业务员" width="120">
            <template #default="{ row }">
              {{ row.salesperson_name || '-' }}
            </template>
          </el-table-column>
          <el-table-column label="金额" width="120">
            <template #default="{ row }">
              <span class="amount">¥{{ row.amount.toFixed(2) }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="note" label="备注" show-overflow-tooltip />
          <el-table-column prop="created_at" label="时间" width="160" />
          <el-table-column label="操作" width="80">
            <template #default="{ row }">
              <el-button type="danger" size="small" circle @click="deleteRecord(row.id)">
                <el-icon><Delete /></el-icon>
              </el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>

    <!-- 月报 -->
    <template v-if="reportType === 'monthly' && monthlyData">
      <div class="summary-cards">
        <el-card class="summary-card">
          <div class="card-value">¥{{ monthlyData.summary.total_amount.toFixed(2) }}</div>
          <div class="card-label">总业绩</div>
        </el-card>
        <el-card class="summary-card store">
          <div class="card-value">¥{{ monthlyData.summary.store_amount.toFixed(2) }}</div>
          <div class="card-label">到店购买</div>
        </el-card>
        <el-card class="summary-card salesperson">
          <div class="card-value">¥{{ monthlyData.summary.salesperson_amount.toFixed(2) }}</div>
          <div class="card-label">业务员推销</div>
        </el-card>
        <el-card class="summary-card">
          <div class="card-value">{{ monthlyData.summary.total_count }}</div>
          <div class="card-label">总笔数</div>
        </el-card>
      </div>

      <div class="detail-section">
        <el-card>
          <template #header>
            <span class="card-title">每日业绩</span>
          </template>
          <el-table :data="monthlyData.daily_data" stripe>
            <el-table-column prop="date" label="日期" width="120" />
            <el-table-column label="到店金额" width="120">
              <template #default="{ row }">¥{{ row.store_amount.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column label="推销金额" width="120">
              <template #default="{ row }">¥{{ row.salesperson_amount.toFixed(2) }}</template>
            </el-table-column>
            <el-table-column label="当日合计">
              <template #default="{ row }">
                <span class="amount">¥{{ row.daily_amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
          </el-table>
        </el-card>

        <el-card v-if="monthlyData.salesperson_data.length > 0">
          <template #header>
            <span class="card-title">业务员业绩</span>
          </template>
          <el-table :data="monthlyData.salesperson_data" stripe>
            <el-table-column prop="salesperson_name" label="业务员" width="120" />
            <el-table-column label="业绩">
              <template #default="{ row }">
                <span class="amount">¥{{ row.total_amount.toFixed(2) }}</span>
              </template>
            </el-table-column>
            <el-table-column prop="count" label="笔数" width="80" />
          </el-table>
        </el-card>
      </div>
    </template>

    <!-- 季报 -->
    <template v-if="reportType === 'quarterly' && quarterlyData">
      <div class="summary-cards">
        <el-card class="summary-card">
          <div class="card-value">¥{{ quarterlyData.summary.total_amount.toFixed(2) }}</div>
          <div class="card-label">总业绩</div>
        </el-card>
        <el-card class="summary-card store">
          <div class="card-value">¥{{ quarterlyData.summary.store_amount.toFixed(2) }}</div>
          <div class="card-label">到店购买</div>
        </el-card>
        <el-card class="summary-card salesperson">
          <div class="card-value">¥{{ quarterlyData.summary.salesperson_amount.toFixed(2) }}</div>
          <div class="card-label">业务员推销</div>
        </el-card>
        <el-card class="summary-card">
          <div class="card-value">{{ quarterlyData.summary.total_count }}</div>
          <div class="card-label">总笔数</div>
        </el-card>
      </div>

      <el-card>
        <template #header>
          <span class="card-title">每月业绩</span>
        </template>
        <el-table :data="quarterlyData.monthly_data" stripe>
          <el-table-column prop="month" label="月份" width="100">
            <template #default="{ row }">{{ row.month }}月</template>
          </el-table-column>
          <el-table-column label="到店金额" width="120">
            <template #default="{ row }">¥{{ row.store_amount.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="推销金额" width="120">
            <template #default="{ row }">¥{{ row.salesperson_amount.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="月合计">
            <template #default="{ row }">
              <span class="amount">¥{{ row.monthly_amount.toFixed(2) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>

    <!-- 年报 -->
    <template v-if="reportType === 'yearly' && yearlyData">
      <div class="summary-cards">
        <el-card class="summary-card">
          <div class="card-value">¥{{ yearlyData.summary.total_amount.toFixed(2) }}</div>
          <div class="card-label">总业绩</div>
        </el-card>
        <el-card class="summary-card store">
          <div class="card-value">¥{{ yearlyData.summary.store_amount.toFixed(2) }}</div>
          <div class="card-label">到店购买</div>
        </el-card>
        <el-card class="summary-card salesperson">
          <div class="card-value">¥{{ yearlyData.summary.salesperson_amount.toFixed(2) }}</div>
          <div class="card-label">业务员推销</div>
        </el-card>
        <el-card class="summary-card">
          <div class="card-value">{{ yearlyData.summary.total_count }}</div>
          <div class="card-label">总笔数</div>
        </el-card>
      </div>

      <el-card>
        <template #header>
          <span class="card-title">每月业绩</span>
        </template>
        <el-table :data="yearlyData.monthly_data" stripe>
          <el-table-column prop="month" label="月份" width="100">
            <template #default="{ row }">{{ row.month }}月</template>
          </el-table-column>
          <el-table-column label="到店金额" width="120">
            <template #default="{ row }">¥{{ row.store_amount.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="推销金额" width="120">
            <template #default="{ row }">¥{{ row.salesperson_amount.toFixed(2) }}</template>
          </el-table-column>
          <el-table-column label="月合计">
            <template #default="{ row }">
              <span class="amount">¥{{ row.monthly_amount.toFixed(2) }}</span>
            </template>
          </el-table-column>
        </el-table>
      </el-card>
    </template>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { reportsApi, salesApi } from '../api'

const reportType = ref('daily')
const dailyDate = ref(new Date().toISOString().split('T')[0])
const monthlyDate = ref(new Date().toISOString().slice(0, 7))
const quarterlyYear = ref(new Date().getFullYear().toString())
const quarterlyQuarter = ref(Math.ceil((new Date().getMonth() + 1) / 3))
const yearlyYear = ref(new Date().getFullYear().toString())

const dailyData = ref(null)
const monthlyData = ref(null)
const quarterlyData = ref(null)
const yearlyData = ref(null)

const onTypeChange = () => {
  loadReport()
}

const loadReport = async () => {
  try {
    if (reportType.value === 'daily') {
      const res = await reportsApi.getDaily(dailyDate.value)
      dailyData.value = res.data
    } else if (reportType.value === 'monthly') {
      const [year, month] = monthlyDate.value.split('-')
      const res = await reportsApi.getMonthly(parseInt(year), parseInt(month))
      monthlyData.value = res.data
    } else if (reportType.value === 'quarterly') {
      const res = await reportsApi.getQuarterly(parseInt(quarterlyYear.value), quarterlyQuarter.value)
      quarterlyData.value = res.data
    } else if (reportType.value === 'yearly') {
      const res = await reportsApi.getYearly(parseInt(yearlyYear.value))
      yearlyData.value = res.data
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
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
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
    } else if (reportType.value === 'quarterly') {
      year = quarterlyYear.value
    } else {
      year = yearlyYear.value
    }

    const res = await reportsApi.exportExcel(parseInt(year), month)
    const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `业绩报表_${year}${month ? month + '月' : '全年'}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)
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
.quarter-picker,
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

.summary-card .card-sub {
  color: #c0c4cc;
  font-size: 12px;
  margin-top: 2px;
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

.detail-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
</style>
