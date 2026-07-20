# -*- coding: utf-8 -*-
import aiosqlite
import os
import base64
import httpx
from datetime import datetime

DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sales.db")

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "xiaokang22/-new")

async def get_db():
    """获取数据库连接"""
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA journal_mode=WAL")
    return db

async def init_db():
    """初始化数据库表，启动时自动检查并恢复数据"""
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    db = await get_db()
    try:
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
        
        # 安全检查：如果本地数据库为空，自动从 GitHub 恢复
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM sales")
        row = await cursor.fetchone()
        if row["cnt"] == 0:
            print("本地数据库为空，尝试从 GitHub 恢复...")
            restored = await _restore_from_github()
            if restored:
                print("从 GitHub 恢复数据成功")
            else:
                print("GitHub 恢复跳过或失败，使用空数据库")
        else:
            print(f"数据库初始化完成，已有 {row['cnt']} 条销售记录")
    finally:
        await db.close()

async def _restore_from_github():
    """从 GitHub 恢复数据库"""
    if not GITHUB_TOKEN:
        return False
    try:
        async with httpx.AsyncClient() as client:
            url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/data/sales.db"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            resp = await client.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                content = base64.b64decode(data["content"])
                with open(DATABASE_PATH, "wb") as f:
                    f.write(content)
                return True
            return False
    except Exception as e:
        print(f"GitHub 恢复失败: {e}")
        return False
