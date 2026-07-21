-- 添加 refund 渠道支持
ALTER TABLE sales DROP CONSTRAINT IF EXISTS sales_channel_check;
ALTER TABLE sales ADD CONSTRAINT sales_channel_check CHECK(channel IN ('store', 'salesperson', 'refund'));
