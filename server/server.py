import socket
import threading
import tkinter as tk

# Define the server's IP address and port
HOST = '127.0.0.1'
PORT = 8080

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

# Create a GUI window using Tkinter
root = tk.Tk()
root.title("Server GUI")

# Create a text widget to display server status and client messages
text_widget = tk.Text(root, height=15, width=50)
text_widget.pack()

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

