"""
Port Scanner - Core scanning logic
Usage: python scanner.py
"""

import socket
import concurrent.futures

# Common ports and their service names
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    8080: "HTTP-Alt",
}


def scan_port(host: str, port: int) -> bool:
    """
    Check if a single port is open on the given host.
    Returns True if open, False if closed or filtered.
    """
    try:
        s = socket.create_connection((host, port), timeout=1)
        s.close()
        return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        return False


def get_banner(host: str, port: int) -> str:
    """
    Attempt to grab the service banner from an open port.
    Returns the banner string or empty string if unavailable.
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host, port))
        s.send(b"HEAD / HTTP/1.0\r\n\r\n")  # basic HTTP probe
        banner = s.recv(1024).decode("utf-8", errors="ignore").strip()
        s.close()
        return banner.split("\n")[0]  # return just the first line
    except Exception:
        return ""


def get_service_name(port: int) -> str:
    """Return a human-readable service name for known ports."""
    return COMMON_PORTS.get(port, "Unknown")


def scan_range(host: str, start: int, end: int) -> list:
    """
    Sequentially scan a range of ports on the given host.
    Returns a list of dicts for open ports.

    NOTE: This is intentionally simple for hour 1-2.
    We will replace this with a threaded version in hour 3.
    """
    open_ports = []

    print(f"\nScanning {host} from port {start} to {end}...")
    print("-" * 50)

    for port in range(start, end + 1):
        if scan_port(host, port):
            service = get_service_name(port)
            banner = get_banner(host, port)
            open_ports.append({
                "port": port,
                "service": service,
                "banner": banner,
            })
            # Print immediately so you see results as they come in
            print(f"[OPEN] Port {port:<6} | {service:<15} | {banner[:40]}")

    return open_ports
def Scan_range_threaded( host : str, start : int, end : int) -> list:
    with concurrent.futures.ThreadPoolExecutor(max_workers = 5) as executor:
        results = list(executor.map(scan_port, [host] *(len(range(start, end+1))), range(start, end + 1)))
        combined = list(zip(results, range(start, end + 1)))
        opens = []
        for val in combined: 
            if (val[0]):
                opens.append(val)
                print(f'[Open] Port {val[1]}')
        return opens
def print_summary(open_ports: list) -> None:
    """Print a clean summary of scan results."""
    print("-" * 50)
    if not open_ports:
        print("No open ports found.")
    else:
        print(f"Found {len(open_ports)} open port(s).")


# --- Hour 1 goal: get this running on localhost ---
if __name__ == "__main__":
    HOST = "127.0.0.1"  # localhost - always safe to scan
    START_PORT = 1
    END_PORT = 10000

    results = Scan_range_threaded(HOST, START_PORT, END_PORT)
    print_summary(results)