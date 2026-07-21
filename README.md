# 楼邦建材业绩报表系统

为建材店店长打造的 Web 端业绩管理系统，自动区分"到店购买"与"业务员推销"渠道，支持会员管理，生成日报/月报/年报。

## 技术栈

- **前端**: Vue 3 + Vite + Element Plus
- **数据库**: Supabase (PostgreSQL)
- **部署**: Vercel (前端) + Supabase (数据库)
- **Excel 导出**: SheetJS (前端生成)

## 功能模块

- **数据录入** (`/entry`): 选择日期录入销售记录，支持到店/推销两种渠道
- **报表** (`/reports`): 日报/月报/年报，Excel 导出
- **业务员管理** (`/salespersons`): 增删改业务员
- **会员业绩汇总** (`/member`): 按会员查询本月消费记录

## 快速开始

### 1. 注册 Supabase

1. 访问 [supabase.com](https://supabase.com) 注册账号
2. 创建项目（选择 **Singapore** 区域，国内访问快）
3. 在 SQL Editor 中执行 `supabase-schema.sql`
4. 在 Settings → API 中获取 Project URL 和 anon key

### 2. 配置环境变量

在 `frontend/` 目录下创建 `.env` 文件：

```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your-anon-key-here
```

### 3. 本地开发

```bash
cd frontend
npm install
npm run dev
```

访问 http://127.0.0.1:3000

### 4. 部署到 Vercel

1. 访问 [vercel.com](https://vercel.com)，用 GitHub 登录
2. 导入 GitHub 仓库
3. 框架选 Vite，根目录填 `frontend`
4. 添加环境变量：
   - `VITE_SUPABASE_URL`: 你的 Supabase Project URL
   - `VITE_SUPABASE_ANON_KEY`: 你的 Supabase anon key
5. 部署

## 项目结构

```
loubang-project/
├── frontend/                    # Vue 3 前端
│   ├── src/
│   │   ├── api/index.js        # Supabase API 封装
│   │   ├── supabase.js         # Supabase 客户端配置
│   │   ├── views/              # 页面组件
│   │   ├── router/             # 路由配置
│   │   └── App.vue             # 主布局
│   ├── package.json
│   └── vite.config.js
├── backend/                     # Python FastAPI (已弃用)
├── supabase-schema.sql         # Supabase 建表脚本
├── vercel.json                  # Vercel 部署配置
└── README.md                    # 本文件
```

## 数据安全

- Supabase 自带数据存储和备份
- 启用 RLS（行级安全策略）保护数据
- 支持 Supabase Dashboard 手动备份

## 本地开发（无后端）

改造后前端直接调用 Supabase，不再需要启动 Python 后端。本地开发只需：

```bash
cd frontend
npm run dev
```

## 注意事项

1. **Supabase 免费额度**: 500MB 数据库 + 1GB 文件存储，足够日常使用
2. **Vercel 免费额度**: 每月 100GB 带宽，足够小型应用
3. **国内访问**: Supabase 选择 Singapore 区域，延迟约 200-300ms
4. **Excel 导出**: 现在由前端生成，无需服务器参与
