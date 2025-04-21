# DCT Steganography Web App

This is a simple web application built using Streamlit that allows users to hide messages within images using the Discrete Cosine Transform (DCT). It supports both encoding (embedding a message into an image) and decoding (extracting the hidden message from an image).

## Features

- **Encode Message**: Upload an image and input a message to hide. The message will be embedded in the image using DCT.
- **Decode Message**: Upload an encoded image to extract the hidden message.

## Installation

1. Clone the repository or download the files.
2. Run the following commands:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Usage

1. Run the application using `streamlit run app.py`.
2. Select the "Encode Message" option to hide a message in an image.
3. Upload an image and input the message to hide.
4. Click the "Encode" button to embed the message in the image.
5. Select the "Decode Message" option to extract a hidden message from an image.
6. Upload the encoded image.
7. Click the "Decode" button to extract the hidden message.

## Code Structure

The code is structured into the following sections:

- `app.py`: The main application file that contains the Streamlit app.
- `utils.py`: A module that contains the DCT steganography functions.
- `requirements.txt`: A file that lists the required dependencies.

## Future Improvements

- Improve the security of the application by adding authentication and authorization.
- Add support for more image formats.
- Improve the performance of the application by optimizing the DCT steganography functions.