<template>
  <div class="salespersons">
    <el-card>
      <template #header>
        <div class="card-header">
          <span class="card-title">👥 业务员管理</span>
          <el-button type="primary" @click="openDialog()">
            <el-icon><Plus /></el-icon>
            新增业务员
          </el-button>
        </div>
      </template>

      <el-table :data="salespersons" stripe style="width: 100%">
        <el-table-column prop="name" label="姓名" width="120" />
        <el-table-column prop="phone" label="手机号" width="140" />
        <el-table-column prop="position" label="职位" width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180" />
        <el-table-column label="操作" min-width="180">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button type="danger" size="small" @click="deleteSalesperson(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑业务员' : '新增业务员'"
      width="400px"
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="姓名">
          <el-input v-model="form.name" placeholder="请输入姓名" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="职位">
          <el-input v-model="form.position" placeholder="请输入职位" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveForm" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { salespersonsApi } from '../api'

const salespersons = ref([])
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)
const saving = ref(false)

const form = reactive({
  name: '',
  phone: '',
  position: ''
})

const loadData = async () => {
  try {
    const res = await salespersonsApi.getList()
    salespersons.value = res.data
  } catch (e) {
    ElMessage.error('加载业务员列表失败')
  }
}

const openDialog = (row) => {
  if (row) {
    isEdit.value = true
    editId.value = row.id
    form.name = row.name
    form.phone = row.phone || ''
    form.position = row.position || ''
  } else {
    isEdit.value = false
    editId.value = null
    form.name = ''
    form.phone = ''
    form.position = ''
  }
  dialogVisible.value = true
}

const saveForm = async () => {
  if (!form.name.trim()) {
    ElMessage.warning('请输入姓名')
    return
  }

  saving.value = true
  try {
    if (isEdit.value) {
      await salespersonsApi.update(editId.value, { ...form })
      ElMessage.success('编辑成功')
    } else {
      await salespersonsApi.create({ ...form })
      ElMessage.success('新增成功')
    }
    dialogVisible.value = false
    await loadData()
  } catch (e) {
    ElMessage.error('操作失败：' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}

const deleteSalesperson = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除业务员「${row.name}」吗？`, '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await salespersonsApi.delete(row.id)
    ElMessage.success('删除成功')
    await loadData()
  } catch (e) {
    if (e !== 'cancel') {
      ElMessage.error('删除失败：' + (e.response?.data?.detail || e.message))
    }
  }
}

onMounted(() => {
  loadData()
})
</script>

<style scoped>
.salespersons {
  max-width: 1000px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-weight: bold;
  font-size: 16px;
}
</style>
