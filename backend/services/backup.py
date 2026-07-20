# -*- coding: utf-8 -*-
import os
import httpx
import base64
from datetime import datetime
from services.database import get_db

# GitHub 配置
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
GITHUB_REPO = os.getenv("GITHUB_REPO", "xiaokang22/-new")
GITHUB_BRANCH = "main"
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "sales.db")

async def trigger_backup():
    """触发实时备份到GitHub"""
    if not GITHUB_TOKEN:
        return {"status": "skipped", "message": "未配置GitHub Token"}
    
    try:
        # 读取数据库文件
        with open(DATABASE_PATH, "rb") as f:
            content = f.read()
        
        # Base64 编码
        content_base64 = base64.b64encode(content).decode("utf-8")
        
        # 检查文件是否已存在
        async with httpx.AsyncClient() as client:
            # 获取文件SHA（如果存在）
            check_url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/data/sales.db"
            headers = {
                "Authorization": f"token {GITHUB_TOKEN}",
                "Accept": "application/vnd.github.v3+json"
            }
            
            sha = None
            try:
                resp = await client.get(check_url, headers=headers)
                if resp.status_code == 200:
                    sha = resp.json().get("sha")
            except:
                pass
            
            # 上传文件
            data = {
                "message": f"Backup at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "content": content_base64,
                "branch": GITHUB_BRANCH
            }
            if sha:
                data["sha"] = sha
            
            resp = await client.put(check_url, headers=headers, json=data)
            
            if resp.status_code in [200, 201]:
                # 记录成功
                db = await get_db()
                try:
                    await db.execute(
                        "INSERT INTO backup_log (backup_type, status, message) VALUES (?, ?, ?)",
                        ("realtime", "success", "备份成功")
                    )
                    await db.commit()
                finally:
                    await db.close()
                
                return {"status": "success", "message": "备份成功"}
            else:
                raise Exception(f"GitHub API 错误: {resp.status_code}")
    
    except Exception as e:
        # 记录失败
        try:
            db = await get_db()
            try:
                await db.execute(
                    "INSERT INTO backup_log (backup_type, status, message) VALUES (?, ?, ?)",
                    ("realtime", "failed", str(e))
                )
                await db.commit()
            finally:
                await db.close()
        except:
            pass
        
        return {"status": "failed", "message": str(e)}

async def get_backup_status():
    """获取备份状态"""
    db = await get_db()
    try:
        cursor = await db.execute(
            "SELECT * FROM backup_log ORDER BY created_at DESC LIMIT 10"
        )
        logs = [dict(row) for row in await cursor.fetchall()]
        return {"logs": logs}
    finally:
        await db.close()

async def restore_from_github():
    """从GitHub恢复数据库"""
    if not GITHUB_TOKEN:
        return {"status": "skipped", "message": "未配置GitHub Token"}
    
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
                
                os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
                with open(DATABASE_PATH, "wb") as f:
                    f.write(content)
                
                return {"status": "success", "message": "恢复成功"}
            else:
                return {"status": "not_found", "message": "GitHub上没有备份文件"}
    
    except Exception as e:
        return {"status": "failed", "message": str(e)}
