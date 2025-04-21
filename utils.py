import numpy as np
import cv2

def dct2(a):
    return cv2.dct(np.float32(a))

def idct2(a):
    return cv2.idct(a)

def embed_message(image, message):
    message += chr(0)  
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(binary_message)

    img_copy = image.copy()
    img_ycrcb = cv2.cvtColor(img_copy, cv2.COLOR_BGR2YCrCb)
    y, cr, cb = cv2.split(img_ycrcb)

    rows, cols = y.shape
    rows = (rows // 8) * 8 
    cols = (cols // 8) * 8
    
    max_bits = (rows // 8) * (cols // 8)
    if message_length > max_bits:
        raise ValueError(f"Pesan terlalu panjang. Max: {max_bits//8} karakter, Pesan: {message_length//8} karakter")

    bit_idx = 0
    THRESHOLD = 50.0 
    
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            if bit_idx >= message_length:
                break
                
            block = y[i:i+8, j:j+8].astype(np.float32)
            
            dct_block = dct2(block)
            
            coeff = dct_block[4, 4]
            
            bit = int(binary_message[bit_idx])
            
            if bit == 1:
                if coeff <= THRESHOLD:
                    coeff = THRESHOLD + 10
            else:
                if coeff >= -THRESHOLD:
                    coeff = -THRESHOLD - 10
                    
            dct_block[4, 4] = coeff
            
            idct_block = idct2(dct_block)
            y[i:i+8, j:j+8] = np.clip(idct_block, 0, 255).astype(np.uint8)
            
            bit_idx += 1

    img_result = cv2.merge([y, cr, cb])
    img_result = cv2.cvtColor(img_result, cv2.COLOR_YCrCb2BGR)
    
    return img_result

def extract_message(image):
    img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCrCb)
    y, _, _ = cv2.split(img_ycrcb)

    rows, cols = y.shape
    rows = (rows // 8) * 8
    cols = (cols // 8) * 8

    bits = []
    found_terminator = False
    
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            if found_terminator:
                break
                
            block = y[i:i+8, j:j+8].astype(np.float32)
            
            dct_block = dct2(block)
            
            coeff = dct_block[4, 4]
            
            bit = 1 if coeff > 0 else 0
            bits.append(str(bit))
            
            if len(bits) % 8 == 0:
                current_byte = bits[-8:]
                char_code = int(''.join(current_byte), 2)
                if char_code == 0:
                    bits = bits[:-8]
                    found_terminator = True
    
    message = ""
    for i in range(0, len(bits), 8):
        if i + 8 <= len(bits):
            byte = bits[i:i+8]
            char = chr(int(''.join(byte), 2))
            message += char
    
    return message if message else "Tidak ditemukan pesan tersembunyi."

