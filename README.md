# Cisco DNA Center Network Automation App

## Overview
This Django web application demonstrates network automation capabilities using the Cisco DNA Center REST API. It provides a user-friendly interface to interact with Cisco's DNA Center platform, allowing network administrators to view network devices, analyze interface configurations, and track all operations through comprehensive logging.

Whether you're a network engineer exploring automation possibilities or a developer learning network programmability, this application offers a practical example of integrating with enterprise networking platforms.

## Key Features
- **Cisco DNA Center Integration**: Seamless authentication and communication with Cisco DNA Center
- **Network Device Management**: View comprehensive inventory of network devices managed by DNA Center
- **Interface Analysis**: Detailed inspection of device interfaces and their configurations
- **Operation Logging**: All actions are automatically logged to MongoDB for audit and troubleshooting
- **Responsive Web Interface**: Clean, intuitive UI built with Django templates
- **Cloud Deployment Ready**: Includes scripts for easy deployment to AWS EC2 instances

## How It Works
The application connects to Cisco's DNA Center sandbox environment to retrieve real network data. Users can authenticate with the system, browse network devices, and examine interface details for any device. Every interaction is recorded in MongoDB, providing a complete audit trail of all operations.

This makes it ideal for:
- Learning network automation concepts
- Prototyping Cisco DNA Center integrations
- Monitoring network device configurations
- Tracking changes in network infrastructure

## Technology Stack
- **Backend**: Python/Django
- **Frontend**: HTML/CSS with Django Templates
- **Database**: MongoDB for operation logging
- **APIs**: Cisco DNA Center REST API
- **Deployment**: AWS EC2 ready with provided scripts

## Getting Started

### Prerequisites
- Python 3.8+
- Django 5.2+
- MongoDB
- AWS CLI configured (for cloud deployment)

### Quick Start
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

### Cloud Deployment
Deploy the application to AWS with the provided scripts:
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

## Application Components
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

## Using the Application
1. Navigate to the home page to see an overview of the application
2. Click "Authenticate" to connect to Cisco DNA Center and obtain an authentication token
3. Click "Network Devices" to list all devices managed by DNA Center
4. Click "Device Interfaces" to view interfaces for a specific device by IP address
5. Click "View Logs" to see MongoDB logs of all operations

## Cisco DNA Center Connection
The application uses the Cisco DevNet sandbox environment for demonstration purposes:
- Host: sandboxdnac.cisco.com
- Username: devnetuser
- Password: Cisco123!

To connect to your own Cisco DNA Center instance, modify the credentials in [dna_center_cisco/dnac_config.py](file:///C:/Users/ssilva/college/IST105-Assignment9/dna_center_cisco/dnac_config.py).

## Data Logging
All operations are automatically logged to MongoDB with the following information:
- Timestamp of the operation
- Type of action performed (authentication, device listing, interface retrieval)
- Success/failure status
- Detailed information about the operation
- Device IP address (when applicable)

This logging feature enables administrators to track all interactions with the network infrastructure, making it easier to audit changes and troubleshoot issues.

## Contributing
The project includes two main branches:
- `main`: Stable production code
- `development`: Testing and integration work

Feel free to fork the repository and submit pull requests with improvements or bug fixes.