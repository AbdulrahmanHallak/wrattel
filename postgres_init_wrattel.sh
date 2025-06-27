#!/bin/bash

set -e

DB_NAME="wrattel"
DB_USER="postgres"
INIT_SCRIPT="postgres_init.sql"
TABLES_SCRIPT="postgres_schema.sql"  # This is your table definitions file

# Step 1: Create the wrattel database
psql -U "$DB_USER" -f "$INIT_SCRIPT"

# Step 2: Run schema creation against wrattel
psql -U "$DB_USER" -d "$DB_NAME" -f "$TABLES_SCRIPT"

echo "Database '$DB_NAME' initialized and tables created."
