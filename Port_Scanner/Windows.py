import pyfiglet
import socket
from datetime import datetime
import concurrent.futures

# Display the ASCII banner
ascii_banner = pyfiglet.figlet_format("PORT SCANNER")
print(ascii_banner)

# Function to scan a single port
def scan_port(target, port):
    try:
        # Determine the address family based on the target IP
        if ':' in target:  # This indicates an IPv6 address
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:  # This indicates an IPv4 address
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        socket.setdefaulttimeout(1)
        result = s.connect_ex((target, port))
        s.close()
        return port, result == 0  # Return port and whether it's open
    except socket.error:
        return port, False  # Return port and closed status

# Function to scan a single target
def scan_target(target, ports):
    print("-" * 50)
    print("Scanning Target: " + target)
    print("Scanning started at: " + str(datetime.now()))
    print("-" * 50)

    # Split the input ports and convert to a list of integers
    port_list = []
    try:
        for port in ports.split(','):
            port = int(port.strip())
            if port < 1 or port > 65535:
                print(f"Invalid port number: {port}. Please enter a number between 1 and 65535.")
                return
            port_list.append(port)
    except ValueError:
        print("Invalid input. Please enter numeric values for ports.")
        return

    # Use ThreadPoolExecutor to scan ports concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        future_to_port = {executor.submit(scan_port, target, port): port for port in port_list}
        for future in concurrent.futures.as_completed(future_to_port):
            port, is_open = future.result()
            if is_open:
                print(f"Port {port} is open")
            else:
                print(f"Port {port} is closed")

# Main loop to scan multiple targets
while True:
    target = input("Enter the target IP address (IPv4 or IPv6) or 'q' to quit: ")
    if target.lower() == 'q':
        break

    ports_input = input("Enter the port numbers separated by commas (e.g., 80, 443, 8080): ")

    try:
        scan_target(target, ports_input)
    except KeyboardInterrupt:
        print("\nExiting Program !!!!")
        break
    except socket.gaierror:
        print("\nHostname Could Not Be Resolved !!!!")
        continue
    except socket.error:
        print("\nServer not responding !!!!")
        continue
