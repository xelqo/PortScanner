# Multithreaded TCP Port Scanner

A fast, multithreaded TCP port scanner built in Python. Uses `ThreadPoolExecutor` to scan ports concurrently,
leveraging I/O-bound concurrency to scan thousands of ports significantly faster than sequential scanning.

## Features

- **Multithreaded scanning** using `concurrent.futures.ThreadPoolExecutor`
- **Service banner grabbing** to identify running services on open ports
- **Common port name mapping** (SSH, HTTP, FTP, MySQL, etc.)
- **CLI interface** via `argparse` for flexible usage

## Requirements

- Python 3.7+
- No external libraries required (standard library only)

## Usage

```bash
python scanner.py <host> <start_port> <end_port>
```

### Examples

Scan localhost ports 1 through 1024:
```bash
python scanner.py 127.0.0.1 1 1024
```

Scan a broader range:
```bash
python scanner.py 127.0.0.1 1 9999
```

Scan a public practice host:
```bash
python scanner.py scanme.nmap.org 1 1024
```

### Example Output

```
[Open] Port 22
[Open] Port 80
[Open] Port 8080
--------------------------------------------------
Found 3 open port(s).
```

## How It Works

1. **Argument parsing** — accepts host, start port, and end port via CLI
2. **Concurrent scanning** — `ThreadPoolExecutor` dispatches `scan_port()` calls simultaneously across the port range
3. **I/O-bound concurrency** — threads release the GIL during network wait time, making concurrent scanning significantly faster than sequential
4. **Result matching** — `zip()` pairs boolean scan results back to their port numbers
5. **Banner grabbing** — attempts to read service banners from open ports via HTTP probe

## Technical Notes

- Uses `socket.create_connection()` for cross-platform compatibility
- Timeout set to 1 second per port to balance speed and accuracy
- Threading is effective here because port scanning is I/O-bound — threads spend most of their time waiting on network responses, not executing Python code

## Ethical Use

**Only scan hosts you own or have explicit permission to scan.** Unauthorized port scanning may be illegal in your jurisdiction.
This tool is intended for educational purposes and authorized security testing only.

## Author

Alex Tsai  
github.com/xelqo
