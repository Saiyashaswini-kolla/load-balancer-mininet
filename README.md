# Load Balancer Simulation with Mininet

A software-defined networking (SDN) simulation of a load balancer built using **Mininet**, supporting 6 different load balancing algorithms. The system routes client HTTP requests across multiple backend servers and benchmarks performance under varying concurrent loads.

---

## Architecture

```
Client (10.0.0.1)
     |
    sw1 ──────────────── s1 (10.0.0.3)
     |  \                s2 (10.0.0.4)
     |   \               s3 (10.0.0.5)
     |    \              s4 (10.0.0.6)
     |    sw3
     |     |
     |    lb (10.0.0.2)  ← Load Balancer
     |
    sw2 ──────────────── s5 (10.0.0.7)
                         s6 (10.0.0.8)
                         s7 (10.0.0.9)
                         s8 (10.0.0.10)
```

- **1 Client**, **1 Load Balancer**, **3 Switches**, **8 Backend Servers**
- All servers expose a key-value HTTP store on port `8000`
- Load balancer listens on port `8888`

---

## Features

- Custom Mininet topology defined in `topo.py`
- 6 load balancing algorithms in `load_balancer.py`
- HTTP key-value store server with `GET`, `PUT`, `DELETE` support
- Multi-threaded client simulation (1–50 concurrent clients)
- Response time logging and benchmarking

---

## Load Balancing Algorithms

| Algorithm | Description |
|---|---|
| `round-robin` | Cycles through servers sequentially |
| `weighted-round-robin` | Distributes load based on server weights |
| `random` | Randomly selects a backend server |
| `ip-hash` | Routes same client IP consistently to the same server |
| `least-connection` | Routes to the server with fewest active connections |
| `weighted-least-connection` | Combines server weights with connection counts |

To switch algorithms, edit the `algorithm` parameter in `load_balancer.py`:
```python
load_balancer = LoadBalancer(server_addresses=backend_servers, algorithm="round-robin")
```

---

## File Structure

```
load-balancer-mininet/
├── topo.py            # Mininet topology definition
├── load_balancer.py   # Load balancer with 6 algorithms
├── server.py          # Backend HTTP key-value server
├── client.py          # Client with multi-threaded requests
├── simulate.py        # Benchmarking script (1–50 clients)
├── logs/              # Log output directory (auto-created)
└── random/            # Benchmark results directory (auto-created)
```

---

## Requirements

- Python 3
- [Mininet](http://mininet.org/download/)

---

## How to Run

### 1. Start the Mininet topology
```bash
sudo mn --custom topo.py --topo loadbalancer --mac
```

### 2. Start backend servers (run on each server node)
```bash
# In Mininet CLI, open xterm for each server
xterm s1 s2 s3 s4 s5 s6 s7 s8

# On each server terminal
python3 server.py <server_ip>
# e.g., on s1: python3 server.py 10.0.0.3
```

### 3. Start the load balancer (run on lb node)
```bash
xterm lb
python3 load_balancer.py
```

### 4. Run the client (run on client node)
```bash
xterm client
python3 client.py
```

### 5. Run the benchmark simulation
```bash
python3 simulate.py
# Simulates 1 to 50 concurrent clients and logs average response times
```

---

## HTTP API

The backend servers support a simple key-value store over HTTP:

| Method | URL Format | Description |
|---|---|---|
| `GET` | `/assignment2?request=<key>` | Retrieve value by key |
| `PUT` | `/assignment2/<key>/<value>` | Insert or update a key-value pair |
| `DELETE` | `/assignment2/<key>` | Delete a key |

---

## Benchmark

`simulate.py` runs 1 to 50 concurrent client threads, each sending a GET request, and records the **average response time** per concurrency level. Results are saved to `random/response_times_3.txt` and logged to `logs/all_logs.txt`.

---

## Changing Number of Backend Servers

The load balancer supports N = 3, 5, or 7 servers. Uncomment the relevant line in `load_balancer.py`:

```python
# N = 3
backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000), ("10.0.0.7", 8000)]

# N = 5
# backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000), ("10.0.0.7", 8000), ("10.0.0.8", 8000), ("10.0.0.9", 8000)]

# N = 7
# backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000), ("10.0.0.5", 8000), ("10.0.0.6", 8000), ("10.0.0.7", 8000), ("10.0.0.8", 8000), ("10.0.0.9", 8000)]
```
