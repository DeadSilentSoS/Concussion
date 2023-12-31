import socket
import threading
import tkinter as tk
import time
import logging

# Configure the logging settings
logging.basicConfig(filename='server_logs.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 2222

# Create a GUI window using Tkinter
root = tk.Tk()
root.title("Concussion")
root.geometry("700x500")

# Define the common color scheme
root.configure(bg="#000046")

# Example usage:
logging.info('Server started')
logging.error('An error occurred')

server_socket = None # Initialize the server socket variable
accept_thread = None # Initialize the accept_thread variable
server_started = False # Variable to track whether the server is running or not

# Create a list to keep track of connected clients
connected_clients = []

# Create a listbox widget to display connected clients
client_listbox = tk.Listbox(root, selectmode=tk.SINGLE)  # Example listbox creation
client_listbox.pack(side=tk.LEFT, padx=10, pady=10)

# Function to add a client to the client listbox
def add_client_to_listbox(client_socket):
    client_address = client_socket.getpeername()
    connected_clients.append(client_socket)
    client_listbox.insert(tk.END, f"{client_address[0]}:{client_address[1]}")

# Function to remove a client from the client listbox
def remove_client_from_listbox(client_socket):
    client_address = client_socket.getpeername()
    connected_clients.remove(client_socket)
    client_listbox.delete(0, tk.END)  # Clear the listbox
    for client in connected_clients:
        address = client.getpeername()
        client_listbox.insert(tk.END, f"{address[0]}:{address[1]}")

# Function to handle a client's connection
def handle_client(client_socket, client_address):
    # Add the client to the list of connected clients
    add_client_to_listbox(client_socket)

# Function to update the text widget with server status and messages
def update_status(message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Auto-scroll to the end

# Function to send a command to a selected client
def send_command_to_client():
    selected_client = client_listbox.get(tk.ACTIVE)
    if selected_client:
        command = command_entry.get()
        if command:
            try:
                selected_client.send(command.encode('utf-8'))
                update_status(f"Sent command to {selected_client.getpeername()}: {command}")
            except Exception as e:
                update_status(f"Error sending command: {e}")

# Function to initialize the server socket
def initialize_server():
    global server_socket
    global HOST, PORT  # Define HOST and PORT as global variables
    HOST = '127.0.0.1'  # Set the desired IP address
    PORT = 2222  # Set the desired port

    while True:
        try:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            debug_message = f"Server is listening on {HOST}:{PORT}"

            # Log the debug message
            logging.info(debug_message)

            # Update the text widget with the debug message
            update_status(debug_message)  # Update the server's GUI display
            debug_text_widget.insert(tk.END, debug_message + "\n")
            debug_text_widget.see(tk.END)  # Scroll to the end of the text widget

            break  # Break out of the loop if binding is successful
        except OSError as e:
            if e.errno == 98:  # Address already in use error
                debug_message = f"Port {PORT} is already in use. Waiting..."
                update_status(debug_message)  # Update the server's GUI display
                time.sleep(5)  # Wait for 5 seconds before retrying
            else:
                raise e  # Raise other OSError exceptions

# Function to start the server
def start_server():
    global server_socket, accept_thread, server_started
    if server_socket is None:
        initialize_server()  # Call the initialization function
        accept_thread = threading.Thread(target=accept_connections)
        accept_thread.start()  # Start accepting connections
        server_started = True  # Update the server status

        # Update the connection status label
        server_status.config(text="Server Status: Running")

# Function to stop the server
def stop_server():
    global server_socket, server_started
    if server_socket is not None:
        server_socket.close()
        server_socket = None
        server_started = False  # Update the server status

        # Update the connection status label
        server_status.config(text="Server Status: Stopped")
        update_status("Server stopped.")
    else:
        update_status("Server is not running.")

# Function to handle a redirect command
def handle_redirect(target_ip, target_port):
    global redirect_target
    redirect_target = (target_ip, target_port)

# Function to update the text widget with server status and messages
def update_status(message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Auto-scroll to the end

# Function to handle a client's connection
def handle_client(client_socket, client_address):
    # Add the client to the list of connected clients
    connected_clients.append(client_socket)
    client_listbox.insert(tk.END, client_socket)

    # Continuously listen for commands from the client
    while server_started:
        try:
            command = client_socket.recv(1024).decode('utf-8')
            if not command:
                break  # If no data received, the client might have disconnected

            # Execute the command and get the output
            # Implement your command execution logic here
            # For example:
            # result = execute_command(command)
            # client_socket.send(result.encode('utf-8'))
        except Exception as e:
            print(f"Error receiving command from {client_address}: {e}")
            break

    # Remove the client from the list of connected clients and close the socket
    client_listbox.delete(tk.ACTIVE)
    connected_clients.remove(client_socket)
    client_socket.close()

# Create a frame for server title and status
title_frame = tk.Frame(root, bg="#000046")
title_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Server title
server_title = tk.Label(title_frame, text="Concussion", font=("Helvetica", 24, "bold"), fg="#00c8ff", bg="#000046")
server_title.pack()

# Server status text
server_status = tk.Label(root, text="Server Status: Not Running", font=("Helvetica", 16, "bold"), fg="#41E67B", bg="#000046")
server_status.pack(padx=10, pady=10)

# Frame for start and stop buttons
button_frame = tk.Frame(root, bg="#000046")
button_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Start server button
start_button = tk.Button(button_frame, text="Start Server", font=("Helvetica", 14, "bold"), fg="#004D02", bg="#00F517", command=start_server)
start_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')

# Stop server button
stop_button = tk.Button(button_frame, text="Stop Server", font=("Helvetica", 14, "bold"), fg="#000000", bg="#FF0000", command=stop_server)
stop_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')

# Create a frame for command input and sending
input_frame = tk.Frame(root, bg="#000046")
input_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Entry field for commands to be sent
command_entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="#000017", fg="#0296FF")
command_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Send command button
send_button = tk.Button(input_frame, text="Send Command", font=("Helvetica", 12, "bold"), fg="#00002E", bg="#00C8FF", command=send_command_to_client)
send_button.pack(side=tk.LEFT, padx=10, pady=10)

# Text widget for displaying server status and messages
text_widget = tk.Text(root, height=15, width=50, fg="#0295FF", bg="#000046")
text_widget.pack(fill=tk.BOTH, padx=10, pady=10)

# Create a text widget for displaying debug messages
debug_text_widget = tk.Text(root, height=10, width=50, fg="#FFFFFF", bg="#000046")
debug_text_widget.pack(fill=tk.BOTH, padx=10, pady=10)

# Accept incoming connections and start a thread to handle each client
def accept_connections():
    while server_started:  # Only run if the server has been started
        try:
            client_socket, client_address = server_socket.accept()
            print(f"Connected to client at {client_address}")
            update_status(f"Connected to client at {client_address}")

            # Create a thread to handle the client
            client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_thread.start()
        except KeyboardInterrupt:
            update_status("Server is shutting down.")
            break
        except Exception as e:
            update_status(f"Error: {e}")

# Start accepting connections in a separate thread
accept_thread = threading.Thread(target=accept_connections)
accept_thread.start()

# Start the Tkinter main loop
root.mainloop()

# Close the server socket (this will happen when you close the GUI window)
if server_socket is not None:
    server_socket.close()
