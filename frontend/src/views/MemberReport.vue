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
          @change="loadMembers"
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
          <el-table-column prop="created_at" label="创建时间" />
        </el-table>
      </el-card>

      <el-card v-else style="margin-top: 16px">
        <el-empty description="该会员本月暂无消费记录" />
      </el-card>
    </template>
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

const loadMembers = () => {
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

onMounted(() => {})
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
</style>
