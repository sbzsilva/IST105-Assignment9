import requests
from requests.auth import HTTPBasicAuth
from .dnac_config import DNAC
import urllib3
import sys
from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime
import pymongo
import os

# Disable SSL warnings for sandbox
urllib3.disable_warnings()

# MongoDB connection
try:
    # Try to get MongoDB connection details from environment variables
    mongo_host = os.environ.get('MONGODB_HOST', 'localhost')
    mongo_port = os.environ.get('MONGODB_PORT', '27017')
    mongo_db = os.environ.get('MONGODB_DB', 'assignment9')
    mongo_collection = os.environ.get('MONGODB_COLLECTION', 'logs')
    
    # Create MongoDB client
    client = pymongo.MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
    db = client[mongo_db]
    logs_collection = db[mongo_collection]
except Exception as e:
    print(f"Failed to connect to MongoDB: {str(e)}")
    logs_collection = None

class DNAC_Manager:

    def __init__(self):
        self.token = None

    def get_auth_token(self, display_token=False):
        """Authenticates to DNA Center and stores token"""
        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/dna/system/api/v1/auth/token"
            response = requests.post(
                url,
                auth=HTTPBasicAuth(DNAC['username'], DNAC['password']),
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            self.token = response.json()['Token']

            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "authentication",
                "result": "success",
                "details": "Token obtained successfully"
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)

            return True

        except Exception as e:
            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "authentication",
                "result": "failure",
                "details": str(e)
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)
                
            print(f" ❌  Authentication failed: {str(e)}")
            return False

    def get_network_devices(self):
        """Retrieves all network devices"""
        if not self.token:
            print(" ⚠️  Please authenticate first!")
            return None

        try:
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/network-device"
            headers = {"X-Auth-Token": self.token}
            response = requests.get(
                url,
                headers=headers,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            
            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "get_network_devices",
                "result": "success",
                "details": "Devices retrieved successfully"
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)
                
            return response.json().get('response', [])

        except Exception as e:
            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "get_network_devices",
                "result": "failure",
                "details": str(e)
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)
                
            print(f" ❌  Failed to get devices: {str(e)}")
            return None

    def display_devices(self, devices):
        """Formats device list output"""
        if not devices:
            print("No devices found!")
            return

        print("\n 📡  Network Devices")
        print("="*80)
        print(f"{'Hostname':20}{'IP Address':15}{'Platform':20}{'Status':10}")
        print("-"*80)

        for device in devices:
            print(
                f"{device.get('hostname', 'N/A'):20}"
                f"{device.get('managementIpAddress', 'N/A'):15}"
                f"{device.get('platformId', 'N/A'):20}"
                f"{device.get('reachabilityStatus', 'N/A'):10}"
            )

    def get_device_interfaces(self, device_ip):
        """Retrieves interfaces for specific device"""
        if not self.token:
            print(" ⚠️  Please authenticate first!")
            return None

        try:
            # Find device by IP
            devices = self.get_network_devices()
            device = next(
                (d for d in devices if d.get('managementIpAddress') == device_ip),
                None
            )
            if not device:
                # Log to MongoDB
                log_entry = {
                    "timestamp": datetime.utcnow(),
                    "action": "get_device_interfaces",
                    "result": "failure",
                    "details": f"Device {device_ip} not found!",
                    "ip_address": device_ip
                }
                if logs_collection:
                    logs_collection.insert_one(log_entry)
                    
                print(f" ❌  Device {device_ip} not found!")
                return None

            # Get interfaces
            url = f"https://{DNAC['host']}:{DNAC['port']}/api/v1/interface"
            headers = {"X-Auth-Token": self.token}
            params = {"deviceId": device['id']}
            response = requests.get(
                url,
                headers=headers,
                params=params,
                verify=False,
                timeout=10
            )
            response.raise_for_status()
            
            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "get_device_interfaces",
                "result": "success",
                "details": f"Interfaces retrieved for device {device_ip}",
                "ip_address": device_ip
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)
                
            return response.json().get('response', [])

        except Exception as e:
            # Log to MongoDB
            log_entry = {
                "timestamp": datetime.utcnow(),
                "action": "get_device_interfaces",
                "result": "failure",
                "details": str(e),
                "ip_address": device_ip if 'device_ip' in locals() else None
            }
            if logs_collection:
                logs_collection.insert_one(log_entry)
                
            print(f" ❌  Failed to get interfaces: {str(e)}")
            return None

    def display_interfaces(self, interfaces):
        """Formats interface output"""
        if not interfaces:
            print("No interfaces found!")
            return

        print("\n 🔌  Device Interfaces")
        print("="*80)
        print(f"{'Interface':20}{'Status':10}{'VLAN':10}{'Speed':10}")
        print("-"*80)

        for intf in interfaces:
            print(
                f"{intf.get('portName', 'N/A'):20}"
                f"{intf.get('status', 'N/A'):10}"
                f"{intf.get('vlanId', 'N/A'):10}"
                f"{intf.get('speed', 'N/A'):10}"
            )

def index(request):
    """Index page with menu options"""
    return render(request, 'dna_center_cisco/index.html')

def authenticate_view(request):
    """Authenticate and show token"""
    dnac = DNAC_Manager()
    if dnac.get_auth_token():
        token_display = dnac.token[:50] + "..." if len(dnac.token) > 50 else dnac.token
        context = {
            'token': dnac.token,
            'token_display': token_display,
            'success': True
        }
        return render(request, 'dna_center_cisco/auth_result.html', context)
    else:
        context = {
            'error': 'Authentication failed'
        }
        return render(request, 'dna_center_cisco/auth_result.html', context)

def list_devices_view(request):
    """List network devices"""
    dnac = DNAC_Manager()
    if not dnac.get_auth_token():
        context = {
            'error': 'Authentication failed'
        }
        return render(request, 'dna_center_cisco/devices_list.html', context)
    
    devices = dnac.get_network_devices()
    context = {
        'devices': devices
    }
    return render(request, 'dna_center_cisco/devices_list.html', context)

def device_interfaces_view(request):
    """Show device interfaces"""
    if request.method == 'POST':
        device_ip = request.POST.get('device_ip', '').strip()
        if not device_ip:
            context = {
                'error': 'Device IP is required'
            }
            return render(request, 'dna_center_cisco/interfaces_list.html', context)
        
        dnac = DNAC_Manager()
        if not dnac.get_auth_token():
            context = {
                'error': 'Authentication failed'
            }
            return render(request, 'dna_center_cisco/interfaces_list.html', context)
        
        interfaces = dnac.get_device_interfaces(device_ip)
        context = {
            'interfaces': interfaces,
            'device_ip': device_ip
        }
        return render(request, 'dna_center_cisco/interfaces_list.html', context)
    
    return render(request, 'dna_center_cisco/interfaces_form.html')

def view_logs(request):
    """View MongoDB logs"""
    if logs_collection:
        logs = list(logs_collection.find().sort("timestamp", -1).limit(50))
        # Convert ObjectId to string for serialization
        for log in logs:
            log['_id'] = str(log['_id'])
    else:
        logs = []
    
    context = {
        'logs': logs
    }
    return render(request, 'dna_center_cisco/logs.html', context)