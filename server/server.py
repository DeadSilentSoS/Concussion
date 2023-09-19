import socket
import threading
import tkinter as tk

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 8080

# Create a GUI window using Tkinter
root = tk.Tk()
root.title("Concussion")
root.geometry("700x500")
root.configure(bg="#000017")

# Create a socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((HOST, PORT))

# Start listening for incoming connections
server_socket.listen()

print(f"Server is listening on {HOST}:{PORT}")

# Function to handle individual client connections
def handle_client(client_socket, client_address):
    while True:
        try:
            # Receive data from the client
            data = client_socket.recv(1024)
            
            if not data:
                break

            # Process the received data (e.g., execute commands)
            # Add your logic here

            # Send a response back to the client
            response = "Response to the command"
            client_socket.send(response.encode('utf-8'))
        except Exception as e:
            print(f"Error: {e}")
            break

    # Close the client socket when disconnected
    client_socket.close()
    update_status(f"Client at {client_address} disconnected.")

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
start_button.pack(side=tk.LEFT, padx=10, pady=10)

# Stop server button
stop_button = tk.Button(button_frame, text="Stop Server", font=("Helvetica", 14, "bold"), fg="#000000", bg="#FF0000")
stop_button.pack(side=tk.LEFT, padx=10, pady=10)

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
    while True:
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
server_socket.close()
