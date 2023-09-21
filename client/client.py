import tkinter as tk
import socket
import threading
import argparse

# Create an argument parser to specify server IP and port
parser = argparse.ArgumentParser(description="Concussion C2 Client")
parser.add_argument('--server-ip', default='127.0.0.1', help="Server IP")
parser.add_argument('--server-port', type=int, default=2222, help="Server port")
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

def update_connection_status(status):
    connection_status_label.config(text=f"Connection Status: {status}")

# Function to handle the send command button click
def send_command():
    try:
        command = command_var.get()
        if command:
            if command.startswith("redirect"):
                # Handle a redirect command
                redirect_command, target_ip, target_port = command.split(' ')
                handle_redirect(target_ip, int(target_port))
                update_status(f"Redirected to {target_ip}:{target_port}.")
            else:
                send_request(command)

            # Update connection status
            update_connection_status("Connected to Server")

    except ConnectionRefusedError:
        update_status("Connection refused. Ensure the server is running and the IP/port are correct.")
        update_connection_status("Connection Refused")

    except Exception as e:
        print(f"Error: {e}")
        update_status(f"Error: {e}")
        update_connection_status("Error Occurred")

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

        # Update connection status when successfully connected
        update_connection_status("Connected to Server")

    except Exception as e:
        print(f"Error: {e}")
        update_status(f"Error: {e}")
        update_connection_status("Error Occurred")

# Add Labels and Headings (unchanged)
main_heading = tk.Label(root, text="Concussion C2 Client", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
main_heading.pack(pady=(20, 10))

# Create a label for the server connection status
status_label = tk.Label(root, text="Connection Status: Not Connected", font=("Helvetica", 16, "bold"), bg="#000046", fg="#41E67B")
status_label.pack(padx=10, pady=10)

# Create a label for the response
response_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#000046", fg="#00C8FF")
response_label.pack(padx=10, pady=10)

# Enhance Button Styling (unchanged)
send_button = tk.Button(root, text="Send Command",font=("Helvetica", 16, "bold"), bg="#00FFEA", fg="#0000A2", command=send_command)
send_button.pack()

# Run the GUI application
root.mainloop()
