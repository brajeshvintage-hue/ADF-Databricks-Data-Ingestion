-- Databricks notebook source
USE CATALOG main;
USE SCHEMA de_pro_lab;
-- Day 21: persistent UC SQL function, distinct from session UDF registration.
CREATE OR REPLACE FUNCTION normalize_name_sql(s STRING)
RETURNS STRING
RETURN nullif(upper(trim(regexp_replace(s, '\\s+', ' '))), '');
SELECT normalize_name_sql('  Alice  Smith  '), normalize_name_sql(NULL);

-- COMMAND ----------
-- Day 22: policies attach only to this synthetic table.
CREATE OR REPLACE TABLE people_demo AS
SELECT 1 AS id, 'alice@example.test' AS email, 'CA' AS region
UNION ALL SELECT 2, 'bob@example.test', 'US';
CREATE OR REPLACE FUNCTION mask_email_lab(email STRING)
RETURNS STRING
RETURN CASE WHEN is_account_group_member('lab_pii_readers') THEN email ELSE '***' END;
ALTER TABLE people_demo ALTER COLUMN email SET MASK mask_email_lab;
CREATE OR REPLACE FUNCTION region_filter_lab(region STRING)
RETURNS BOOLEAN
RETURN is_account_group_member('lab_global_readers') OR region = 'CA';
ALTER TABLE people_demo SET ROW FILTER region_filter_lab ON (region);
SELECT * FROM people_demo;
-- Use a second principal with the grants below to verify behavior.
-- SELECT as the table owner alone does not prove least privilege.

-- COMMAND ----------
-- Replace with a real account-level group created for this exercise; execute as
-- an authorized grantor. These lines are intentionally gated, not auto-applied.
-- GRANT USE CATALOG ON CATALOG main TO `lab_analysts`;
-- GRANT USE SCHEMA ON SCHEMA main.de_pro_lab TO `lab_analysts`;
-- GRANT SELECT ON TABLE main.de_pro_lab.people_demo TO `lab_analysts`;
COMMENT ON TABLE people_demo IS 'Synthetic contacts for access-control experiments';
ALTER TABLE people_demo SET TAGS ('purpose' = 'training');
SHOW GRANTS ON TABLE people_demo;

-- COMMAND ----------
-- Day 24: deletion is logical first. Never lower retention to force a demonstration.
CREATE OR REPLACE TABLE purge_demo AS SELECT 1 AS subject_id, 'synthetic' AS payload;
DELETE FROM purge_demo WHERE subject_id = 1;
SELECT COUNT(*) FROM purge_demo;
DESCRIBE HISTORY purge_demo;
VACUUM purge_demo DRY RUN;
-- Map all replicas, source files, shares, checkpoints, CDF, backups and retention
-- obligations before claiming erasure. VACUUM cannot erase external copies.
