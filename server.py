import socket
import threading
import json
import os
import sys

def load_data(path="file.json"):
    '''Check whether file exists and returns its content in form of dictionary'''
    if os.path.exists(path):
        with open(path, "r") as f:
            data = json.load(f)
        return data
    else:
        return {}

def save_data(data,path="file.json"):
    '''Takes data which is dictionary object and writes it into given json file'''
    with open(path, "w") as f:
        json.dump(data, f)

def get_response(request):
    '''Takes request string, parses it and send appropriate response to client'''
    splitted = request.split(" ")
    request_type = splitted[0]
    res = "HTTP/1.1 400 Bad Request\r\n\r\n"
    if(request_type == "GET"):
        if("request=" in request):
            # check whether HTTP request has request="" format
            split_by_request_keyword = request.split("request=")[1]
            key = split_by_request_keyword.split(" ")[0]
            dict = load_data()
            if(key in dict.keys()):
                res = "HTTP/1.1 200 OK "+dict[key]+"\r\n\r\n"
            else:
                res = "HTTP/1.1 404 Not Found\r\n\r\n"
            return res
    elif(request_type == "PUT"):
        try:
            key, value = splitted[1][13:].split("/")
            dict = load_data()
            dict[key] = value
            save_data(dict)
            # print("Added key-val pair...")
            res = "HTTP/1.1 200 OK\r\n\r\n"
            return res
        except Exception as e:
            print("Exception : ",e)
            return res
    elif(request_type == "DELETE"):
        try:
            key = splitted[1][13:]
            dict = load_data()
            if(key in dict.keys()):
                del dict[key]
                save_data(dict)
                # print("Deleted key-val pair...")
                res = "HTTP/1.1 200 OK\r\n\r\n"
                return res
            else:
                res = "HTTP/1.1 404 Not Found\r\n\r\n"
                return res
        except Exception as e:
            return res
    else:
        print("Request :", request)
        return res

class Server:
    def __init__(self, server_address):
        self.server_address = server_address

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(self.server_address)
        server_socket.listen(5)

        print("Server listening on ",self.server_address)

        while True:
            client_socket, _ = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket,)).start()

    def handle_client(self, client_socket):
        data = client_socket.recv(1024).decode()
        print("Received request: ",data.strip())

        response = get_response(data)
        client_socket.sendall(response.encode())
        client_socket.close()

if __name__ == "__main__":
    _,addr = sys.argv 
    server_address = (str(addr),8000) 
    server = Server(server_address)
    server.start()
