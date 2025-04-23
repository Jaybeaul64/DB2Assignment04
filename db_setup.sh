#!/bin/bash

# allthough the setup.sh was all written by me, I can't say the same with this one. the logic is from me but most of it was written by ChatGPT

env_file=".env"
sql_file="table_creation.sql"
database="task_db"

if ! command -v mysql &> /dev/null; then
    echo "Error: MySQL is not installed. You can install it following this documentation: https://documentation.ubuntu.com/server/how-to/databases/install-mysql/index.html" >&2
    exit 1
fi

create_db_user() {
    echo "For security purposes, we need to create a new user with limited privileges that will only have access to the tables we just created."
    
    read -p "Enter the new user's username: " new_user
    read -s -p "Enter the new user's password: " new_pass
    echo

    create_user_sql="
    CREATE USER IF NOT EXISTS '$new_user'@'%' IDENTIFIED BY '$new_pass';
    GRANT SELECT, UPDATE, DELETE ON \`${database}\`.* TO '$new_user'@'%';
    FLUSH PRIVILEGES;
    "

    if [[ -z "$1" ]]; then
        if echo "$create_user_sql" | mysql -u root; then
            echo "User '$new_user'@'%' created with limited permissions on '$database'."
        else
            echo -e "\033[0;31m MySQL root access failed.\033[0m"
            exit 1
        fi
    else
        if echo "$create_user_sql" | mysql -u "$1" -p"$2"; then
            echo " User '$new_user'@'%' created with limited permissions on '$database'."
        else
            echo -e "\033[0;31m Failed to create or configure user.\033[0m"
            exit 1
        fi
    fi

    # Create the .env file with defaults if it doesn't exist
    if [[ ! -f "$env_file" ]]; then
        echo ".env file not found. Creating a new one with default values..."
        {
            echo "DB_HOST=127.0.0.1"
            echo "DB=$database"
        } > "$env_file"
    fi

    # Escape special characters (like $ or `) in password
    escaped_pass=$(printf '%s\n' "$new_pass" | sed -e 's/\\/\\\\/g' -e 's/&/\\&/g')

    # Update .env file
    # If keys exist, replace them. If not, append them.
    if grep -q "^DB_USER=" "$env_file"; then
        sed -i "s/^DB_USER=.*/DB_USER=$new_user/" "$env_file"
    else
        echo "DB_USER=$new_user" >> "$env_file"
    fi

    if grep -q "^DB_PASSWORD=" "$env_file"; then
        sed -i "s/^DB_PASSWORD=.*/DB_PASSWORD=$escaped_pass/" "$env_file"
    else
        echo "DB_PASSWORD=$escaped_pass" >> "$env_file"
    fi

    echo ".env file updated with provided credentials."
}

if [[ "$EUID" -eq 0 ]]; then
    echo "Running as Linux root — trying MySQL root access (no password)..."
    if mysql -u root "$database" < "$sql_file" 2>/dev/null; then
        echo "Successfully ran SQL as MySQL root with no password."
        create_db_user
        exit 0
    else
        echo -e "\033[0;31m MySQL root access failed.\033[0m"
    fi
else
    echo "Not running as root — skipping MySQL root access attempt."
fi

# Prompt for fallback MySQL user credentials
read -p "Enter MySQL username: " db_user
read -s -p "Enter MySQL password: " db_pass
echo

if mysql -u "$db_user" -p"$db_pass" "$database" < "$sql_file"; then
    echo "SQL script executed successfully."
    create_db_user "$db_user" "$db_pass"
else
    echo -e "\033[0;31m Failed to execute SQL script with provided credentials.\033[0m"
    exit 1
fi