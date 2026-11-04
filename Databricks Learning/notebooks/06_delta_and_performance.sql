-- Databricks notebook source
-- Set these to the same catalog/schema as setup. Run one cell at a time.
USE CATALOG main;
USE SCHEMA de_pro_lab;

-- COMMAND ----------
-- Day 16: the toy table is isolated and can be reset before the exercise.
CREATE OR REPLACE TABLE delta_changes
TBLPROPERTIES ('delta.enableChangeDataFeed' = 'true') AS
SELECT 1 AS id, 'first' AS value;
UPDATE delta_changes SET value = 'updated' WHERE id = 1;
INSERT INTO delta_changes VALUES (2, 'second');
DELETE FROM delta_changes WHERE id = 2;
DESCRIBE HISTORY delta_changes;
-- Pick the CREATE/REPLACE version from history; do not assume every rerun starts at 0.
-- SELECT * FROM table_changes('main.de_pro_lab.delta_changes', <start_version>);

-- COMMAND ----------
-- Days 17–19: modest synthetic data; scale only after measuring cost.
CREATE OR REPLACE TABLE perf_orders USING DELTA AS
SELECT id AS order_id, id % 1000 AS customer_id, id % 7 AS region_id,
       CAST(id % 200 AS DOUBLE) AS amount
FROM range(100000);
EXPLAIN FORMATTED SELECT SUM(amount) FROM perf_orders WHERE customer_id = 42;
SELECT SUM(amount) FROM perf_orders WHERE customer_id = 42;
ALTER TABLE perf_orders CLUSTER BY (customer_id);
OPTIMIZE perf_orders;
DESCRIBE DETAIL perf_orders;
-- On supported compute/workspace, compare automated key selection:
-- ALTER TABLE perf_orders CLUSTER BY AUTO;
-- Record query profile bytes/files read, not merely elapsed time on this tiny table.

-- COMMAND ----------
-- Day 20: observe a join plan and broadcast strategy on a bounded dimension.
CREATE OR REPLACE TEMP VIEW dim_customer_demo AS
SELECT id AS customer_id, CONCAT('Customer ', id) AS name FROM range(1000);
EXPLAIN FORMATTED
SELECT /*+ BROADCAST(d) */ d.name, SUM(f.amount)
FROM perf_orders f JOIN dim_customer_demo d USING (customer_id)
GROUP BY d.name;
