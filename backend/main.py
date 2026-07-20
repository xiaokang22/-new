# -*- coding: utf-8 -*-
from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from services.database import init_db
from routes import sales, salespersons, reports, backup

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="楼邦建材业绩报表系统",
    description="自动区分到店购买与业务员推销渠道的业绩管理系统",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sales.router, prefix="/api/sales", tags=["销售记录"])
app.include_router(salespersons.router, prefix="/api/salespersons", tags=["业务员"])
app.include_router(reports.router, prefix="/api/reports", tags=["报表"])
app.include_router(backup.router, prefix="/api/backup", tags=["备份"])

@app.get("/health")
async def health():
    return {"status": "healthy"}

# 生产环境：托管前端静态文件
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
if os.path.isdir(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "楼邦建材业绩报表系统 API"}
