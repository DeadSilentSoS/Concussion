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

# Define the common color scheme
primary_color = "#000046"
secondary_color = "#41E67B"
background_color = "#000046"
text_color = "#00c8ff"

root.configure(bg=background_color)

def start_listening():
    print("listening logic goes here...")

# Add Labels and Headings
main_heading = tk.Label(root, text="Concussion C2 Listening Post", font=("Helvetica", 16, "bold"), bg=primary_color, fg=text_color)
main_heading.pack(pady=(20, 10))

# Create a label for the listening post status
status_label = tk.Label(root, text="Listening Post Status: Not Listening", bg=background_color)
status_label.pack(pady=10)

# Enhance Button Styling
start_button = tk.Button(root, text="Start Listening", bg=secondary_color, fg=text_color, command=start_listening)
start_button.pack()

# ... (Other GUI code)

# Run the GUI application
root.mainloop()

