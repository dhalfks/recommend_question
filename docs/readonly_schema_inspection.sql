-- PostgreSQL / Neon schema inspection (read-only)
-- Run this after connecting to the intended database.
-- The transaction is explicitly read-only and is always rolled back.

BEGIN TRANSACTION READ ONLY;

SELECT
    current_database() AS database_name,
    current_schema() AS current_schema,
    version() AS server_version;

-- User-defined tables and views
SELECT
    table_schema,
    table_name,
    table_type
FROM information_schema.tables
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;

-- Columns, types, nullability, and defaults
SELECT
    table_schema,
    table_name,
    ordinal_position,
    column_name,
    data_type,
    udt_name,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name, ordinal_position;

-- Primary keys, unique constraints, foreign keys, and check constraints.
-- pg_get_constraintdef preserves ON DELETE/UPDATE actions and check expressions.
SELECT
    namespace.nspname AS table_schema,
    relation.relname AS table_name,
    constraint_record.conname AS constraint_name,
    CASE constraint_record.contype
        WHEN 'p' THEN 'PRIMARY KEY'
        WHEN 'u' THEN 'UNIQUE'
        WHEN 'f' THEN 'FOREIGN KEY'
        WHEN 'c' THEN 'CHECK'
        WHEN 'x' THEN 'EXCLUSION'
        ELSE constraint_record.contype::text
    END AS constraint_type,
    pg_get_constraintdef(constraint_record.oid, true) AS definition
FROM pg_constraint AS constraint_record
JOIN pg_class AS relation
  ON relation.oid = constraint_record.conrelid
JOIN pg_namespace AS namespace
  ON namespace.oid = relation.relnamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY namespace.nspname, relation.relname,
         constraint_record.contype, constraint_record.conname;

-- Indexes, including partial-index predicates
SELECT
    schemaname AS table_schema,
    tablename AS table_name,
    indexname AS index_name,
    indexdef AS definition
FROM pg_indexes
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY schemaname, tablename, indexname;

-- PostgreSQL enum types and their allowed values
SELECT
    namespace.nspname AS enum_schema,
    enum_type.typname AS enum_name,
    enum_value.enumsortorder,
    enum_value.enumlabel
FROM pg_type AS enum_type
JOIN pg_enum AS enum_value
  ON enum_type.oid = enum_value.enumtypid
JOIN pg_namespace AS namespace
  ON namespace.oid = enum_type.typnamespace
WHERE namespace.nspname NOT IN ('pg_catalog', 'information_schema')
ORDER BY namespace.nspname, enum_type.typname, enum_value.enumsortorder;

-- User-defined triggers (useful for professor ownership validation)
SELECT
    trigger_schema,
    event_object_table AS table_name,
    trigger_name,
    event_manipulation,
    action_timing,
    action_statement
FROM information_schema.triggers
WHERE trigger_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY trigger_schema, event_object_table, trigger_name, event_manipulation;

ROLLBACK;
