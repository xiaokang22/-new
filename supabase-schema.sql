-- =====================================================
-- 楼邦建材业绩报表系统 - Supabase 建表脚本
-- 在 Supabase 控制台的 SQL Editor 中执行此脚本
-- =====================================================

-- 1. 创建业务员表
CREATE TABLE IF NOT EXISTS salespersons (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    position TEXT,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. 创建销售记录表
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    date TEXT NOT NULL,
    channel TEXT NOT NULL CHECK(channel IN ('store', 'salesperson')),
    salesperson_id INTEGER REFERENCES salespersons(id),
    amount NUMERIC NOT NULL CHECK(amount > 0),
    note TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. 启用 RLS（行级安全策略）
ALTER TABLE salespersons ENABLE ROW LEVEL SECURITY;
ALTER TABLE sales ENABLE ROW LEVEL SECURITY;

-- 4. 创建策略允许所有操作（简化访问控制）
CREATE POLICY "Allow all operations on salespersons" ON salespersons FOR ALL USING (true);
CREATE POLICY "Allow all operations on sales" ON sales FOR ALL USING (true);

-- 5. 创建索引加速查询
CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(date);
CREATE INDEX IF NOT EXISTS idx_sales_channel ON sales(channel);
CREATE INDEX IF NOT EXISTS idx_sales_salesperson_id ON sales(salesperson_id);
CREATE INDEX IF NOT EXISTS idx_sales_note ON sales(note);
CREATE INDEX IF NOT EXISTS idx_salespersons_is_active ON salespersons(is_active);
