import socket
import threading
import random

class LoadBalancer:
    def __init__(self, server_addresses, algorithm):
        self.server_addresses = server_addresses
        self.algorithm = algorithm
        self.current_index = 0
        self.weights = [0.4,0.4,0.2]
        # for N = 3 weights = [0.4,0.4,0.2]
        # for N = 5 weights = [0.25,0.25,0.15,0.15,0.2]
        # for N = 7 weights = [0.15,0.15,0.15,0.15,0.2,0.1,0.1]
        self.connection_count = [0] * len(server_addresses)  # For least connection algorithm
        self.response_times = [0] * len(server_addresses)  # For least response time algorithm
        self.lock = threading.Lock()

    def start(self, host, port):
        balancer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        balancer_socket.bind((host, port))
        balancer_socket.listen(5)
        print("Load Balancer is running on", host, port)

        while True:
            client_socket, client_address = balancer_socket.accept()
            print("Received connection from", client_address)

            # Choose the backend server using the specified algorithm
            with self.lock:
                backend_address = self.choose_backend(client_address[0])  # Pass client IP for IP hash

            # Update connection count
            with self.lock:
                self.connection_count[self.server_addresses.index(backend_address)] += 1

            # Forward the connection to the selected backend server
            threading.Thread(target=self.forward, args=(client_socket, backend_address)).start()

    def choose_backend(self, client_ip):
        if self.algorithm == "round-robin":
            backend_address = self.server_addresses[self.current_index]
            self.current_index = (self.current_index + 1) % len(self.server_addresses)
            return backend_address
        elif self.algorithm == "weighted-round-robin":
            backend_address = self.weighted_round_robin()
            return backend_address
        elif self.algorithm == "random":
            backend_address = random.choice(self.server_addresses)
            return backend_address
        elif self.algorithm == "ip-hash":
            hash_value = hash(client_ip) % len(self.server_addresses)
            return self.server_addresses[hash_value]
        elif self.algorithm == "least-connection":
            backend_address = self.least_connection()
            return backend_address
        elif self.algorithm == "weighted-least-connection":
            backend_address = self.weighted_least_connection()
            return backend_address

    def weighted_round_robin(self):
        total_weight = sum(self.weights)
        selected_index = (self.current_index + 1) % len(self.server_addresses)
        while True:
            if self.weights[selected_index] >= random.uniform(0, total_weight):
                self.current_index = selected_index
                return self.server_addresses[self.current_index]
            selected_index = (selected_index + 1) % len(self.server_addresses)

    def least_connection(self):
        min_connections = min(self.connection_count)
        min_index = self.connection_count.index(min_connections)
        self.connection_count[min_index] += 1
        return self.server_addresses[min_index]

    def weighted_least_connection(self):
        total_weight = sum(self.weights)
        min_connections = min(self.connection_count)
        min_index = self.connection_count.index(min_connections)
        self.connection_count[min_index] += 1
        return self.server_addresses[min_index]

    def least_response_time(self):
        min_response_time = min(self.response_times)
        min_index = self.response_times.index(min_response_time)
        return self.server_addresses[min_index]

    def forward(self, client_socket, backend_address):
        backend_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        backend_socket.connect(backend_address)

        # Forward data from client to backend
        threading.Thread(target=self.forward_data, args=(client_socket, backend_socket)).start()

        # Forward data from backend to client
        self.forward_data(backend_socket, client_socket)

    def forward_data(self, source, destination):
        while True:
            data = source.recv(1024)
            if not data:
                break
            destination.sendall(data)

# backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000),("10.0.0.7", 8000)] for N = 3
# backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000),("10.0.0.7", 8000), ("10.0.0.8", 8000), ("10.0.0.9", 8000)] for N = 5
# backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000), ("10.0.0.5", 8000), ("10.0.0.6", 8000),("10.0.0.7", 8000), ("10.0.0.8", 8000), ("10.0.0.9", 8000)] for N = 7

if __name__ == "__main__":
    # Define the addresses of backend servers
    backend_servers = [("10.0.0.3", 8000), ("10.0.0.4", 8000),("10.0.0.7", 8000)] 
    # Create a load balancer with the desired algorithm
    load_balancer = LoadBalancer(server_addresses=backend_servers, algorithm="random")

    # Start the load balancer on a specific host and port
    load_balancer.start(host="10.0.0.2", port=8888)

