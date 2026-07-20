# 楼邦建材业绩报表系统

自动区分"到店购买"与"业务员推销"渠道的业绩管理系统。

## 功能

- ✅ 按日期录入业绩，区分到店购买/业务员推销
- ✅ 业务员管理（新增、编辑、禁用）
- ✅ 日报/月报/季报/年报
- ✅ 数据导出 Excel
- ✅ 自动备份到 GitHub
- ✅ 刷新功能

## 技术栈

- 前端：Vue 3 + Vite + Element Plus
- 后端：Python FastAPI
- 数据库：SQLite
- 备份：GitHub API

## 本地开发

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境（首次）
python -m venv venv
.\venv\Scripts\activate

# 安装依赖
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

# 启动服务
uvicorn main:app --reload --port 8000
```

后端运行后访问 http://localhost:8000/docs 查看 API 文档

### 2. 启动前端

```bash
cd frontend

# 安装依赖（首次）
npm install

# 启动开发服务器
npm run dev
```

前端运行后访问 http://localhost:3000

### 3. 配置备份

在 backend 目录下创建 .env 文件：

```
GITHUB_TOKEN=你的GitHub Token
GITHUB_REPO=xiaokang22/-new
```

## 部署

项目使用 Railway 部署，详见部署配置。
