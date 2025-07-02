@echo off
setlocal

:: Configuration
set DB_NAME=wrattel
set DB_USER=postgres
set INIT_SCRIPT=postgres_init.sql
set TABLES_SCRIPT=postgres_schema.sql
set DATA_SCRIPT=postgres_data.sql

echo Creating database "%DB_NAME%"...

:: Step 1: Run the init.sql to create the database
psql -U %DB_USER% -f %INIT_SCRIPT%
if ERRORLEVEL 1 (
    echo Failed to run %INIT_SCRIPT%
    exit /b 1
)

:: Step 2: Run the table schema script on the new database
psql -U %DB_USER% -d %DB_NAME% -f %TABLES_SCRIPT%
if ERRORLEVEL 1 (
    echo Failed to run %TABLES_SCRIPT%
    exit /b 1
)

psql -U %DB_USER% -d %DB_NAME% -f %DATA_SCRIPT%
if ERRORLEVEL 1 (
    echo Failed to run %DATA_SCRIPT%
    exit /b 1
)

echo Database "%DB_NAME%" initialized, tables created, and data seeded.

endlocal
