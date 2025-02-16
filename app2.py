import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image
import PyPDF2
import nltk
from transformers import pipeline

# Load environment variables from .env file
load_dotenv()

# Download necessary nltk resources
nltk.download('punkt')

# Load pre-trained question-answering model
qa_pipeline = pipeline("question-answering")

# Function to extract text from PDF


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n'
    return text

# Function to retrieve answer using the QA model


def retrieve_answer_from_pdf(question, text):
    result = qa_pipeline(question=question, context=text)
    return result['answer']


def app():
    st.set_page_config(layout="wide")

    # Load image from file
    img = Image.open("weebsu.png")
    img = img.resize((150, 150))
    st.image(img)

    st.title("🗿 Admin Pondok")
    st.caption("Saya Adalah Admin")

    # Extract text from PDF
    pdf_text = extract_text_from_pdf("pppm.pdf")

    if 'messages' not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "halo saya adalah admin pondok"}]

    # Display chat history
    for msg in st.session_state.messages:
        st.chat_message("🗿" if msg["role"] ==
                        "assistant" else "🙂").write(msg["content"])

    # Handle user input
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("🙂").write(prompt)

        # Retrieve response based on input
        response = retrieve_answer_from_pdf(prompt, pdf_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": response})
        st.chat_message("🗿").write(response)

    # Button to copy conversation text
    if st.button("Salin Teks"):
        conversation_text = "\n".join(
            f"🙂: {msg['content']}" if msg["role"] == "user" else f"🗿: {msg['content']}"
            for msg in st.session_state.messages
        )

        # JavaScript for copying text to clipboard
        st.components.v1.html(f"""
        <textarea id="conversation-text" style="display:none;">{conversation_text}</textarea>
        <button onclick="copyToClipboard()">Salin Teks</button>
        <script>
        function copyToClipboard() {{
            var copyText = document.getElementById("conversation-text");
            copyText.style.display = "block";
            copyText.select();
            document.execCommand("copy");
            copyText.style.display = "none";
            alert("Percakapan telah disalin sebagai teks!");
        }}
        </script>
        """)


if __name__ == "__main__":
    app()
