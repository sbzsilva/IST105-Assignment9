#!/bin/bash

# Update system
sudo yum update -y

# Install Python and pip
sudo yum install python3 python3-pip -y

# Install virtualenv
sudo pip3 install virtualenv

# Install git
sudo yum install git -y

# Create and activate virtual environment
virtualenv ~/venv
source ~/venv/bin/activate

# Install Django and MongoDB driver
pip install django pymongo requests urllib3

# Clone the repository
cd ~
git clone https://github.com/sbzsilva/IST105-Assignment9.git
cd IST105-Assignment9/assignment9

# Set environment variables for MongoDB connection (these need to be updated with actual IPs)
echo "export MONGODB_HOST='localhost'" >> ~/.bashrc
echo "export MONGODB_PORT=27017" >> ~/.bashrc
echo "export MONGODB_DB='assignment9'" >> ~/.bashrc
echo "export MONGODB_COLLECTION='logs'" >> ~/.bashrc

echo "Web server installation completed!"
echo "Next steps:"
echo "1. Update the MONGODB_HOST environment variable in ~/.bashrc with the actual MongoDB private IP"
echo "2. Run: source ~/venv/bin/activate"
echo "3. Run: python3 manage.py migrate"
echo "4. Run: python3 manage.py runserver 0.0.0.0:8000"