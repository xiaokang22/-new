<template>
  <div class="member-report">
    <el-card class="search-card">
      <template #header>
        <span class="card-title">🔍 会员业绩汇总</span>
      </template>
      <div class="search-row">
        <el-date-picker
          v-model="selectMonth"
          type="month"
          placeholder="选择月份"
          format="YYYY年MM月"
          value-format="YYYY-MM"
          @change="onMonthChange"
        />
        <el-input
          v-model="searchName"
          placeholder="输入会员名字搜索"
          style="width: 220px"
          clearable
          @keyup.enter="searchMember"
        />
        <el-button type="primary" @click="searchMember" :loading="loading">查询</el-button>
      </div>
    </el-card>

    <!-- 查询结果 -->
    <template v-if="result">
      <el-card class="result-card">
        <div class="result-summary">
          <span class="result-item">会员：<strong>{{ result.member_name }}</strong></span>
          <span class="result-item">本月单数：<strong>{{ result.total_count }}</strong></span>
          <span class="result-item">本月业绩：<strong class="amount">¥{{ result.total_amount.toFixed(2) }}</strong></span>
        </div>
      </el-card>

      <el-card v-if="result.records.length > 0" style="margin-top: 16px">
        <el-table :data="result.records" stripe>
          <el-table-column prop="date" label="日期" width="130" />
          <el-table-column label="类型" width="80">
            <template #default="{ row }">
              <el-tag v-if="row.is_refund" type="danger" size="small">退款</el-tag>
              <el-tag v-else :type="row.channel === 'store' ? 'success' : 'warning'" size="small">
                {{ row.channel === 'store' ? '到店' : '推销' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="salesperson_name" label="业务员" width="120">
            <template #default="{ row }">{{ row.salesperson_name || '-' }}</template>
          </el-table-column>
          <el-table-column label="金额" width="120">
            <template #default="{ row }">
              <span class="amount" :class="{ 'refund-amount': row.is_refund }">
                {{ row.is_refund ? '-' : '' }}¥{{ row.amount.toFixed(2) }}
              </span>
            </template>
          </el-table-column>
          <el-table-column prop="created_at" label="创建时间" />
        </el-table>
      </el-card>

      <el-card v-else style="margin-top: 16px">
        <el-empty description="该会员本月暂无消费记录" />
      </el-card>
    </template>

    <!-- 月会员业绩汇总 -->
    <el-card v-if="memberSummary.length > 0" class="summary-card" style="margin-top: 16px">
      <template #header>
        <span class="card-title">📊 {{ summaryYear }}年{{ summaryMonth }}月 会员业绩汇总</span>
      </template>
      <div class="summary-grid">
        <div v-for="m in memberSummary" :key="m.member_name" class="member-item">
          <div class="member-name">{{ m.member_name }}</div>
          <div class="member-amount" :class="{ 'negative': m.total_amount < 0 }">
            ¥{{ m.total_amount.toFixed(2) }}
          </div>
          <div class="member-count">{{ m.total_count }} 笔{{ m.has_refund ? '（含退款）' : '' }}</div>
        </div>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { reportsApi } from '../api'

const selectMonth = ref(new Date().toISOString().slice(0, 7))
const searchName = ref('')
const result = ref(null)
const loading = ref(false)
const memberSummary = ref([])
const summaryYear = ref('')
const summaryMonth = ref('')

const loadMemberSummary = async () => {
  try {
    const [year, month] = selectMonth.value.split('-')
    summaryYear.value = year
    summaryMonth.value = month.replace(/^0/, '')
    const res = await reportsApi.getMemberSummary(parseInt(year), parseInt(month))
    memberSummary.value = res.data
  } catch (e) {
    memberSummary.value = []
  }
}

const onMonthChange = () => {
  loadMemberSummary()
  if (searchName.value.trim()) {
    searchMember()
  }
}

const searchMember = async () => {
  if (!searchName.value.trim()) {
    ElMessage.warning('请输入会员名字')
    return
  }
  loading.value = true
  try {
    const [year, month] = selectMonth.value.split('-')
    const res = await reportsApi.getMember(parseInt(year), parseInt(month), searchName.value.trim())
    result.value = res.data
  } catch (e) {
    ElMessage.error('查询失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadMemberSummary()
})
</script>

<style scoped>
.member-report {
  max-width: 1000px;
  margin: 0 auto;
}

.card-title {
  font-weight: bold;
  font-size: 16px;
}

.search-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.result-summary {
  display: flex;
  gap: 24px;
  font-size: 15px;
  color: #606266;
  flex-wrap: wrap;
}

.result-item strong {
  color: #303133;
}

.result-item .amount {
  color: #e6a23c;
  font-size: 17px;
}

.amount {
  font-weight: bold;
  color: #303133;
}

.refund-amount {
  color: #f56c6c !important;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}

.member-item {
  background: #f0f9ff;
  border-radius: 8px;
  padding: 16px;
  text-align: center;
  border: 1px solid #e0f0ff;
}

.member-name {
  font-size: 15px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 6px;
}

.member-amount {
  font-size: 22px;
  font-weight: bold;
  color: #e6a23c;
}

.member-amount.negative {
  color: #f56c6c;
}

.member-count {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}
</style>
