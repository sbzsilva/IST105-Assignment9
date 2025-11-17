#!/bin/bash

# Update system
sudo dnf update -y

# Remove any existing MongoDB repo files
sudo rm -f /etc/yum.repos.d/mongodb-org*.repo

# Create MongoDB repo file for Amazon Linux 2023 - CORRECTED
echo "[mongodb-org-7.0]
name=MongoDB Repository
baseurl=https://repo.mongodb.org/yum/amazon/2023/mongodb-org/7.0/x86_64/
gpgcheck=1
enabled=1
gpgkey=https://pgp.mongodb.com/server-7.0.asc" | sudo tee /etc/yum.repos.d/mongodb-org-7.0.repo

# Clean dnf cache
sudo dnf clean all

# Install MongoDB
sudo dnf install -y mongodb-org

# Start MongoDB service
sudo systemctl start mongod
sudo systemctl enable mongod

# Configure MongoDB to accept remote connections
sudo sed -i 's/bindIp: 127.0.0.1/bindIp: 0.0.0.0/g' /etc/mongod.conf
sudo systemctl restart mongod

# Open firewall for MongoDB (if firewalld is installed)
if command -v firewall-cmd &> /dev/null; then
    sudo firewall-cmd --permanent --add-port=27017/tcp
    sudo firewall-cmd --reload
fi

# Install the MongoDB Shell (mongosh) if not already included
sudo dnf install -y mongodb-mongosh

# Create the assignment9 database and logs collection
mongosh --eval "use assignment9; db.createCollection('logs')"

echo "MongoDB installation completed!"
echo "MongoDB is now listening on 0.0.0.0:27017"