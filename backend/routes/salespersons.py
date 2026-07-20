# -*- coding: utf-8 -*-
from fastapi import APIRouter, HTTPException
from typing import List
from models import SalespersonCreate, SalespersonUpdate, SalespersonResponse
from services.database import get_db

router = APIRouter()

@router.get("/", response_model=List[SalespersonResponse])
async def get_salespersons(active_only: bool = False):
    """获取业务员列表"""
    db = await get_db()
    try:
        if active_only:
            query = "SELECT * FROM salespersons WHERE is_active = 1 ORDER BY name"
        else:
            query = "SELECT * FROM salespersons ORDER BY name"
        cursor = await db.execute(query)
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        await db.close()

@router.post("/", response_model=SalespersonResponse)
async def create_salesperson(salesperson: SalespersonCreate):
    """新增业务员"""
    db = await get_db()
    try:
        cursor = await db.execute(
            "INSERT INTO salespersons (name, phone, position) VALUES (?, ?, ?)",
            (salesperson.name, salesperson.phone, salesperson.position)
        )
        await db.commit()
        new_id = cursor.lastrowid
        cursor = await db.execute("SELECT * FROM salespersons WHERE id = ?", (new_id,))
        row = await cursor.fetchone()
        return dict(row)
    finally:
        await db.close()

@router.put("/{salesperson_id}", response_model=SalespersonResponse)
async def update_salesperson(salesperson_id: int, salesperson: SalespersonUpdate):
    """编辑业务员"""
    db = await get_db()
    try:
        # 检查是否存在
        cursor = await db.execute("SELECT * FROM salespersons WHERE id = ?", (salesperson_id,))
        existing = await cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="业务员不存在")
        
        # 更新字段
        update_fields = []
        update_values = []
        if salesperson.name is not None:
            update_fields.append("name = ?")
            update_values.append(salesperson.name)
        if salesperson.phone is not None:
            update_fields.append("phone = ?")
            update_values.append(salesperson.phone)
        if salesperson.position is not None:
            update_fields.append("position = ?")
            update_values.append(salesperson.position)
        
        if update_fields:
            update_fields.append("updated_at = datetime('now', 'localtime')")
            update_values.append(salesperson_id)
            query = f"UPDATE salespersons SET {', '.join(update_fields)} WHERE id = ?"
            await db.execute(query, update_values)
            await db.commit()
        
        cursor = await db.execute("SELECT * FROM salespersons WHERE id = ?", (salesperson_id,))
        row = await cursor.fetchone()
        return dict(row)
    finally:
        await db.close()

@router.delete("/{salesperson_id}")
async def delete_salesperson(salesperson_id: int):
    """删除业务员"""
    db = await get_db()
    try:
        cursor = await db.execute("SELECT * FROM salespersons WHERE id = ?", (salesperson_id,))
        existing = await cursor.fetchone()
        if not existing:
            raise HTTPException(status_code=404, detail="业务员不存在")
        
        # 检查是否有关联的销售记录
        cursor = await db.execute("SELECT COUNT(*) as cnt FROM sales WHERE salesperson_id = ?", (salesperson_id,))
        row = await cursor.fetchone()
        if row["cnt"] > 0:
            raise HTTPException(status_code=400, detail="该业务员有关联的销售记录，无法删除。请先删除相关销售记录。")
        
        await db.execute("DELETE FROM salespersons WHERE id = ?", (salesperson_id,))
        await db.commit()
        return {"message": "删除成功"}
    finally:
        await db.close()
