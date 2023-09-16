import tkinter as tk
import socket
import threading

# Define the IP address and port for the listening post
LISTENING_IP = '0.0.0.0'
LISTENING_PORT = 8081

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Listening Post")
root.geometry("400x300")  # Adjust the window size as needed

# 1. Use a Consistent Color Scheme
primary_color = "#3498db"
secondary_color = "#2ecc71"
background_color = "#f2f2f2"
text_color = "#333333"

root.configure(bg=background_color)

def start_listening():
    print("listening logic goes here...")

# 2. Add Labels and Headings
main_heading = tk.Label(root, text="Concussion C2 Listening Post", font=("Helvetica", 16, "bold"), bg=primary_color, fg=text_color)
main_heading.pack(pady=(20, 10))

# Create a label for the listening post status
status_label = tk.Label(root, text="Listening Post Status: Not Listening", bg=background_color)
status_label.pack(pady=10)

# 3. Improve Button Styling
start_button = tk.Button(root, text="Start Listening", bg=secondary_color, fg=text_color, command=start_listening)
start_button.pack()

# Placeholder for the start_listening function
server_socket = None  # Store the server socket globally

def start_listening():
    global server_socket
    try:
        # Create a socket and start listening for incoming connections
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((LISTENING_IP, LISTENING_PORT))
        server_socket.listen()

        status_label.config(text=f"Listening Post Status: Listening on {LISTENING_IP}:{LISTENING_PORT}")

        # Start a thread to handle incoming connections
        threading.Thread(target=accept_connections).start()
    except Exception as e:
        status_label.config(text=f"Listening Post Status: Error - {e}")

# Function to accept incoming client connections
def accept_connections():
    while True:
        client_socket, client_address = server_socket.accept()
        status_label.config(text=f"Listening Post Status: Connected to {client_address}")
        # Handle the connection here, e.g., process incoming data, send responses

# Placeholder for the icon_button_event function
def icon_button_event():
    # Add code to handle the icon button click event
    pass

# 4. Enhance Entry Fields
command_entry = tk.Entry(root, width=40, font=("Helvetica", 12), bg="#ffffff")
command_entry.pack()

# 5. Incorporate Icons (Replace with your icon path)
icon_image = tk.PhotoImage(file="/home/noone/Desktop/Projects/Concussion/resources/icon.png")
icon_button = tk.Button(root, image=icon_image, text="Icon Button", compound="left", bg=primary_color, fg=text_color, command=icon_button_event)
icon_button.image = icon_image  # Store a reference to the image
icon_button.pack(pady=20)

# Run the GUI application
root.mainloop()
