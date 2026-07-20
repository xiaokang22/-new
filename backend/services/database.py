# -*- coding: utf-8 -*-
import aiosqlite
import os
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sales.db")

async def get_db():
    """获取数据库连接"""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    return db

async def init_db():
    """初始化数据库表"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    db = await get_db()
    try:
        # 创建业务员表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS salespersons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                phone TEXT,
                position TEXT,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                updated_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        
        # 创建销售记录表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                channel TEXT NOT NULL CHECK(channel IN ('store', 'salesperson')),
                salesperson_id INTEGER,
                amount REAL NOT NULL CHECK(amount > 0),
                note TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (salesperson_id) REFERENCES salespersons(id)
            )
        """)
        
        # 创建备份记录表
        await db.execute("""
            CREATE TABLE IF NOT EXISTS backup_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                backup_type TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT,
                created_at TEXT DEFAULT (datetime('now', 'localtime'))
            )
        """)
        
        await db.commit()
        print("数据库初始化完成")
    finally:
        await db.close()
