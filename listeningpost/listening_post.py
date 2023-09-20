import tkinter as tk
import socket
import threading
import argparse

# Create an argument parser to specify listening post IP and port
parser = argparse.ArgumentParser(description="Concussion C2 Listening Post")
parser.add_argument('--listening-ip', default='0.0.0.0', help="Listening Post IP")
parser.add_argument('--listening-port', type=int, default=8081, help="Listening Post port")
args = parser.parse_args()

# Define the IP address and port for the listening post
LISTENING_IP = args.listening_ip
LISTENING_PORT = args.listening_port

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Listening Post")
root.geometry("400x300")  # Adjust the window size as needed

# Define the common color scheme
root.configure(bg="#000046")
# Define the common color scheme
#primary_color = "#000046"
#secondary_color = "#41E67B"
#background_color = "#000046"
#text_color = "#00c8ff"

# Create a variable to store the current redirection target
current_redirect_target = None

# Function to start listening (placeholder for the actual logic)
def start_listening():
    global current_redirect_target
    if redirect_target:
        current_redirect_target = redirect_target
        status_label.config(text=f"Listening Post Status: Redirected to {redirect_target[0]}:{redirect_target[1]}")
    else:
        status_label.config(text="Listening Post Status: Listening")

# Add Labels and Headings
main_heading = tk.Label(root, text="Concussion C2 Listening Post", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
main_heading.pack(pady=(20, 10))

# Create a label for the listening post status
status_label = tk.Label(root, text="Listening Post Status: Not Listening", font=("Helvetica", 16, "bold"), bg="#000046", fg="#41E67B")
status_label.pack(pady=10)

# Enhance Button Styling
start_button = tk.Button(root, text="Start Listening", font=("Helvetica", 14, "bold"), bg="#0000A2", fg="#00FFEA", command=start_listening)
start_button.pack()

# ... (Other GUI code)

# Run the GUI application
root.mainloop()

