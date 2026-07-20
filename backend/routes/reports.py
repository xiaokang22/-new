# -*- coding: utf-8 -*-
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from typing import Optional
from services.database import get_db
from services.excel import export_excel
import io

router = APIRouter()

@router.get("/daily")
async def get_daily_report(date: str):
    """获取日报数据"""
    db = await get_db()
    try:
        # 获取当天汇总
        cursor = await db.execute("""
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(amount), 0) as total_amount,
                COALESCE(SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END), 0) as store_amount,
                COALESCE(SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END), 0) as salesperson_amount,
                SUM(CASE WHEN channel = 'store' THEN 1 ELSE 0 END) as store_count,
                SUM(CASE WHEN channel = 'salesperson' THEN 1 ELSE 0 END) as salesperson_count
            FROM sales WHERE date = ?
        """, (date,))
        summary = dict(await cursor.fetchone())
        
        # 计算占比和笔均
        summary["store_ratio"] = summary["total_amount"] > 0 and summary["store_amount"] / summary["total_amount"] * 100 or 0
        summary["avg_amount"] = summary["total_count"] > 0 and summary["total_amount"] / summary["total_count"] or 0
        summary["date"] = date
        
        # 获取明细
        cursor = await db.execute("""
            SELECT s.*, sp.name as salesperson_name 
            FROM sales s 
            LEFT JOIN salespersons sp ON s.salesperson_id = sp.id 
            WHERE s.date = ? 
            ORDER BY s.created_at DESC
        """, (date,))
        details = [dict(row) for row in await cursor.fetchall()]
        
        return {"summary": summary, "details": details}
    finally:
        await db.close()

@router.get("/monthly")
async def get_monthly_report(year: int, month: int):
    """获取月报数据"""
    db = await get_db()
    try:
        # 获取月度汇总
        cursor = await db.execute("""
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(amount), 0) as total_amount,
                COALESCE(SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END), 0) as store_amount,
                COALESCE(SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END), 0) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
        """, (str(year), f"{month:02d}"))
        summary = dict(await cursor.fetchone())
        summary["year"] = year
        summary["month"] = month
        
        # 获取每日数据
        cursor = await db.execute("""
            SELECT 
                date,
                SUM(amount) as daily_amount,
                SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END) as store_amount,
                SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ? AND strftime('%m', date) = ?
            GROUP BY date
            ORDER BY date
        """, (str(year), f"{month:02d}"))
        daily_data = [dict(row) for row in await cursor.fetchall()]
        
        # 获取业务员数据
        cursor = await db.execute("""
            SELECT 
                sp.name as salesperson_name,
                SUM(s.amount) as total_amount,
                COUNT(*) as count
            FROM sales s
            JOIN salespersons sp ON s.salesperson_id = sp.id
            WHERE strftime('%Y', s.date) = ? AND strftime('%m', s.date) = ? AND s.channel = 'salesperson'
            GROUP BY s.salesperson_id
            ORDER BY total_amount DESC
        """, (str(year), f"{month:02d}"))
        salesperson_data = [dict(row) for row in await cursor.fetchall()]
        
        return {
            "summary": summary,
            "daily_data": daily_data,
            "salesperson_data": salesperson_data
        }
    finally:
        await db.close()

@router.get("/quarterly")
async def get_quarterly_report(year: int, quarter: int):
    """获取季报数据"""
    # 计算季度起止月份
    start_month = (quarter - 1) * 3 + 1
    end_month = quarter * 3
    
    db = await get_db()
    try:
        # 获取季度汇总
        cursor = await db.execute("""
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(amount), 0) as total_amount,
                COALESCE(SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END), 0) as store_amount,
                COALESCE(SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END), 0) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ? 
            AND CAST(strftime('%m', date) AS INTEGER) BETWEEN ? AND ?
        """, (str(year), start_month, end_month))
        summary = dict(await cursor.fetchone())
        summary["year"] = year
        summary["quarter"] = quarter
        
        # 获取每月数据
        cursor = await db.execute("""
            SELECT 
                strftime('%m', date) as month,
                SUM(amount) as monthly_amount,
                SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END) as store_amount,
                SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ? 
            AND CAST(strftime('%m', date) AS INTEGER) BETWEEN ? AND ?
            GROUP BY strftime('%m', date)
            ORDER BY month
        """, (str(year), start_month, end_month))
        monthly_data = [dict(row) for row in await cursor.fetchall()]
        
        return {
            "summary": summary,
            "monthly_data": monthly_data
        }
    finally:
        await db.close()

@router.get("/yearly")
async def get_yearly_report(year: int):
    """获取年报数据"""
    db = await get_db()
    try:
        # 获取年度汇总
        cursor = await db.execute("""
            SELECT 
                COUNT(*) as total_count,
                COALESCE(SUM(amount), 0) as total_amount,
                COALESCE(SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END), 0) as store_amount,
                COALESCE(SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END), 0) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ?
        """, (str(year),))
        summary = dict(await cursor.fetchone())
        summary["year"] = year
        
        # 获取每月数据
        cursor = await db.execute("""
            SELECT 
                strftime('%m', date) as month,
                SUM(amount) as monthly_amount,
                SUM(CASE WHEN channel = 'store' THEN amount ELSE 0 END) as store_amount,
                SUM(CASE WHEN channel = 'salesperson' THEN amount ELSE 0 END) as salesperson_amount
            FROM sales 
            WHERE strftime('%Y', date) = ?
            GROUP BY strftime('%m', date)
            ORDER BY month
        """, (str(year),))
        monthly_data = [dict(row) for row in await cursor.fetchall()]
        
        return {
            "summary": summary,
            "monthly_data": monthly_data
        }
    finally:
        await db.close()

@router.get("/export/excel")
async def export_excel_report(year: int, month: Optional[int] = None):
    """导出Excel报表"""
    db = await get_db()
    try:
        if month:
            # 月报
            cursor = await db.execute("""
                SELECT s.*, sp.name as salesperson_name 
                FROM sales s 
                LEFT JOIN salespersons sp ON s.salesperson_id = sp.id 
                WHERE strftime('%Y', s.date) = ? AND strftime('%m', s.date) = ?
                ORDER BY s.date, s.created_at
            """, (str(year), f"{month:02d}"))
            title = f"{year}年{month}月业绩报表"
        else:
            # 年报
            cursor = await db.execute("""
                SELECT s.*, sp.name as salesperson_name 
                FROM sales s 
                LEFT JOIN salespersons sp ON s.salesperson_id = sp.id 
                WHERE strftime('%Y', s.date) = ?
                ORDER BY s.date, s.created_at
            """, (str(year),))
            title = f"{year}年业绩报表"
        
        records = [dict(row) for row in await cursor.fetchall()]
        
        # 生成Excel
        excel_file = export_excel(records, title)
        
        return StreamingResponse(
            io.BytesIO(excel_file),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f"attachment; filename={title}.xlsx"}
        )
    finally:
        await db.close()
