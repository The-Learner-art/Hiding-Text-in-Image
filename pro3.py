import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image
import numpy as np

def text_to_binary(text):
    binary = ''.join(format(ord(char), '08b') for char in text)
    return binary

def binary_to_text(binary):
    text = ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
    return text

def xor_encrypt_decrypt(text, key):
    encrypted_decrypted = ''.join(chr(ord(char) ^ ord(key[i % len(key)])) for i, char in enumerate(text))
    return encrypted_decrypted

class CustomInputDialog(tk.Toplevel):
    def __init__(self, parent, title, prompt):
        super().__init__(parent)
        self.title(title)
        self.geometry("400x200")
        self.prompt = prompt
        self.result = None
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=self.prompt, font=("Helvetica", 12)).pack(pady=20)
        self.entry = tk.Entry(self, font=("Helvetica", 12))
        self.entry.pack(pady=10)
        self.entry.focus()
        
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="OK", command=self.on_ok, width=10, font=("Helvetica", 12)).pack(side="left", padx=10)
        tk.Button(button_frame, text="Cancel", command=self.on_cancel, width=10, font=("Helvetica", 12)).pack(side="right", padx=10)

    def on_ok(self):
        self.result = self.entry.get()
        self.destroy()

    def on_cancel(self):
        self.result = None
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result

class CustomMessageDialog(tk.Toplevel):
    def __init__(self, parent, title, message):
        super().__init__(parent)
        self.title(title)
        self.geometry("200x200")
        self.message = message
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self, text=self.message, font=("Helvetica", 12), wraplength=380).pack(pady=20)
        
        tk.Button(self, text="OK", command=self.on_ok, width=10, font=("Helvetica", 12)).pack(pady=10)

    def on_ok(self):
        self.destroy()

    def show(self):
        self.wait_window()

def show_info_message(title, message):
    info_dialog = CustomMessageDialog(root, title, message)
    info_dialog.show()

def show_error_message(title, message):
    error_dialog = CustomMessageDialog(root, title, message)
    error_dialog.show()

def encode_text_to_image(image_path, text, output_path, key):
    try:
        image = Image.open(image_path)
        image = image.convert('RGB')
        arr = np.array(image)
        
        # Add a signature to the text
        text_with_signature = "--SECRET--" + text
        encrypted_text = xor_encrypt_decrypt(text_with_signature, key)
        binary_text = text_to_binary(encrypted_text) + '1111111111111110'  # Add a delimiter at the end

        data_index = 0
        binary_text_length = len(binary_text)
        
        for values in arr:
            for value in values:
                for i in range(3):
                    if data_index < binary_text_length:
                        value[i] = int(format(value[i], '08b')[:-1] + binary_text[data_index], 2)
                        data_index += 1
                    if data_index >= binary_text_length:
                        break
            if data_index >= binary_text_length:
                break

        encoded_image = Image.fromarray(arr)
        encoded_image.save(output_path, 'PNG')
        show_info_message("Success", "Text successfully encoded into image.")
    except Exception as e:
        show_error_message("Error", str(e))

def decode_text_from_image(image_path, key):
    try:
        image = Image.open(image_path)
        image = image.convert('RGB')
        arr = np.array(image)

        binary_text = ''
        for values in arr:
            for value in values:
                for i in range(3):
                    binary_text += format(value[i], '08b')[-1]
                    if binary_text[-16:] == '1111111111111110':  # Check for delimiter
                        encrypted_text = binary_to_text(binary_text[:-16])
                        decrypted_text = xor_encrypt_decrypt(encrypted_text, key)
                        if decrypted_text.startswith("--SECRET--"):
                            show_info_message("Decoded Message", decrypted_text[len("--SECRET--"):])
                        else:
                            show_error_message("Error", "Wrong secret key entered.")
                        return
        show_error_message("Error", "No hidden message found.")
    except Exception as e:
        show_error_message("Error", str(e))

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    return file_path

def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
    return file_path

def encode_action():
    image_path = select_image()
    if not image_path:
        return
    
    text_to_hide_dialog = CustomInputDialog(root, "Input", "Enter the text to hide:")
    text_to_hide = text_to_hide_dialog.show()
    if not text_to_hide:
        return
    
    secret_key_dialog = CustomInputDialog(root, "Input", "Enter the secret key:")
    secret_key = secret_key_dialog.show()
    if not secret_key:
        return
    
    output_path = save_image()
    if not output_path:
        return
    
    encode_text_to_image(image_path, text_to_hide, output_path, secret_key)

def decode_action():
    image_path = select_image()
    if not image_path:
        return
    
    secret_key_dialog = CustomInputDialog(root, "Input", "Enter the secret key:")
    secret_key = secret_key_dialog.show()
    if not secret_key:
        return
    
    decode_text_from_image(image_path, secret_key)

# Create the main window
root = tk.Tk()
root.title("Image Steganography")
root.geometry("600x200")
root.configure(bg="#f0f0f0")

# Create a frame for better organization
frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=20)

# Create buttons for encode and decode actions
encode_button = tk.Button(frame, text="Encode Text into Image", command=encode_action, width=25, height=2, bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"))
encode_button.grid(row=0, column=0, padx=10, pady=10)

decode_button = tk.Button(frame, text="Decode Text from Image", command=decode_action, width=25, height=2, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold"))
decode_button.grid(row=0, column=1, padx=10, pady=10)

# Run the application
root.mainloop()
