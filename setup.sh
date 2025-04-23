#!/bin/bash

# tags: --create-venv --no-docs --no-install

compile_docs=true
install=true

for arg in "$@"; do
    # Creates venv
    if [[ "$arg" == "--create-venv" ]]; then
        python3 -m venv .venv
        source .venv/bin/activate
        echo "venv created. You will need do use the command "source .venv/bin/activate" to activate it prior to running the application."
    fi

    # compiles the documentation
    if [[ "$arg" == "--no-docs" ]]; thens
        compile_docs=false
    fi

    # install dependencies
    if [[ "$arg" == "--no-install" ]]; then
        install=false
    fi
done

# check if python and pip are installed.
if ! command -v python3 &> /dev/null; then
    echo -e "\033[0;31mError: python3 is not installed.\033[0m" >&2
    echo "Install it: https://docs.python.org/3/using/unix.html" >&2
    exit 1
fi

if ! command -v pip3 &> /dev/null; then
    echo -e "\033[0;31mError: pip3 is not installed.\033[0m" >&2
    echo "Install it: https://docs.python.org/3/using/unix.html" >&2
    exit 1
fi

# Check for venv. Exit if not.
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo -e "\033[0;31mError: This script must run inside a virtual environment.\033[0m"
    echo "Use the tag --create-venv if you want this script to create one for you."
    exit 1
fi

# install dependencies.
if $install; then
    pip install -r requirements.txt
fi

# compile documentation.
if $compile_docs; then
    cd docs || { echo -e "\033[0;31mFailed to cd into docs directory.\033[0m"; exit 1; }
    make clean && make html
    xdg-open _build/html/index.html >/dev/null 2>&1 &
fi