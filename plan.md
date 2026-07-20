# 楼邦建材业绩报表系统 - 实施计划

## 任务清单

### 第一阶段：后端基础 (预计 30 分钟)

#### 任务 1.1：初始化 FastAPI 项目
- 文件：backend/main.py, backend/requirements.txt
- 安装依赖：fastapi, uvicorn, aiosqlite, openpyxl, pydantic
- 创建 FastAPI 应用实例
- 验证：运行 uvicorn main:app --reload，访问 /docs 查看 Swagger

#### 任务 1.2：创建数据库模型和初始化
- 文件：backend/models.py, backend/database.py
- 创建 salespersons、sales、backup_log 三张表
- 实现 WAL 模式
- 验证：运行脚本检查表是否创建成功

#### 任务 1.3：实现业务员 CRUD API
- 文件：backend/routes/salespersons.py
- GET /api/salespersons - 列表
- POST /api/salespersons - 新增
- PUT /api/salespersons/{id} - 编辑
- PATCH /api/salespersons/{id}/toggle - 启用/禁用
- 验证：用 Swagger 测试每个接口

#### 任务 1.4：实现销售记录 API
- 文件：backend/routes/sales.py
- POST /api/sales - 新增
- GET /api/sales?date=YYYY-MM-DD - 查询
- DELETE /api/sales/{id} - 删除
- 验证：用 Swagger 测试增删查

#### 任务 1.5：实现报表 API
- 文件：backend/routes/reports.py
- GET /api/sales/daily?date=YYYY-MM-DD
- GET /api/sales/monthly?year=YYYY&month=MM
- GET /api/sales/quarterly?year=YYYY&q=1
- GET /api/sales/yearly?year=YYYY
- 验证：用 Swagger 测试各报表接口

#### 任务 1.6：实现 Excel 导出
- 文件：backend/services/excel.py
- 设计 Excel 模板：标题、日期、汇总表、明细表
- 格式化：字体、边框、背景色
- 验证：导出文件检查格式

### 第二阶段：备份系统 (预计 20 分钟)

#### 任务 2.1：实现 GitHub 备份服务
- 文件：backend/services/backup.py
- GitHub API 调用：上传文件、获取文件
- 实时备份：每次写入后自动触发
- 验证：手动触发备份，检查 GitHub 仓库

#### 任务 2.2：实现每日本地备份
- 文件：backend/services/backup.py
- 定时任务：每天凌晨复制 db 文件
- 保留最近 30 天
- 验证：手动触发，检查备份文件

#### 任务 2.3：实现启动时恢复
- 文件：backend/main.py
- 服务启动时检查 GitHub 备份
- 自动恢复数据库
- 验证：删除本地 db，重启服务，检查恢复

### 第三阶段：前端开发 (预计 40 分钟)

#### 任务 3.1：初始化 Vue 3 项目
- 文件：frontend/
- 使用 Vite 创建项目
- 安装 Element Plus、axios
- 配置代理到后端 API
- 验证：运行 npm run dev，访问页面

#### 任务 3.2：开发数据录入页
- 文件：frontend/src/views/SalesEntry.vue
- 日期选择器组件
- 渠道切换组件（到店/推销）
- 业务员下拉选择
- 金额和备注输入
- 当天记录列表
- 汇总信息显示
- 验证：完整录入流程测试

#### 任务 3.3：开发业务员管理页
- 文件：frontend/src/views/Salespersons.vue
- 业务员列表表格
- 新增/编辑弹窗
- 启用/禁用切换
- 验证：CRUD 操作测试

#### 任务 3.4：开发报表页
- 文件：frontend/src/views/Reports.vue
- 报表类型切换
- 日期选择器
- 汇总卡片
- 销售明细表格
- 导出 Excel 按钮
- 验证：各报表类型显示正确

#### 任务 3.5：开发导航和布局
- 文件：frontend/src/App.vue
- 顶部导航栏
- 路由配置
- 响应式布局
- 验证：页面切换正常

### 第四阶段：集成测试 (预计 15 分钟)

#### 任务 4.1：端到端测试
- 录入数据 -> 查看报表 -> 导出 Excel
- 业务员管理 -> 录入推销记录 -> 查看报表
- 删除记录 -> 验证报表更新
- 验证：完整业务流程通过

#### 任务 4.2：备份系统测试
- 录入数据 -> 自动备份到 GitHub
- 删除本地 db -> 重启服务 -> 验证恢复
- 验证：数据不丢失

### 第五阶段：部署准备 (预计 10 分钟)

#### 任务 5.1：准备部署配置
- 文件：backend/Dockerfile, frontend/Dockerfile
- Railway 配置文件
- 环境变量模板
- 验证：本地构建 Docker 镜像成功

#### 任务 5.2：编写 README
- 本地开发说明
- 部署说明
- 环境变量配置说明
- 验证：文档完整清晰

## 总计时间：约 115 分钟（2 小时）

## 开发顺序
1. 先完成后端 API（任务 1.1-1.6）
2. 再完成备份系统（任务 2.1-2.3）
3. 然后开发前端（任务 3.1-3.5）
4. 最后集成测试和部署（任务 4.1-5.2）

## 注意事项
- 每个任务完成后立即测试
- 代码编写前先写测试用例
- 遇到问题立即记录并解决
- 保持代码简洁，避免过度设计
