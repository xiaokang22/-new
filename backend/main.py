# -*- coding: utf-8 -*-
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from services.database import init_db
from routes import sales, salespersons, reports, backup

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时初始化数据库
    await init_db()
    yield

app = FastAPI(
    title="楼邦建材业绩报表系统",
    description="自动区分到店购买与业务员推销渠道的业绩管理系统",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(sales.router, prefix="/api/sales", tags=["销售记录"])
app.include_router(salespersons.router, prefix="/api/salespersons", tags=["业务员"])
app.include_router(reports.router, prefix="/api/reports", tags=["报表"])
app.include_router(backup.router, prefix="/api/backup", tags=["备份"])

@app.get("/")
async def root():
    return {"message": "楼邦建材业绩报表系统 API"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
