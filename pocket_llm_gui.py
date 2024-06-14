import tkinter as tk
from tkinter import scrolledtext
import webbrowser
import pyautogui
import configparser
import os
import pyperclip
import sys

# Function to save settings
def save_settings():
    config['Settings'] = {
        'delay': delay_var.get().rstrip('s'),  # Remove 's' before saving
        'port': port_var.get()
    }
    with open(config_file, 'w') as configfile:
        config.write(configfile)

# Function to load settings
def load_settings():
    if os.path.exists(config_file):
        config.read(config_file)
    # Set default values if not present in the config file
    if 'Settings' not in config or 'delay' not in config['Settings']:
        delay_var.set('1.5s')
    else:
        delay_var.set(f"{config.get('Settings', 'delay')}s")  # Add 's' when loading

    if 'Settings' not in config or 'port' not in config['Settings']:
        port_var.set('3000')
    else:
        port_var.set(config.get('Settings', 'port'))

# Function to send the text
def send_text():
    delay = float(delay_var.get().rstrip('s'))  # Strip 's' from the delay value
    port = port_var.get()
    input_text = input_textbox.get('1.0', tk.END).strip()
    
    # Open the default web browser and navigate to the URL
    webbrowser.open(f'http://localhost:{port}')

    # Wait for the browser to open and load the page
    root.after(int(delay * 1000), paste_text)

    # Save settings after sending text
    save_settings()

def paste_text():
    # Copy the text to the clipboard
    pyperclip.copy(input_textbox.get('1.0', tk.END).strip())

    # Paste the text into the focused input box
    if sys.platform == 'darwin':  # macOS
        print("Macos paste")
        pyautogui.keyDown('command')
        pyautogui.press('v')
        pyautogui.keyUp('command')
    else:  # Windows or Linux
        print("winpaste")
        pyautogui.keyDown('ctrl')
        pyautogui.press('v')
        pyautogui.keyUp('ctrl')

    # Press Enter to submit the form
    pyautogui.press('enter')
    exit(0)

# Function to increase delay
def increase_delay():
    delay = float(delay_var.get().rstrip('s'))  # Strip 's' from the delay value
    delay += 0.1
    delay_var.set(f"{delay:.1f}s")
    root.update_idletasks()  # Ensure the UI updates immediately

# Function to decrease delay
def decrease_delay():
    delay = float(delay_var.get().rstrip('s'))  # Strip 's' from the delay value
    if delay > 0.1:
        delay -= 0.1
        delay_var.set(f"{delay:.1f}s")
    root.update_idletasks()  # Ensure the UI updates immediately

def adjust_height(event):
    widget = event.widget
    # Calculate the number of visible lines, including wrapped lines
    visible_lines = max(3, widget.count("1.0", "end", "displaylines")[0])
    widget.configure(height=visible_lines)

def handle_keypress(event):
    if event.keysym == 'Return':
        if event.state & 0x0001:  # Shift key is pressed
            input_textbox.insert(tk.INSERT, '\n')
        else:
            send_text()
        return "break"  # Prevent the default handling of the key press

# Create main window
root = tk.Tk()
root.focus_set()
# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the window's width and height
window_width = root.winfo_width()
window_height = root.winfo_height()

# Calculate the x and y coordinates for the center of the screen
x = (screen_width/2) - 300
y = (screen_height/2) - 160

# Set the initial window position to the center of the screen
root.geometry(f'+{int(x)}+{int(y)}')

root.title("Pocket LLM-GUI")

config_file = 'settings.ini'
config = configparser.ConfigParser()
delay_var = tk.StringVar()
port_var = tk.StringVar()

load_settings()

# Create a frame to contain delay and port settings
settings_frame = tk.Frame(root)
settings_frame.grid(row=0, column=0, padx=5, pady=5, sticky='w')

# Create delay label and field
delay_label = tk.Label(settings_frame, text="Delay:")
delay_label.grid(row=0, column=0, padx=(0, 5), pady=5, sticky='w')

delay_entry = tk.Entry(settings_frame, textvariable=delay_var, width=10)
delay_entry.grid(row=0, column=1, padx=(0, 5), pady=5, sticky='w')

delay_up_button = tk.Button(settings_frame, text="↑", command=increase_delay, width=2)
delay_up_button.grid(row=0, column=2, padx=(0, 5))

delay_down_button = tk.Button(settings_frame, text="↓", command=decrease_delay, width=2)
delay_down_button.grid(row=0, column=3, padx=(0, 5))

# Create port label and field
port_label = tk.Label(settings_frame, text="Port:")
port_label.grid(row=0, column=4, padx=(30, 5), pady=5, sticky='w')

port_entry = tk.Entry(settings_frame, textvariable=port_var, width=10)
port_entry.grid(row=0, column=5, padx=(0, 5), pady=5, sticky='w')

# Create send button
send_button = tk.Button(root, text="Send", command=send_text)
send_button.grid(row=0, column=1, padx=5, pady=5, sticky='e')

# Create input text box
input_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=3)
input_textbox.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)


# Configure root for resizing
root.grid_rowconfigure(1, weight=1)  # Allow row 1 (containing input_textbox) to expand vertically
root.grid_columnconfigure(0, weight=1)  # Allow column 0 to expand horizontally
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.update_idletasks()

# Resize the window based on the initial content
input_textbox.bind("<Configure>", adjust_height)
input_textbox.bind("<KeyPress>", adjust_height)
input_textbox.bind("<Return>", handle_keypress)

# Set focus on input text box
input_textbox.focus_set()

# Run the application
root.mainloop()