-- Databricks notebook source
-- Day 25. System schema access is controlled by the workspace/metastore admins.
SELECT workspace_id, sku_name, usage_unit, SUM(usage_quantity) AS quantity
FROM system.billing.usage
WHERE usage_date >= current_date() - INTERVAL 7 DAYS
GROUP BY ALL ORDER BY quantity DESC;
-- Quantity is not cost. Keep units separate; joining price lists requires matching
-- SKU, cloud and effective price dates, and list price is not your invoiced rate.

-- COMMAND ----------
SELECT * FROM system.lakeflow.job_run_timeline
WHERE period_start_time >= current_timestamp() - INTERVAL 1 DAY
LIMIT 20;

-- COMMAND ----------
SELECT event_time, action_name, service_name
FROM system.access.audit
WHERE event_date >= current_date() - INTERVAL 1 DAY
ORDER BY event_time DESC LIMIT 20;

-- COMMAND ----------
-- Day 26: replace the string with your actual pipeline ID before executing.
-- SELECT timestamp, event_type, message, details
-- FROM event_log('<pipeline-id>')
-- ORDER BY timestamp DESC LIMIT 100;

-- A local data-quality signal usable as an alert query:
SELECT COUNT(*) AS invalid_orders FROM main.de_pro_lab.quarantine_orders;
