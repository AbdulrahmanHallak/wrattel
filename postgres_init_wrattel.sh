#!/bin/bash

set -e

DB_NAME="wrattel"
DB_USER="postgres"
INIT_SCRIPT="postgres_init.sql"
TABLES_SCRIPT="postgres_schema.sql"  # This is your table definitions file
DATA_SCRIPT="postgres_data.sql"

psql -U "$DB_USER" -f "$INIT_SCRIPT"

psql -U "$DB_USER" -d "$DB_NAME" -f "$TABLES_SCRIPT"

psql -U "$DB_USER" -d "$DB_NAME" -f "$DATA_SCRIPT"

echo "Database '$DB_NAME' initialized, tables created, and data seeded."
