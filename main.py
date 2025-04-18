import yaml
import requests
import time
import threading
from collections import defaultdict
from datetime import datetime

# Function to load configuration from the YAML file
def load_config(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

# Function to perform health checks
def check_health(endpoint):
    url = endpoint['url']
    method = endpoint.get('method', 'GET').upper()
    headers = endpoint.get('headers')
    body = endpoint.get('body')

    try:
        response = requests.request(method, url, headers=headers, json=body, timeout=5)
        latency = response.elapsed.total_seconds() * 1000
        if (200 <= response.status_code < 300) and (latency <= 500):  # if latency is greater than 500ms also reject it.
            return "UP"
        else:
            return "DOWN"
    except requests.RequestException:
        return "DOWN"

# Function to check a single endpoint and update stats
def check_endpoint(endpoint, domain_stats, lock):
    domain = endpoint["url"].split("//")[-1].split("/")[0].split(":")[0]  # Split to remove the port number from domain
    result = check_health(endpoint)
    
    with lock:
        domain_stats[domain]["total"] += 1
        if result == "UP":
            domain_stats[domain]["up"] += 1

# Run healthchecks in parallel to meet 15 second max requirement
def run_health_checks(config, domain_stats, lock):
    threads = []
    for endpoint in config:
        thread = threading.Thread(target=check_endpoint, args=(endpoint, domain_stats, lock))
        thread.start()
        threads.append(thread)
    

# Function to log results
def log_results(domain_stats, lock):
    with lock:
        print(f"\n--- {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
        for domain, stats in domain_stats.items():
            if stats["total"] > 0: 
                availability = round(100 * stats["up"] / stats["total"]) #The availability declaration already drops the decimal point, no modification necessary. This was specifically called out in PDF to add a comment so here it is
                print(f"{domain} has {availability}% availability percentage")

# Main function to monitor endpoints
def monitor_endpoints(file_path):
    config = load_config(file_path)
    domain_stats = defaultdict(lambda: {"up": 0, "total": 0})
    lock = threading.Lock()  # Create a lock for thread
    
    try:
        while True:
            cycle_start_time = time.time()
            
            run_health_checks(config, domain_stats, lock) #Start threaded health checks
            
            # Log results
            log_results(domain_stats, lock)
            
            # Calculate time to wait
            elapsed_time = time.time() - cycle_start_time
            sleep_time = max(0, 15 - elapsed_time)
            
            time.sleep(sleep_time)
            
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")

# Entry point of the program
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python monitor.py <config_file_path>")
        sys.exit(1)

    config_file = sys.argv[1]
    try:
        monitor_endpoints(config_file)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")