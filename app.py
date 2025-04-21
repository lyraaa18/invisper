import streamlit as st
import numpy as np
import cv2
from PIL import Image
import io

from utils import embed_message, extract_message

def main():
    st.set_page_config(page_title="Invisper", page_icon="🔐", layout="wide")
    
    st.markdown("""
    <style>
        # .centered-title {
        #     text-align: center;
        # }
        # .stButton>button {
        #     width: fit-content;
        #     background-color: #ff4b4b;
        #     color: white;
        #     padding: 0.5rem 1.5rem;
        #     border-radius: 8px;
        #     font-weight: 600;
        #     border: none;
        # }
        # .stDownloadButton>button {
        #     width: fit-content;
        #     background-color: #ff4b4b;
        #     color: white;
        #     padding: 0.5rem 1.5rem;
        #     border-radius: 8px;
        #     font-weight: 600;
        #     border: none;
        # }
        .centered-title {
            text-align: center;
        }
        .stTabs [data-baseweb="tab"] {
            font-weight: bold;
            font-size: 16px;
            color: #444;
        }
        .stTabs [aria-selected="true"] {
            border-bottom: 3px solid #ff4b4b;
            color: #ff4b4b;
        }
        section.main > div {
            padding-top: 1rem;
        }
        .stFileUploader {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 10px;
        }
        .stFileUploader .css-1cpxqw2 {
            max-width: 180px;
            height : 120
        }
        .stTextArea textarea {
            background-color: #f6f6f6;
            font-size: 14px;
        }
        .stButton>button, .stDownloadButton>button {
            width: fit-content;
            background-color: #ff4b4b;
            color: white !important;
            padding: 0.5rem 1.5rem;
            border-radius: 8px;
            font-weight: 600;
            border: none;
            transition: 0.2s ease-in-out;
        }

        .stButton>button:hover, .stDownloadButton>button:hover {
            background-color: #ff6b6b;
            color: white !important;
        }

    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("<h1 class='centered-title'>Invisper</h1>", unsafe_allow_html=True)
    st.markdown("<h4 class='centered-title'>Hide secret messages inside images using DCT Steganography</h4>", unsafe_allow_html=True)
    
    tabs = st.tabs(["Encode message", "Decode message", "About"])
    encode_btn = False
    with tabs[0]:
        # st.subheader("Step 1: Upload Image & Input Message")
        
        col1, col2 = st.columns([1.5, 2])
        with col1:
            uploaded_file = st.file_uploader("Upload image (PNG/JPG/BMP)", type=["png", "jpg", "jpeg", "bmp"])
        with col2:
            message = st.text_area("Enter your secret message:", height=160, placeholder="e.g. The treasure is buried under the tree.")
        colA, colB = st.columns([2, 2])
        with colA:
            if uploaded_file:
                image_pil = Image.open(uploaded_file).convert("RGB")
                image_np = np.array(image_pil)
                image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
                st.image(image_pil, caption="Original Image Preview", use_container_width=True)
                
                h, w = image_np.shape[:2]
                max_bits = (h // 8) * (w // 8)
                max_chars = max_bits // 8
                st.info(f"🖼️ Image Size: {w}x{h} px | Max message size ~ {max_chars} characters")
                col_enc1, col_enc2 = st.columns([1, 4])
                with col_enc1:
                    encode_btn = st.button("Encode")
        with colB:
            # col_enc1, col_enc2 = st.columns([1, 4])
            # with col_enc1:
            #     encode_btn = st.button("Encode")
            
            if encode_btn:
                if not uploaded_file or not message.strip():
                    st.warning("Please upload an image and enter a message.")
                else:
                    with st.spinner("Encoding message..."):
                        try:
                            encoded_img = embed_message(image_bgr, message)
                            encoded_rgb = cv2.cvtColor(encoded_img, cv2.COLOR_BGR2RGB)
                            
                            st.image(encoded_rgb, caption="Encoded Image", use_container_width=True)
                            st.success("✅ Message successfully embedded!")

                            # colA, colB = st.columns([2])
                            # with colA:
                            #     st.image(image_pil, caption="Original Image", use_container_width=True)

                            # with colB:
                            #     st.image(encoded_rgb, caption="Encoded Image", use_container_width=True)
                            _, buffer = cv2.imencode('.png', encoded_img)
                            st.session_state['last_encoded'] = buffer.tobytes()
                            
                            st.download_button("Download Encoded Image", buffer.tobytes(), "encoded.png", "image/png")
                        except Exception as e:
                            st.error(f"❌ Error: {str(e)}")

    with tabs[1]:
        # st.subheader("Step 1: Select Encoded Image")
        
        use_last = 'last_encoded' in st.session_state and st.checkbox("Use previously encoded image", value=True)

        if use_last:
            st.image(cv2.cvtColor(cv2.imdecode(np.frombuffer(st.session_state['last_encoded'], np.uint8), 1), cv2.COLOR_BGR2RGB),
                     caption="Recent Encoded Image", width=300)
            
            if st.button("Decode", key="decode_last"):
                with st.spinner("Decoding..."):
                    try:
                        img = cv2.imdecode(np.frombuffer(st.session_state['last_encoded'], np.uint8), cv2.IMREAD_COLOR)
                        message = extract_message(img)
                        if message and message != "Tidak ditemukan pesan tersembunyi.":
                            st.success("✅ Message extracted:")
                            st.text_area("Hidden Message", value=message, height=150, disabled=True)
                        else:
                            st.warning("No hidden message found.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
        
        st.markdown("Or upload a different image:")
        uploaded_decode = st.file_uploader("Upload encoded image", type=["png", "jpg", "jpeg", "bmp"], key="decode_image")
        
        if uploaded_decode:
            decode_pil = Image.open(uploaded_decode).convert("RGB")
            decode_np = np.array(decode_pil)
            decode_bgr = cv2.cvtColor(decode_np, cv2.COLOR_RGB2BGR)
            st.image(decode_pil, caption="Uploaded Image", width=360)

            if st.button("Decode", key="decode_uploaded"):
                with st.spinner("Decoding..."):
                    try:
                        message = extract_message(decode_bgr)
                        if message and message != "Tidak ditemukan pesan tersembunyi.":
                            st.success("✅ Message extracted:")
                            st.text_area("Hidden Message", value=message, height=150, disabled=True)
                        else:
                            st.warning("No hidden message found.")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    
    with tabs[2]:
        st.subheader("📘 About Whispr")
        st.markdown("""
        **Whispr** is a simple tool to embed and extract secret messages in images using the **Discrete Cosine Transform (DCT)** method.

        ---
        ### 🔍 Why DCT?
        - **Less noticeable** changes to human eyes
        - **Robust** to image editing (e.g. resizing, compression)
        - **Difficult to detect** via visual inspection

        ---
        ### 🔐 To Hide a Message:
        1. Upload a cover image (PNG recommended)
        2. Type your secret message
        3. Click **Encode**
        4. Download the encoded image

        ### 🔓 To Extract a Message:
        1. Upload the encoded image
        2. Click **Decode**
        3. View the hidden message

        > ⚠️ Steganography hides, but doesn’t encrypt — for sensitive content, combine with encryption.
        """)
        
if __name__ == "__main__":
    main()
