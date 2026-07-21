<template>
  <div class="sales-entry">
    <!-- 日期选择 -->
    <el-card class="date-card">
      <div class="date-row">
        <span class="date-label">选择日期：</span>
        <el-date-picker
          v-model="selectedDate"
          type="date"
          placeholder="选择日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DD"
          :clearable="false"
          @change="loadRecords"
        />
      </div>
    </el-card>

    <div class="main-content">
      <!-- 左侧：录入表单 -->
      <el-card class="form-card">
        <template #header>
          <span class="card-title">📝 新增记录</span>
        </template>

        <el-form :model="form" label-width="80px">
          <el-form-item label="退款">
            <el-switch
              v-model="form.is_refund"
              active-text="是"
              inactive-text="否"
              @change="onRefundChange"
            />
          </el-form-item>

          <el-form-item label="渠道">
            <el-radio-group v-model="form.channel">
              <el-radio-button value="store">到店购买</el-radio-button>
              <el-radio-button value="salesperson">业务员推销</el-radio-button>
            </el-radio-group>
          </el-form-item>

          <el-form-item v-if="form.channel === 'salesperson'" label="业务员">
            <el-select v-model="form.salesperson_id" placeholder="选择业务员" style="width: 100%">
              <el-option
                v-for="sp in salespersons"
                :key="sp.id"
                :label="sp.name"
                :value="sp.id"
              />
            </el-select>
          </el-form-item>

          <el-form-item label="金额">
            <el-input-number
              v-model="form.amount"
              :min="0"
              :precision="2"
              :step="10"
              style="width: 100%"
            />
          </el-form-item>

          <el-form-item label="会员">
            <el-input
              v-model="form.note"
              :placeholder="'输入会员名字'"
            />
          </el-form-item>

          <el-form-item>
            <el-button type="primary" @click="submitForm" :loading="submitting" style="width: 100%">
              {{ form.is_refund ? '添加退款' : '添加记录' }}
            </el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 右侧：当日记录 -->
      <el-card class="records-card">
        <template #header>
          <div class="records-header">
            <span class="card-title">📋 当日记录</span>
            <span class="record-count">共 {{ records.length }} 条</span>
          </div>
        </template>

        <div v-if="records.length === 0" class="empty-state">
          <el-empty description="暂无记录" />
        </div>

        <div v-else class="records-list">
          <div v-for="record in records" :key="record.id" class="record-item" :class="{ 'refund-item': record.is_refund }">
            <div class="record-info">
              <div class="record-main">
                <el-tag v-if="record.is_refund" type="danger" size="small">退款</el-tag>
                <el-tag v-else :type="record.channel === 'store' ? 'success' : 'warning'" size="small">
                  {{ record.channel === 'store' ? '到店' : '推销' }}
                </el-tag>
                <span class="record-amount" :class="{ 'refund-amount': record.is_refund }">
                  {{ record.is_refund ? '-' : '' }}¥{{ record.amount.toFixed(2) }}
                </span>
                <span v-if="record.salesperson_name" class="record-person">{{ record.salesperson_name }}</span>
              </div>
              <div v-if="record.note" class="record-note">{{ record.is_refund ? '原因：' : '会员：' }}{{ record.note }}</div>
              <div class="record-time">{{ record.created_at }}</div>
            </div>
            <el-button
              type="danger"
              size="small"
              circle
              @click="deleteRecord(record.id)"
            >
              <el-icon><Delete /></el-icon>
            </el-button>
          </div>
        </div>

        <!-- 汇总 -->
        <div v-if="records.length > 0" class="summary">
          <el-divider />
          <div class="summary-grid">
            <div class="summary-item">
              <span class="summary-label">总业绩</span>
              <span class="summary-value">¥{{ summary.total.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">到店</span>
              <span class="summary-value store">¥{{ summary.store.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">推销</span>
              <span class="summary-value salesperson">¥{{ summary.salesperson.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span class="summary-label">退款</span>
              <span class="summary-value refund">¥{{ summary.refund.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { salesApi, salespersonsApi } from '../api'

const selectedDate = ref(new Date().toISOString().split('T')[0])
const records = ref([])
const salespersons = ref([])
const submitting = ref(false)

const form = reactive({
  channel: 'store',
  salesperson_id: null,
  amount: 0,
  note: '',
  is_refund: false
})

const onRefundChange = () => {
  form.salesperson_id = null
  form.note = ''
}

const summary = computed(() => {
  const store = records.value.filter(r => r.channel === 'store' && !r.is_refund).reduce((sum, r) => sum + r.amount, 0)
    - records.value.filter(r => r.channel === 'store' && r.is_refund).reduce((sum, r) => sum + r.amount, 0)
  const salesperson = records.value.filter(r => r.channel === 'salesperson' && !r.is_refund).reduce((sum, r) => sum + r.amount, 0)
    - records.value.filter(r => r.channel === 'salesperson' && r.is_refund).reduce((sum, r) => sum + r.amount, 0)
  const refund = records.value.filter(r => r.is_refund).reduce((sum, r) => sum + r.amount, 0)
  const total = store + salesperson
  return { total, store, salesperson, refund }
})

const loadSalespersons = async () => {
  try {
    const res = await salespersonsApi.getList(true)
    salespersons.value = res.data
  } catch (e) {
    ElMessage.error('加载业务员失败')
  }
}

const loadRecords = async () => {
  try {
    const res = await salesApi.getList(selectedDate.value)
    records.value = res.data
  } catch (e) {
    ElMessage.error('加载记录失败')
  }
}

const submitForm = async () => {
  if (form.amount <= 0) {
    ElMessage.warning('请输入金额')
    return
  }
  if (form.channel === 'salesperson' && !form.salesperson_id) {
    ElMessage.warning('请选择业务员')
    return
  }

  submitting.value = true
  try {
    await salesApi.create({
      date: selectedDate.value,
      channel: form.channel,
      salesperson_id: form.salesperson_id,
      amount: form.amount,
      note: form.note,
      is_refund: form.is_refund
    })
    ElMessage.success(form.is_refund ? '退款添加成功' : '添加成功')
    form.amount = 0
    form.note = ''
    form.salesperson_id = null
    form.is_refund = false
    await loadRecords()
  } catch (e) {
    ElMessage.error('添加失败：' + (e.message || '未知错误'))
  } finally {
    submitting.value = false
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
    await loadRecords()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

onMounted(() => {
  loadSalespersons()
  loadRecords()
})
</script>

<style scoped>
.sales-entry {
  max-width: 1200px;
  margin: 0 auto;
}

.date-card {
  margin-bottom: 20px;
}

.date-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.date-label {
  font-weight: bold;
  font-size: 15px;
}

.main-content {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 20px;
}

.card-title {
  font-weight: bold;
  font-size: 16px;
}

.records-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.record-count {
  color: #909399;
  font-size: 13px;
}

.empty-state {
  padding: 40px 0;
}

.records-list {
  max-height: 500px;
  overflow-y: auto;
}

.record-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.record-item.refund-item {
  background-color: #fef0f0;
  margin: 0 -20px;
  padding: 12px 20px;
}

.record-item:last-child {
  border-bottom: none;
}

.record-info {
  flex: 1;
}

.record-main {
  display: flex;
  align-items: center;
  gap: 10px;
}

.record-amount {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.record-amount.refund-amount {
  color: #f56c6c;
}

.record-person {
  color: #909399;
  font-size: 13px;
}

.record-note {
  color: #909399;
  font-size: 13px;
  margin-top: 4px;
}

.record-time {
  color: #c0c4cc;
  font-size: 12px;
  margin-top: 2px;
}

.summary {
  margin-top: 10px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.summary-item {
  text-align: center;
}

.summary-label {
  display: block;
  color: #909399;
  font-size: 13px;
  margin-bottom: 4px;
}

.summary-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}

.summary-value.store {
  color: #67c23a;
}

.summary-value.salesperson {
  color: #e6a23c;
}

.summary-value.refund {
  color: #f56c6c;
}
</style>
