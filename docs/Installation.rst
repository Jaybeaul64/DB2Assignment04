Installation
============

.. _scripted-setup:

bash scripts
------------

The easiest way to setup the application is to use the setup.sh and db_setup.sh bash scripts.

You will need to give them both execute permition:

.. code-block:: console

    $ chmod +x setup.sh && chmod +x db_setup.sh

You still need to have python, pip and MySQL installed. If you need to know if they are properly installed on your system, see :ref:`Python-Installation` and :ref:`MySQL-Installation`.

for a totally fresh install, you can setup everything using the following two commands. The db_setup.sh might require root privileges depending on your MySQL installation.
use sudo if you did not setup a password for the root user.

.. code-block:: console

    $ ./setup.sh --create-venv
    $ ./db_setup.sh

The "setup.sh" script will create the virtual environment, install all required dependencies and compile the documentation. There are more tags available for this scripts:

--create-venv: will create a virtual environment.

--no-docs: will not compile the documentation.

--no-install: will skip the dependencies installation process.

The "db_setup.sh" script will execute the "table_creation.sql" script, create a new user in the database who only has access to the tables created and finally edit the .env file.

These two scripts are also available in batch for windows, though they were not tested and converted from the original bash files using AI. use at your own risk.

.. _Python-Installation:

Python Installation
-------------------

Make sure both python3 and pip3 are installed properly (version may change, output diffenrent based on Linux Distribution):

.. code-block:: console

    $ python3 --version && pip3 --version

Output should look like that. Keep in mind that versions and paths might be different:

.. code-block:: console
    
    Python 3.10.12
    pip 24.2 from /usr/local/lib/python3.10/dist-packages/pip (python 3.10)

If not, you can click `here <https://docs.python.org/3/using/unix.html>`_ for python documentation on installation.

.. _VENV-Setup:

Virtual Environment Setup
-------------------------

This application must run in a virtual environment. It is possible to create it using the setup.sh script, otherwise it will need to be created this way:

.. code-block:: console

    $ python3 -m venv venv
    $ source ./venv/bin/activate

Finally, install the required dependencies:

.. code-block:: console

    $ pip install -r requirements.txt

.. _MySQL-Installation:

MySQL Server Installation
-------------------------

Make sure MySQL is installed properly:

.. code-block:: console

    $ mysql --version

Output should look like that (version may change, output diffenrent based on Linux Distribution):

.. code-block:: console

    mysql  Ver 8.0.41-0ubuntu0.22.04.1 for Linux on x86_64 ((Ubuntu))

If an error occures, it means mysql-server is not installed properly. Follow the installation guide from Ubuntu Server's documentation `here <https://documentation.ubuntu.com/server/how-to/databases/install-mysql/index.html>`_.

If you're doing a manual installation, you'll need to run "table_creation.sql". Depending on your MySQL server installation, you will either need to enter your root credential or run the MySQL as root.

Run SQL script without root credentials:

.. code-block:: console

    $ sudo mysql < table_creation.sql

Run SQL script with credentials:

.. code-block:: console

    $ mysql -u [your username] -p < table_creation.sql

you can also run the "table_creation.sql" using any MySQL client. I use the "MySQL" extension in Visual Studio Code by "Database Client". Click `here <https://marketplace.visualstudio.com/items?itemName=cweijan.vscode-mysql-client2>`_ for more information about that.

If you're not using the provided bash script, you will need a user with at least SELECT, UPDATE and DELETE privileges on the database created from the "table_creation.sql" script. Documentation for that is available `here <https://dev.mysql.com/blog-archive/how-to-grant-privileges-to-users-in-mysql-80/>`_.

.. _env-setup:

ENV Variables
-------------

the .env file will be automatically generated if using the "db_setup.sh" script. Otherwise, it will need to be created manually.

An example .env file is available at the root of the project.
This file is named ".env.example". To run the application properly, you need to fill the appropriate values and rename the file to ".env".
The values should be written in plain text after the "=", without quotation marks and without commas to separate them (only new lines).

here are the values:

.. code-block:: text
    
    DB_HOST=127.0.0.1
    DB_USER=
    DB_PASSWORD=
    DB=task_db=task_db

- **DB_HOST**: The database host. It's the address ip of your database. Default is localhost.
- **DB_USER**: The database user to use to login.
- **DB_PASSWORD**: The database uer's password.
- **DB**: The database name that we're going to use. Value should be "task_db". Do not change this one.