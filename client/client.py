import tkinter as tk
import socket
import threading
import json

# Define the server's IP address and port
SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Client")
root.geometry("400x300")  # Adjust the window size as needed

# 1. Use a Consistent Color Scheme
primary_color = "#000098"
secondary_color = "#2ecc71"
background_color = "#000080"
text_color = "#ffffff"

root.configure(bg=background_color)

# 2. Add Labels and Headings
main_heading = tk.Label(root, text="Concussion C2 Client", font=("Helvetica", 16, "bold"), bg=primary_color, fg=text_color)
main_heading.pack(pady=(20, 10))

# Create a label for the server connection status
status_label = tk.Label(root, text="Server Status: Not Connected", bg=background_color)
status_label.pack(pady=10)

# Create an entry field for user input
command_var = tk.StringVar()  # Create a StringVar to hold the entry text
command_var.set("Enter your command")  # Set the default text
command_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#ffffff", textvariable=command_var)
command_entry.pack()

# Function to send a command to the server
def send_command():
    command = command_var.get()
    if command and command != "Enter your command":
        try:
            # Create a socket and establish a connection to the server
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((SERVER_IP, SERVER_PORT))

            # Define a command dictionary with a "type" and "data" field
            command_data = {"type": "command", "data": command}
            # Serialize the command as JSON and send it to the server
            client_socket.send(json.dumps(command_data).encode('utf-8'))

            # Receive and process the response from the server
            response_data = client_socket.recv(1024).decode('utf-8')
            response = json.loads(response_data)
            
            if response["type"] == "response":
                # Process the response as needed (e.g., display it)
                status_label.config(text=f"Server Status: Response - {response['data']}")
            else:
                status_label.config(text="Server Status: Invalid Response")

            # Close the client socket
            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")

            # Handle connection or other errors gracefully
            status_label.config(text=f"Server Status: Error - {e}")

            # Close the client socket if an error occurs
            client_socket.close()

            # Optionally, you can log the error for debugging

# 3. Improve Button Styling
send_button = tk.Button(root, text="Send Command", bg=secondary_color, fg=text_color, command=send_command)
send_button.pack()

# ... (Other GUI code)

# Run the GUI application
root.mainloop()
