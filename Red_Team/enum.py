#!/usr/bin/env python3

import subprocess
import requests
import socket
import concurrent.futures

target_ip = input("Enter IP of Victim: ")
target_domain = input("Enter DNS of Victim: ")
directories_file = "Lists/Directorys.txt"
subdomains_file = "Lists/Subdomains.txt"

def port_scan(ip):
    open_ports = []
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for port in range(1, 65536):
            futures.append(executor.submit(scan_port, ip, port))
        for future in concurrent.futures.as_completed(futures):
            port, result = future.result()
            if result == 0:
                open_ports.append(port)
    return open_ports

def scan_port(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((ip, port))
    sock.close()
    return port, result

def service_detection(port):
    try:
        command = f"nmap -p{port} -sV --script=banner {target_ip}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.output}")

def web_page_enumeration(domain):
    try:
        response = requests.get(f"http://{domain}")
        
        if response.status_code == 200:
            print(f"Web page found: http://{domain}")
    except requests.exceptions.RequestException:
        pass

def subdomain_enumeration(domain):
    try:
        command = f"subdomain-enumeration-tool -d {domain}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.output}")

def directory_enumeration(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Directory found: {url}")
    except requests.exceptions.RequestException:
        pass

def search_exploits(service_name):
    try:
        command = f"searchsploit {service_name}"
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e.output}")

# Port scanning
open_ports = port_scan(target_ip)
print("Open ports:")
print(open_ports)

# Service detection
print("\nService detection:")
for port in open_ports:
    service_info = service_detection(port)
    print(service_info)

# Web page enumeration
print("\nWeb page enumeration:")
web_page_enumeration(target_domain)
web_page_enumeration(target_ip)

# Subdomain enumeration
print("\nSubdomain enumeration:")
with open(subdomains_file, "r") as subdomains_file:
    subdomains = subdomains_file.read().splitlines()
for subdomain in subdomains:
    subdomain_enumeration(subdomain)

# Directory enumeration
print("\nDirectory enumeration:")
with open(directories_file, "r") as directories_file:
    directories = directories_file.read().splitlines()
for directory in directories:
    directory_enumeration(directory)

# Vulnerability search
print("\nVulnerability search:")
for port in open_ports:
    search_results = search_exploits(f"service_name_{port}")  # Replace "service_name" with the actual service name
    print(search_results)
