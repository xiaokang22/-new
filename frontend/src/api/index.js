import supabase from '../supabase'
import * as XLSX from 'xlsx'

// 业务员 API
export const salespersonsApi = {
  async getList(activeOnly = false) {
    let query = supabase.from('salespersons').select('*').order('name')
    if (activeOnly) {
      query = query.eq('is_active', true)
    }
    const { data, error } = await query
    if (error) throw error
    return { data }
  },

  async create(salesperson) {
    const { data, error } = await supabase
      .from('salespersons')
      .insert({ name: salesperson.name, phone: salesperson.phone || null, position: salesperson.position || null })
      .select()
      .single()
    if (error) throw error
    return { data }
  },

  async update(id, salesperson) {
    const updateData = {}
    if (salesperson.name !== undefined) updateData.name = salesperson.name
    if (salesperson.phone !== undefined) updateData.phone = salesperson.phone || null
    if (salesperson.position !== undefined) updateData.position = salesperson.position || null
    updateData.updated_at = new Date().toISOString()
    const { data, error } = await supabase
      .from('salespersons')
      .update(updateData)
      .eq('id', id)
      .select()
      .single()
    if (error) throw error
    return { data }
  },

  async delete(id) {
    const { error } = await supabase
      .from('salespersons')
      .delete()
      .eq('id', id)
    if (error) throw error
    return { message: '删除成功' }
  }
}

// 销售记录 API
export const salesApi = {
  async getList(date) {
    let query = supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .order('created_at', { ascending: false })
    if (date) {
      query = query.eq('date', date)
    }
    const { data, error } = await query
    if (error) throw error
    const result = data.map(r => ({
      ...r,
      salesperson_name: r.salesperson?.name || null
    }))
    return { data: result }
  },

  async create(sale) {
    const { data, error } = await supabase
      .from('sales')
      .insert({
        date: sale.date,
        channel: sale.channel,
        salesperson_id: sale.salesperson_id || null,
        amount: sale.amount,
        note: sale.note || null,
        is_refund: sale.is_refund || false
      })
      .select('*, salesperson:salespersons(name)')
      .single()
    if (error) throw error
    return { data: { ...data, salesperson_name: data.salesperson?.name || null } }
  },

  async delete(id) {
    const { error } = await supabase
      .from('sales')
      .delete()
      .eq('id', id)
    if (error) throw error
    return { message: '删除成功' }
  }
}

// 报表 API
export const reportsApi = {
  async getDaily(date) {
    const { data: records, error } = await supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .eq('date', date)
      .order('created_at', { ascending: false })
    if (error) throw error

    const details = records.map(r => ({ ...r, salesperson_name: r.salesperson?.name || null }))
    const saleRecords = details.filter(r => !r.is_refund)
    const refundRecords = details.filter(r => r.is_refund)
    const refundAmount = refundRecords.reduce((s, r) => s + r.amount, 0)

    const total_amount = saleRecords.reduce((s, r) => s + r.amount, 0) - refundAmount
    const total_count = saleRecords.length
    const store_amount = saleRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0)
    const salesperson_amount = saleRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0)
    const store_count = saleRecords.filter(r => r.channel === 'store').length
    const salesperson_count = saleRecords.filter(r => r.channel === 'salesperson').length

    return {
      data: {
        summary: {
          date,
          total_amount,
          store_amount,
          salesperson_amount,
          total_count,
          store_count,
          salesperson_count,
          store_ratio: total_amount > 0 ? store_amount / total_amount * 100 : 0,
          avg_amount: total_count > 0 ? total_amount / total_count : 0,
          refund_amount: refundAmount
        },
        details
      }
    }
  },

  async getMonthly(year, month) {
    const monthStr = String(month).padStart(2, '0')
    const { data: records, error } = await supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .gte('date', `${year}-${monthStr}-01`)
      .lt('date', `${year}-${monthStr}-32`)
    if (error) throw error

    const saleRecords = records.filter(r => !r.is_refund)
    const refundRecords = records.filter(r => r.is_refund)
    const refundAmount = refundRecords.reduce((s, r) => s + r.amount, 0)

    const total_amount = saleRecords.reduce((s, r) => s + r.amount, 0) - refundAmount
    const total_count = saleRecords.length
    const store_amount = saleRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0)
    const salesperson_amount = saleRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0)

    const dailyMap = {}
    for (const r of records) {
      if (!dailyMap[r.date]) dailyMap[r.date] = { date: r.date, daily_amount: 0, store_amount: 0, salesperson_amount: 0 }
      if (r.is_refund) {
        dailyMap[r.date].daily_amount -= r.amount
        if (r.channel === 'store') dailyMap[r.date].store_amount -= r.amount
        else dailyMap[r.date].salesperson_amount -= r.amount
      } else {
        dailyMap[r.date].daily_amount += r.amount
        if (r.channel === 'store') dailyMap[r.date].store_amount += r.amount
        else dailyMap[r.date].salesperson_amount += r.amount
      }
    }
    const daily_data = Object.values(dailyMap).sort((a, b) => a.date.localeCompare(b.date))

    const spMap = {}
    for (const r of records) {
      if (r.channel === 'salesperson' && r.salesperson?.name) {
        const name = r.salesperson.name
        if (!spMap[name]) spMap[name] = { salesperson_name: name, total_amount: 0, count: 0 }
        if (r.is_refund) {
          spMap[name].total_amount -= r.amount
        } else {
          spMap[name].total_amount += r.amount
          spMap[name].count++
        }
      }
    }
    const salesperson_data = Object.values(spMap).sort((a, b) => b.total_amount - a.total_amount)

    return {
      data: { summary: { year, month, total_amount, store_amount, salesperson_amount, total_count, refund_amount: refundAmount }, daily_data, salesperson_data }
    }
  },

  async getYearly(year) {
    const { data: records, error } = await supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .gte('date', `${year}-01-01`)
      .lt('date', `${year + 1}-01-01`)
    if (error) throw error

    const saleRecords = records.filter(r => !r.is_refund)
    const refundRecords = records.filter(r => r.is_refund)
    const refundAmount = refundRecords.reduce((s, r) => s + r.amount, 0)

    const total_amount = saleRecords.reduce((s, r) => s + r.amount, 0) - refundAmount
    const total_count = saleRecords.length
    const store_amount = saleRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'store').reduce((s, r) => s + r.amount, 0)
    const salesperson_amount = saleRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0) - refundRecords.filter(r => r.channel === 'salesperson').reduce((s, r) => s + r.amount, 0)

    const monthMap = {}
    for (const r of records) {
      const m = r.date.substring(5, 7)
      if (!monthMap[m]) monthMap[m] = { month: m, monthly_amount: 0, store_amount: 0, salesperson_amount: 0 }
      if (r.is_refund) {
        monthMap[m].monthly_amount -= r.amount
        if (r.channel === 'store') monthMap[m].store_amount -= r.amount
        else monthMap[m].salesperson_amount -= r.amount
      } else {
        monthMap[m].monthly_amount += r.amount
        if (r.channel === 'store') monthMap[m].store_amount += r.amount
        else monthMap[m].salesperson_amount += r.amount
      }
    }
    const monthly_data = Object.values(monthMap).sort((a, b) => a.month.localeCompare(b.month))

    const spMap = {}
    for (const r of records) {
      if (r.salesperson?.name) {
        const name = r.salesperson.name
        if (!spMap[name]) spMap[name] = { salesperson_name: name, total_amount: 0, count: 0 }
        if (r.is_refund) {
          spMap[name].total_amount -= r.amount
        } else {
          spMap[name].total_amount += r.amount
          spMap[name].count++
        }
      }
    }
    const salesperson_data = Object.values(spMap).sort((a, b) => b.total_amount - a.total_amount)

    return {
      data: { summary: { year, total_amount, store_amount, salesperson_amount, total_count, refund_amount: refundAmount }, monthly_data, salesperson_data }
    }
  },

  async getMember(year, month, memberName) {
    const monthStr = String(month).padStart(2, '0')
    const { data: records, error } = await supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .eq('note', memberName)
      .gte('date', `${year}-${monthStr}-01`)
      .lt('date', `${year}-${monthStr}-32`)
      .order('date')
    if (error) throw error

    const details = records.map(r => ({ ...r, salesperson_name: r.salesperson?.name || null }))
    const saleRecords = details.filter(r => !r.is_refund)
    const refundRecords = details.filter(r => r.is_refund)
    const refundAmount = refundRecords.reduce((s, r) => s + r.amount, 0)

    return {
      data: {
        member_name: memberName,
        year,
        month,
        total_amount: saleRecords.reduce((s, r) => s + r.amount, 0) - refundAmount,
        total_count: saleRecords.length,
        records: details
      }
    }
  },

  async exportExcel(year, month) {
    let query = supabase
      .from('sales')
      .select('*, salesperson:salespersons(name)')
      .gte('date', `${year}-01-01`)
      .lt('date', `${year + 1}-01-01`)
      .order('date')
    if (month) {
      const monthStr = String(month).padStart(2, '0')
      query = supabase
        .from('sales')
        .select('*, salesperson:salespersons(name)')
        .gte('date', `${year}-${monthStr}-01`)
        .lt('date', `${year}-${monthStr}-32`)
        .order('date')
    }
    const { data, error } = await query
    if (error) throw error
    const records = data.map(r => ({ ...r, salesperson_name: r.salesperson?.name || null }))

    const title = month ? `${year}年${month}月业绩报表` : `${year}年业绩报表`
    const rows = records.map(r => ({
      '日期': r.date,
      '渠道': r.channel === 'store' ? '到店购买' : '业务员推销',
      '类型': r.is_refund ? '退款' : '销售',
      '业务员': r.salesperson_name || '-',
      '金额': r.is_refund ? -r.amount : r.amount,
      '备注': r.note || '',
      '创建时间': r.created_at
    }))

    const ws = XLSX.utils.json_to_sheet(rows)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, '业绩报表')
    XLSX.writeFile(wb, `${title}.xlsx`)
  }
}