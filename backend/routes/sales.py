# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from typing import List, Optional
from models import SaleCreate, SaleResponse
from services.database import get_db
import asyncio
from services.backup import trigger_backup

router = APIRouter()

@router.get("/", response_model=List[SaleResponse])
async def get_sales(date: Optional[str] = None):
    """获取销售记录"""
    db = await get_db()
    try:
        if date:
            query = """
                SELECT s.*, sp.name as salesperson_name 
                FROM sales s 
                LEFT JOIN salespersons sp ON s.salesperson_id = sp.id 
                WHERE s.date = ? 
                ORDER BY s.created_at DESC
            """
            cursor = await db.execute(query, (date,))
        else:
            query = """
                SELECT s.*, sp.name as salesperson_name 
                FROM sales s 
                LEFT JOIN salespersons sp ON s.salesperson_id = sp.id 
                ORDER BY s.date DESC, s.created_at DESC
            """
            cursor = await db.execute(query)
        
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()

@router.post("/", response_model=SaleResponse)
async def create_sale(sale: SaleCreate):
    """新增销售记录"""
    # 验证渠道
    if sale.channel not in ['store', 'salesperson']:
        raise HTTPException(status_code=400, detail="渠道必须是 store 或 salesperson")
    
    # 验证金额
    if sale.amount <= 0:
        raise HTTPException(status_code=400, detail="金额必须大于0")
    
    # 如果是业务员推销，必须选择业务员
    if sale.channel == 'salesperson' and not sale.salesperson_id:
        raise HTTPException(status_code=400, detail="业务员推销必须选择业务员")
    
    db = await get_db()
    try:
        # 验证业务员是否存在
        if sale.salesperson_id:
            cursor = await db.execute(
                "SELECT * FROM salespersons WHERE id = ? AND is_active = 1",
                (sale.salesperson_id,)
            )
            salesperson = await cursor.fetchone()
            if not salesperson:
                raise HTTPException(status_code=400, detail="业务员不存在或已禁用")
        
        cursor = await db.execute(
            "INSERT INTO sales (date, channel, salesperson_id, amount, note) VALUES (?, ?, ?, ?, ?)",
            (sale.date, sale.channel, sale.salesperson_id, sale.amount, sale.note)
        )
        await db.commit()
        new_id = cursor.lastrowid
        
        # 获取完整记录
        cursor = await db.execute(
            "SELECT s.*, sp.name as salesperson_name FROM sales s LEFT JOIN salespersons sp ON s.salesperson_id = sp.id WHERE s.id = ?",
            (new_id,)
        )
        row = await cursor.fetchone()
        
        # 触发备份
        asyncio.create_task(trigger_backup())
        
        return dict(row)
    finally:
        await db.close()

@router.delete("/{sale_id}")
async def delete_sale(sale_id: int):
    """删除销售记录"""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM sales WHERE id = ?", (sale_id,))
        existing = await cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="记录不存在")
        
        await db.execute("DELETE FROM sales WHERE id = ?", (sale_id,))
        await db.commit()
        
        # 触发备份
        asyncio.create_task(trigger_backup())
        
        return {"message": "删除成功"}
    finally:
        await db.close()

