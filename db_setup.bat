echo "this script was converted to batch from the bash script db_setup.sh. It is untested. Here be dragons"

@echo off

REM Define variables
set "env_file=.env"
set "sql_file=table_creation.sql"
set "database=task_db"

REM Check if MySQL is installed
where mysql >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: MySQL is not installed. Download it from https://dev.mysql.com/downloads/installer/
    exit /b 1
)

REM Prompt for MySQL credentials
echo Enter MySQL username:
set /p db_user=
echo Enter MySQL password:
set /p db_pass=

REM Execute SQL script
mysql -u %db_user% -p%db_pass% %database% < %sql_file%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to execute SQL script with provided credentials.
    exit /b 1
)
echo SQL script executed successfully.

REM Prompt for new user credentials
echo For security, create a new user with limited access.
echo Enter the new user's username:
set /p new_user=
echo Enter the new user's password:
set /p new_pass=

REM Create user SQL
setlocal EnableDelayedExpansion
set "create_user_sql=CREATE USER IF NOT EXISTS '!new_user!'@'%%' IDENTIFIED BY '!new_pass!'; GRANT SELECT, UPDATE, DELETE ON `%database%`.* TO '!new_user!'@'%%'; FLUSH PRIVILEGES;"

REM Execute user creation
echo !create_user_sql! | mysql -u %db_user% -p%db_pass%
if %ERRORLEVEL% NEQ 0 (
    echo Failed to create or configure the user.
    exit /b 1
)
echo User created with limited permissions on %database%.

REM Create .env file if not exists
if not exist %env_file% (
    echo DB_HOST=127.0.0.1 > %env_file%
    echo DB=%database% >> %env_file%
)

REM Replace or append DB_USER and DB_PASSWORD
findstr /B /C:"DB_USER=" %env_file% >nul && (
    powershell -Command "(Get-Content %env_file%) -replace '^DB_USER=.*', 'DB_USER=%new_user%' | Set-Content %env_file%"
) || (
    echo DB_USER=%new_user%>>%env_file%
)

findstr /B /C:"DB_PASSWORD=" %env_file% >nul && (
    powershell -Command "(Get-Content %env_file%) -replace '^DB_PASSWORD=.*', 'DB_PASSWORD=%new_pass%' | Set-Content %env_file%"
) || (
    echo DB_PASSWORD=%new_pass%>>%env_file%
)

echo .env file updated with new credentials.
endlocal
