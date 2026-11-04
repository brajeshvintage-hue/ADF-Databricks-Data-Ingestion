-- Databricks notebook source
USE CATALOG main;
USE SCHEMA de_pro_lab;
-- Day 15: supported SQL warehouse/runtime required for VARIANT.
CREATE OR REPLACE TABLE raw_payloads AS
SELECT parse_json('{"order_id":1,"amount":25,"items":[{"sku":"A","qty":2}]}') AS payload
UNION ALL SELECT parse_json('{"order_id":2,"coupon":"SAVE"}');
SELECT payload:order_id::BIGINT AS order_id,
       variant_get(payload, '$.amount', 'double') AS amount,
       payload:coupon::STRING AS coupon
FROM raw_payloads;
SELECT try_parse_json('{invalid') AS malformed,
       is_variant_null(parse_json('null')) AS json_null;

-- COMMAND ----------
-- Day 29: grain is one order, not one line item. Do not join facts directly to
-- an SCD2 dimension without a point-in-time condition or you multiply revenue.
CREATE OR REPLACE VIEW fact_orders AS
SELECT order_id, customer_id, CAST(event_time AS DATE) AS order_date, region, amount
FROM silver_orders;
SELECT order_id, COUNT(*) AS n FROM fact_orders GROUP BY order_id HAVING COUNT(*) > 1;
SELECT SUM(amount) AS expected_revenue FROM fact_orders;

-- COMMAND ----------
-- UC metric view: run on a SQL warehouse/runtime supporting metric views.
CREATE OR REPLACE VIEW sales_metrics WITH METRICS LANGUAGE YAML AS
$$
version: 1.1
source: main.de_pro_lab.fact_orders
dimensions:
  - name: Region
    expr: region
measures:
  - name: Revenue
    expr: SUM(amount)
  - name: Orders
    expr: COUNT(*)
$$;
SELECT Region, MEASURE(Revenue), MEASURE(Orders) FROM sales_metrics GROUP BY Region;
