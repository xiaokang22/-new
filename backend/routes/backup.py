# -*- coding: utf-8 -*-
from fastapi import APIRouter
from services.backup import trigger_backup, get_backup_status

router = APIRouter()

@router.post("/trigger")
async def manual_backup():
    """手动触发备份"""
    result = await trigger_backup()
    return result

@router.get("/status")
async def backup_status():
    """获取备份状态"""
    return await get_backup_status()
