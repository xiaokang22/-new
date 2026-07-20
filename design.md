# 楼邦建材业绩报表系统 - 设计文档

## 1. 项目概述

为建材店店长打造的 Web 端业绩管理系统。核心目标：自动区分到店购买与业务员推销渠道，生成日报/月报/季报/年报，并确保数据永不丢失。

## 2. 技术栈

- 前端: Vue 3 + Vite + Element Plus
- 后端: Python FastAPI
- 数据库: SQLite (WAL模式)
- 数据导出: openpyxl (Excel)
- 备份: GitHub API + 本地定时备份
- 部署: Railway 免费版

## 3. 系统架构

前端(Vue 3) -> 后端(FastAPI) -> 数据库(SQLite) -> GitHub API 备份

## 4. 数据模型

### 4.1 业务员表 (salespersons)
- id: 自增主键
- name: 姓名 (必填)
- phone: 手机号
- position: 职位
- is_active: 是否启用 (默认 true)
- created_at: 创建时间
- updated_at: 更新时间

### 4.2 销售记录表 (sales)
- id: 自增主键
- date: 日期 (YYYY-MM-DD)
- channel: 渠道 (store=到店 / salesperson=推销)
- salesperson_id: 业务员ID (推销时必填)
- amount: 金额 (必填)
- note: 备注
- created_at: 创建时间

### 4.3 备份记录表 (backup_log)
- id: 自增主键
- backup_type: realtime(实时) / daily(每日)
- status: success / failed
- message: 备份结果描述
- created_at: 备份时间

## 5. 页面设计

### 5.1 数据录入页 (首页)
- 日期选择器 (默认今天)
- 刷新按钮
- 录入表单：渠道选择、业务员选择、金额、备注
- 当天记录列表，支持删除 (弹窗确认)
- 底部汇总：总业绩、到店总额、推销总额、笔数

### 5.2 业务员管理页
- 业务员列表：姓名、手机、职位、状态
- 新增/编辑弹窗
- 启用/禁用切换

### 5.3 报表页
- 筛选栏：日报/月报/季报/年报 + 日期选择
- 导出 Excel 按钮
- 汇总卡片：总业绩、渠道对比、笔均金额
- 销售明细表格，支持删除

## 6. API 设计

### 销售记录
- POST /api/sales - 新增
- GET /api/sales?date=YYYY-MM-DD - 查询
- DELETE /api/sales/{id} - 删除
- GET /api/sales/daily?date=YYYY-MM-DD - 日报
- GET /api/sales/monthly?year=YYYY&month=MM - 月报
- GET /api/sales/quarterly?year=YYYY&q=1 - 季报
- GET /api/sales/yearly?year=YYYY - 年报
- GET /api/sales/export/excel?year=YYYY&month=MM - 导出Excel

### 业务员
- GET /api/salespersons - 列表
- POST /api/salespersons - 新增
- PUT /api/salespersons/{id} - 编辑
- PATCH /api/salespersons/{id}/toggle - 启用/禁用

### 系统
- POST /api/backup/trigger - 手动备份
- GET /api/backup/status - 备份状态

## 7. 备份策略

### 7.1 实时备份
- 每次 POST/DELETE 销售记录后，自动触发 GitHub API 备份
- 将 sales.db 文件推送至 GitHub 私有仓库
- 备份失败时记录日志，不阻塞业务操作

### 7.2 每日本地备份
- 每天凌晨自动复制一份 db 文件
- 保留最近 30 天的备份

### 7.3 部署恢复
- 服务启动时自动从 GitHub 拉取最新数据库
- 若 GitHub 备份不存在，则使用本地数据库

## 8. 文件结构

楼邦建材业绩报表小程序/
├── frontend/                # Vue 3 前端
│   ├── src/
│   │   ├── views/
│   │   ├── components/
│   │   ├── api/
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   └── vite.config.js
├── backend/                 # FastAPI 后端
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   ├── services/
│   └── requirements.txt
├── data/                    # 数据目录
├── backups/                 # 本地备份
├── design.md                # 设计文档
├── plan.md                  # 实施计划
└── README.md
