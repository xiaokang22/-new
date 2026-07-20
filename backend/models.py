# -*- coding: utf-8 -*-
from pydantic import BaseModel
from typing import Optional
from datetime import date

class SalespersonCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    position: Optional[str] = None

class SalespersonUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    position: Optional[str] = None

class SalespersonResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    position: Optional[str]
    is_active: bool
    created_at: str
    updated_at: str

class SaleCreate(BaseModel):
    date: str
    channel: str  # 'store' or 'salesperson'
    salesperson_id: Optional[int] = None
    amount: float
    note: Optional[str] = None

class SaleResponse(BaseModel):
    id: int
    date: str
    channel: str
    salesperson_id: Optional[int]
    salesperson_name: Optional[str] = None
    amount: float
    note: Optional[str]
    created_at: str

class DailyReport(BaseModel):
    date: str
    total_amount: float
    store_amount: float
    salesperson_amount: float
    store_ratio: float
    avg_amount: float
    total_count: int
    store_count: int
    salesperson_count: int

class MonthlyReport(BaseModel):
    year: int
    month: int
    total_amount: float
    store_amount: float
    salesperson_amount: float
    total_count: int
    daily_data: list
    salesperson_data: list
