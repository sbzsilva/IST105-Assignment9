# IST105 Assignment 9: Cisco DNA Center Network Automation

## Description
This is a Django web application that demonstrates network automation using Cisco DNA Center REST API. The application provides a web interface to authenticate with Cisco DNA Center, list network devices, and view interface details for specific devices. All interactions are logged to a MongoDB database.

## Features
- Authentication with Cisco DNA Center sandbox
- Retrieve and display network device inventory
- Fetch and analyze interface configurations for specific devices
- MongoDB integration for logging all API interactions
- Responsive web interface with Django templates
- Deployment scripts for AWS EC2 instances

## Prerequisites
- Python 3.8+
- Django 5.2+
- MongoDB
- AWS CLI configured (for EC2 deployment)

## Setup Instructions

### Local Development Setup
1. Clone the repository:
   ```
   git clone https://github.com/sbzsilva/IST105-Assignment9.git
   ```

2. Navigate to the project directory:
   ```
   cd IST105-Assignment9/assignment9
   ```

3. Create a virtual environment and activate it:
   ```
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install required packages:
   ```
   pip install -r requirements.txt
   ```

5. Run database migrations:
   ```
   python manage.py migrate
   ```

6. Start the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at `http://127.0.0.1:8000`

### AWS EC2 Deployment
1. Run the setup script to create EC2 instances:
   ```
   ./setup_ec2.sh
   ```

2. SSH into the MongoDB instance and run:
   ```
   ./install_mongodb.sh
   ```

3. SSH into the Web Server instance and run:
   ```
   ./install_webserver.sh
   ```

4. Update the MongoDB connection settings in the web server's `~/.bashrc` file with the private IP of the MongoDB instance

5. Run the Django application:
   ```
   python3 manage.py runserver 0.0.0.0:8000
   ```

## Project Structure
```
assignment9/
├── assignment9/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── dna_center_cisco/             # Main Django app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   ├── dnac_config.py           # Cisco DNA Center credentials
│   └── templates/               # HTML templates
│       └── dna_center_cisco/
│           ├── base.html
│           ├── index.html
│           ├── auth_result.html
│           ├── devices_list.html
│           ├── interfaces_form.html
│           ├── interfaces_list.html
│           └── logs.html
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
├── setup_ec2.sh                 # AWS EC2 setup script
├── install_mongodb.sh           # MongoDB installation script
└── install_webserver.sh         # Web server installation script
```

## Usage
1. Navigate to the home page to see an overview of the application
2. Click "Authenticate" to connect to Cisco DNA Center and obtain an authentication token
3. Click "Network Devices" to list all devices managed by DNA Center
4. Click "Device Interfaces" to view interfaces for a specific device by IP address
5. Click "View Logs" to see MongoDB logs of all operations

## Cisco DNA Center Sandbox
This application uses the Cisco DevNet sandbox environment:
- Host: sandboxdnac.cisco.com
- Username: devnetuser
- Password: Cisco123!

## MongoDB Integration
All operations are logged to MongoDB with the following information:
- Timestamp
- Action performed (authentication, device listing, interface retrieval)
- Result (success/failure)
- Details about the operation
- Device IP address (when applicable)

## Branches
- main: Final stable code
- development: Testing integration

## Screenshots
Include screenshots in your submission showing:
1. Authentication token displayed in browser
2. Device list output rendered via Django
3. Interface details for at least one device IP
4. Django app running in browser showing public IP
5. MongoDB terminal showing saved log entries
6. Your GitHub repository with all code