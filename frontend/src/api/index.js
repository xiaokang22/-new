import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// 销售记录 API
export const salesApi = {
  getList(date) {
    return api.get('/sales', { params: { date } })
  },
  create(data) {
    return api.post('/sales', data)
  },
  delete(id) {
    return api.delete(`/sales/${id}`)
  }
}

// 业务员 API
export const salespersonsApi = {
  getList(activeOnly = false) {
    return api.get('/salespersons', { params: { active_only: activeOnly } })
  },
  create(data) {
    return api.post('/salespersons', data)
  },
  update(id, data) {
    return api.put(`/salespersons/${id}`, data)
  },
  delete(id) {
    return api.delete(`/salespersons/${id}`)
  }
}

// 报表 API
export const reportsApi = {
  getDaily(date) {
    return api.get('/reports/daily', { params: { date } })
  },
  getMonthly(year, month) {
    return api.get('/reports/monthly', { params: { year, month } })
  },
  getQuarterly(year, quarter) {
    return api.get('/reports/quarterly', { params: { year, quarter } })
  },
  getYearly(year) {
    return api.get('/reports/yearly', { params: { year } })
  },
  exportExcel(year, month) {
    const params = { year }
    if (month) params.month = month
    return api.get('/reports/export/excel', { params, responseType: 'blob' })
  }
}

// 备份 API
export const backupApi = {
  trigger() {
    return api.post('/backup/trigger')
  },
  getStatus() {
    return api.get('/backup/status')
  }
}

export default api
