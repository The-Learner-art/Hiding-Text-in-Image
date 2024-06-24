# Image Steganography Application

## Overview

This application allows users to hide text within images (encoding) and retrieve hidden text from images (decoding). It utilizes simple XOR encryption to protect the hidden text, ensuring that only those with the correct secret key can access the encoded message.

## Features

- **Encode Text into Image**: Hide text within an image using XOR encryption and store the result in a new image file.
- **Decode Text from Image**: Retrieve and decrypt hidden text from an image file.

## Dependencies

The application requires the following Python libraries:

- `tkinter`: For the graphical user interface (GUI).
- `PIL` (Pillow): For image processing.
- `numpy`: For handling image data in array form.

## Installation

To install the required dependencies, run:

```bash
pip install tkinter pillow numpy
```

## Usage

### Running the Application

To run the application, execute the script in a Python environment:

```bash
python steganography_app.py
```

### Encoding Text into an Image

1. Click the "Encode Text into Image" button.
2. Select the image file where you want to hide the text.
3. Enter the text you want to hide.
4. Enter the secret key for encryption.
5. Choose the location to save the encoded image.

### Decoding Text from an Image

1. Click the "Decode Text from Image" button.
2. Select the image file that contains the hidden text.
3. Enter the secret key used during the encoding process.
4. The decoded message will be displayed if the correct key is entered.

## GUI Components

### Custom Input Dialog

A custom dialog box for user input, which prompts the user to enter text or a secret key.

### Custom Message Dialog

A custom dialog box for displaying messages to the user, such as success or error messages.

## Error Handling

- Displays an error message if no hidden message is found in the selected image.
- Displays an error message if the wrong secret key is entered during the decoding process.
- Handles general exceptions and displays relevant error messages to the user.

## How It Works

### Encoding Process

1. The user selects an image and enters the text and secret key.
2. The text is prefixed with a signature (`--SECRET--`) and encrypted using XOR encryption.
3. The encrypted text is converted to binary and appended with a delimiter (`1111111111111110`).
4. The binary text is embedded into the least significant bits of the image pixels.
5. The modified image is saved to the specified location.

### Decoding Process

1. The user selects an image and enters the secret key.
2. The application extracts the binary data from the least significant bits of the image pixels until the delimiter is encountered.
3. The binary data is converted back to text and decrypted using the XOR encryption with the provided key.
4. If the decrypted text contains the signature (`--SECRET--`), the hidden message is displayed. Otherwise, an error message is shown.

## Code Structure

- `text_to_binary(text)`: Converts text to a binary string.
- `binary_to_text(binary)`: Converts a binary string to text.
- `xor_encrypt_decrypt(text, key)`: Encrypts or decrypts text using XOR encryption with the provided key.
- `CustomInputDialog`: Custom dialog class for text input.
- `CustomMessageDialog`: Custom dialog class for displaying messages.
- `show_info_message(title, message)`: Shows an informational message.
- `show_error_message(title, message)`: Shows an error message.
- `encode_text_to_image(image_path, text, output_path, key)`: Encodes text into an image.
- `decode_text_from_image(image_path, key)`: Decodes text from an image.
- `select_image()`: Opens a file dialog to select an image file.
- `save_image()`: Opens a file dialog to save an image file.
- `encode_action()`: Handles the encoding process.
- `decode_action()`: Handles the decoding process.

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following libraries:

- [Pillow](https://python-pillow.org/)
- [NumPy](https://numpy.org/)

## Contact

For any questions or issues, please contact [Chiranjeevi Thota] at [thotachiranjeevi358@gmail.com].
