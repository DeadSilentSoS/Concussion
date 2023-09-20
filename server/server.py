import socket
import threading
import tkinter as tk

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 1234

# Create a GUI window using Tkinter
root = tk.Tk()
root.title("Concussion")
root.geometry("700x500")

# Define the common color scheme
root.configure(bg="#000046")

# Define a variable to store the redirect target
redirect_target = None

server_socket = None  # Initialize the server socket variable
accept_thread = None  # Initialize the accept_thread variable
server_started = False  # Variable to track whether the server is running or not

def initialize_server():
    global server_socket
    global HOST, PORT  # Define HOST and PORT as global variables
    HOST = '127.0.0.1'  # Set the desired IP address
    PORT = 8080  # Set the desired port
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"Server is listening on {HOST}:{PORT}")

def start_server():
    global server_socket, accept_thread, server_started
    if server_socket is None:
        initialize_server()  # Call the initialization function
        accept_thread = threading.Thread(target=accept_connections)
        accept_thread.start()  # Start accepting connections
        server_started = True  # Update the server status

def stop_server():
    global server_socket, server_started
    if server_socket is not None:
        server_socket.close()
        server_socket = None
        server_started = False  # Update the server status
        update_status("Server stopped.")
    # ... Add any cleanup code here ...

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

# Function to handle a redirect command
def handle_redirect(target_ip, target_port):
    global redirect_target
    redirect_target = (target_ip, target_port)

# Function to update the text widget with server status and messages
def update_status(message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Auto-scroll to the end

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
start_button = tk.Button(button_frame, text="Start Server", font=("Helvetica", 14, "bold"), fg="#0000A2", bg="#00FFEA")
start_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')

# Stop server button
stop_button = tk.Button(button_frame, text="Stop Server", font=("Helvetica", 14, "bold"), fg="#000000", bg="#FF0000")
stop_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill='both')

# Command input field and send button
input_frame = tk.Frame(root, bg="#000046")
input_frame.pack(fill=tk.BOTH, padx=10, pady=10)

# Command input field
command_entry = tk.Entry(input_frame, font=("Helvetica", 12), bg="#000017", fg="#0296FF")
command_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

# Send command button
send_button = tk.Button(input_frame, text="Send Command", font=("Helvetica", 12, "bold"), fg="#00002E", bg="#00C8FF")
send_button.pack(side=tk.LEFT, padx=10, pady=10)

# Text widget for display window
text_widget = tk.Text(root, height=15, width=50, fg="#0295FF", bg="#000046")
text_widget.pack(fill=tk.BOTH, padx=10, pady=10)

# Function to update the text widget with server status and messages
def update_status(message):
    text_widget.insert(tk.END, message + "\n")
    text_widget.see(tk.END)  # Auto-scroll to the end

# Accept incoming connections and start a thread to handle each client
def accept_connections():
    while True:  # Always run to accept connections
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
