import socket
import threading
import time
import logging

# Configure logging
logging.basicConfig(filename='./logs/all_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def request_generator(request_type="GET",*args):
    ''' This function takes request_type and args as arguments where request_type tells whether request is 
    PUT/DELETE/GET and args are corresponding keys (or) values needed for those requests'''
    if(request_type=="GET"):
        return r"GET /assignment2?request="+args[0]+r" HTTP/1.1"+"\r\n\r\n"

    elif(request_type=="PUT"):
        return r"PUT /assignment2/"+args[0]+r"/"+args[1]+r" HTTP/1.1"+"\r\n\r\n"

    elif(request_type=="DELETE"):
        return r"DELETE /assignment2/"+args[0]+r" HTTP/1.1"+"\r\n\r\n"

    else:
        return None

def send_request(client_port, request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.0.0.2', client_port))

    start_time = time.time()  # Record the start time

    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()
    end_time = time.time()  # Record the end time
    client_socket.close()

    # Calculate and print the response time
    response_time = end_time - start_time
    print("Request took " + str(response_time) + "seconds")
    logging.info("Request took "+str(response_time)+"seconds")
    return response, response_time

def simulate_client(client_port, requests, total_response_time):

    for request in requests:
        response, response_time = send_request(client_port, request)
        print("Received response: ", response.strip())
        # Update the total response time
        total_response_time[0] += float(response_time)

    # Calculate and log the average response time for the client
    print("Received response: ", response.strip())



if __name__ == "__main__":
    client_port = 8888
    total_response_time = [0]

    with open('./random/response_times_3.txt','w+') as f:
        for Num_clients in range(1,51):
            total_response_time = [0]
            threads = []
            for i in range(Num_clients):
                requests_list= []
                request=  request_generator("GET","key1")
                requests_list.append(request)
                thread = threading.Thread(target=simulate_client, args=(client_port, requests_list, total_response_time), name="Client"+str(i+1))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

            average_response_time = total_response_time[0] / Num_clients
            f.write(str(average_response_time)+'\n')
            logging.info("Average response time: " + str(average_response_time)+ "seconds")
