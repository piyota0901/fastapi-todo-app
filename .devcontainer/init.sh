#!/bin/bash
set -e
cd /home
sudo apt update && sudo apt upgrade -y
sudo apt clean
sudo rm -rf /var/lib/apt/lists/*

echo "-------------------------"
echo "Install PostgreSQL"
echo "-------------------------"

# Create the file repository configuration:
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'

# Import the repository signing key:
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# Update the package lists:
sudo apt-get update

# Install the latest version of PostgreSQL.
# If you want a specific version, use 'postgresql-12' or similar instead of 'postgresql':
sudo apt-get -y install postgresql-15
sudo /usr/sbin/service postgresql start

echo "-------------------------"
echo "Setup Poetry"
echo "-------------------------"
cd /workspace
poetry install

echo "-------------------------"
echo "Initial setting for Postgresql"
echo "-------------------------"
sudo su - postgres <<EOF
/bin/sh /workspace/initdb/1_initdb.sh
/bin/sh /workspace/initdb/2_initTodo.sh
EOF

echo "-------------------------"
echo "Finish!!!!"
echo "-------------------------"

