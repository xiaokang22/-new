-- 添加 is_refund 字段
ALTER TABLE sales ADD COLUMN IF NOT EXISTS is_refund BOOLEAN DEFAULT false;
