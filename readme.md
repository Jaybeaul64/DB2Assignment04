# Compiling and Finding Documentation

## Using the Setup Bash Script

Simply run the `setup.sh` script with the `--create-venv` tag at the project's root directory.

There is a windows batch version, `setup.bat`, but it was converted from the `setup.sh` bash script using AI and is untested. Proceed at your own risk.

## Compiling Manualy
create the virtual environment: `$ python3 -m venv venv`  
activate the virtual environment: `$ source ./venv/bin/activate`  
install the required dependencies: `pip3 install -r requirements.txt`
move into the `docs/` directory: `cd docs`.  
delete the previously compiled documentation and comile it again: `make clean && make html`.

## Finding Compiled HTML Files

Compiled HTML files are located in the `docs/_build/html` directory. You can open any HTML file based on what you are looking for, but if you want to get to the documentation's home page, you need to open the `index.html` file. You can either open them normally using any browser or use something like the Visual Studio Code extention [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer).

# Performing Tests with Pytest

## Installing PyTest
To perform tests using pyTest, it needs to be installed first.

The application must be fully installed before running the tests. If it is not done already, follow the instructions from the documentation first. Documentation can be compiled by following the instructions above.

Install pytest using pip: `pip install -U pytest`  

## Running the tests
To run all the tests, run this command from the root directory: `pytest .`

You can also run specific tests from the test folder by typing `pytest/tests/[test you want to run].py`
