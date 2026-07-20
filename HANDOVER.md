# 楼邦建材业绩报表系统 - 项目交接文档

## 1. 项目目标
为建材店店长打造的 Web 端业绩管理系统，自动区分"到店购买"与"业务员推销"渠道，生成日报/月报/年报，并确保数据永不丢失。

## 2. 当前目录结构
`
loubang-project/
├── backend/                 # Python FastAPI 后端
│   ├── main.py             # 入口，FastAPI 应用
│   ├── models.py           # Pydantic 数据模型
│   ├── requirements.txt    # 依赖：fastapi, uvicorn, aiosqlite, openpyxl, pydantic, python-dotenv, httpx
│   ├── .env                # 环境变量：GITHUB_TOKEN, GITHUB_REPO
│   ├── routes/
│   │   ├── sales.py        # 销售记录 CRUD
│   │   ├── salespersons.py # 业务员 CRUD
│   │   ├── reports.py      # 报表查询 + Excel 导出
│   │   └── backup.py       # 备份接口
│   └── services/
│       ├── database.py     # SQLite 连接 + 表初始化
│       ├── backup.py       # GitHub API 备份逻辑
│       └── excel.py        # Excel 导出生成
├── frontend/                # Vue 3 + Vite + Element Plus 前端
│   ├── vite.config.js      # Vite 配置（代理 /api -> 127.0.0.1:8000）
│   ├── src/
│   │   ├── main.js         # 入口：Element Plus + 中文语言包 + 路由
│   │   ├── router/index.js # 路由：/entry, /salespersons, /reports
│   │   ├── api/index.js    # Axios API 封装
│   │   ├── App.vue         # 布局：顶部导航 + 路由视图
│   │   └── views/
│   │       ├── SalesEntry.vue     # 数据录入页
│   │       ├── Salespersons.vue   # 业务员管理页
│   │       └── Reports.vue        # 报表页（日报/月报/年报）
│   └── package.json        # 依赖：vue3, element-plus, axios, vue-router
├── data/sales.db           # SQLite 数据库文件
├── design.md               # 设计文档
├── plan.md                 # 实施计划
└── README.md               # 项目说明
`

## 3. 已完成的功能
- 后端 API 全部完成：销售记录 CRUD、业务员 CRUD、日报/月报/年报查询、Excel 导出、GitHub 备份
- 前端页面全部完成：数据录入、业务员管理、报表查看
- 数据库：SQLite WAL 模式，3 张表（salespersons, sales, backup_log）
- 备份：每次写入自动备份到 GitHub 私有仓库
- 中文：Element Plus 中文语言包
- 前端构建：
pm run build 通过

## 4. 正在开发/待修复的功能
- **报表页面标题显示错误**：月报和年报的明细表格标题需要区分（已提交代码但用户未确认效果）
- **导出 Excel 失败**：Vite 代理问题已修复（改为 127.0.0.1），但用户报告仍失败
- **后端依赖未安装**：需要手动在 backend/ 目录运行 pip install
- **前端所有页面报错**：用户截图显示日报/月报/年报全部操作失败

## 5. 关键技术栈
- 前端：Vue 3 + Vite 5 + Element Plus + Axios + Vue Router 4
- 后端：Python FastAPI + aiosqlite + openpyxl
- 数据库：SQLite（WAL 模式）
- 备份：GitHub REST API（Personal Access Token）
- 部署目标：Railway 免费版

## 6. 重要文件说明
- ackend/.env：包含 GITHUB_TOKEN 和 GITHUB_REPO，备份功能依赖此文件
- ackend/services/database.py：DATABASE_PATH = data/sales.db，init_db() 创建表
- rontend/vite.config.js：代理配置，/api 转发到 127.0.0.1:8000
- rontend/src/main.js：Element Plus 中文语言包配置

## 7. 已知问题
1. **后端服务经常需要重启**：Start-Process 启动的后端可能不稳定，用户需手动在 CMD 窗口运行
2. **前端代理 502 错误**：已修复为 127.0.0.1，但需确认前端重新启动
3. **报表页面数据显示混乱**：月报显示"每日业绩"标题，年报也是，需要修正标题和数据结构
4. **Excel 导出中文文件名编码问题**：已用 RFC 5987 编码修复
5. **提示消息显示时间**：已设为 1000ms（1秒）
6. **D 盘权限问题**：项目从 D:\Vibecoding项目1\楼邦建材业绩报表小程序 迁移到 C:\Users\user\Desktop\loubang-project

## 8. 下一步要做什么
1. **优先**：确认后端服务正常运行，检查 /api/health 是否返回 200
2. **优先**：确认前端代理工作正常（/api/health 通过 localhost:3000 能访问）
3. **修复报表页面**：确认月报显示每日明细、年报显示每月明细
4. **修复 Excel 导出**：确认导出功能正常工作
5. **部署到 Railway**：准备 Dockerfile 和 railway.json

## 9. 不能改动/需要注意的约束
- 数据安全是第一优先级，每次写入必须备份到 GitHub
- GitHub Token 不能提交到代码仓库（已加入 .gitignore）
- 项目路径不能有中文（已迁移到 C 盘桌面）
- 后端使用 venv 虚拟环境，必须用 .\venv\Scripts\python.exe 运行
- 前端使用 Vite 5（不用 Vite 8，兼容性问题）
- Element Plus 使用中文语言包 zh-cn
- 删除操作必须有二次确认弹窗

## 10. 启动命令
`ash
# 后端
cd C:\Users\user\Desktop\loubang-project\backend
.\venv\Scripts\pip.exe install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
.\venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000

# 前端
cd C:\Users\user\Desktop\loubang-project\frontend
npm install
npm run dev
`

## 11. GitHub 信息
- 仓库：xiaokang22/-new（私有）
- Token：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
- Git 配置：user.name=xiaokang22, user.email=xiaokang060418@163.com
