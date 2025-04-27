import streamlit as st
import requests
import os
import pathlib

BACKEND_URL = "http://localhost:8000"

st.title("AI-Powered Query System")

# Section for clearing memory
st.header("Clear Stored Data")
if st.button("Clear Memory"):
    response = requests.post(f"{BACKEND_URL}/clear")
    if response.status_code == 200:
        st.success("Stored data cleared successfully")
    else:
        st.error(f"Error clearing data: {response.text}")

# Section for inserting sources
st.header("Insert Sources")

# Input for URL
url_input = st.text_input("Enter a URL (e.g., https://example.com)")
if url_input:
    st.write("URL entered:", url_input)

# Input for Image
image_file = st.file_uploader("Upload an Image (JPG, PNG)", type=["jpg", "png"])
if image_file:
    st.image(image_file, caption="Uploaded Image", use_column_width=True)

# Input for PDF
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])
if pdf_file:
    st.write("PDF uploaded:", pdf_file.name)

# Button to insert sources
if st.button("Insert Sources"):
    sources = []
    
    # Use absolute path for the temp directory at project root
    temp_dir = pathlib.Path("temp").absolute()
    os.makedirs(temp_dir, exist_ok=True)
    
    # Add URL source if provided
    if url_input:
        sources.append({"type": "url", "value": url_input})
    
    # Add Image source if provided
    if image_file:
        image_path = temp_dir / image_file.name
        with open(image_path, "wb") as f:
            f.write(image_file.getbuffer())
        st.write(f"Image saved to: {image_path}")
        sources.append({"type": "image", "value": str(image_path)})
    
    # Add PDF source if provided
    if pdf_file:
        pdf_path = temp_dir / pdf_file.name
        with open(pdf_path, "wb") as f:
            f.write(pdf_file.getbuffer())
        st.write(f"PDF saved to: {pdf_path}")
        sources.append({"type": "pdf", "value": str(pdf_path)})
    
    # Send sources to the backend
    if sources:
        response = requests.post(f"{BACKEND_URL}/insert", json={"sources": sources})
        if response.status_code == 200:
            st.success("Sources inserted successfully")
            # Clean up files immediately after the request, as in the working version
            if image_file and os.path.exists(image_path):
                os.remove(image_path)
                st.write(f"Cleaned up image file: {image_path}")
            if pdf_file and os.path.exists(pdf_path):
                os.remove(pdf_path)
                st.write(f"Cleaned up PDF file: {pdf_path}")
        else:
            st.error(f"Error inserting sources: {response.text}")
            st.write("Files not cleaned up due to error. Check the following paths:")
            if image_file:
                st.write(image_path)
            if pdf_file:
                st.write(pdf_path)
    else:
        st.warning("No sources to insert")

# Section for querying
st.header("Query System")
question = st.text_input("Enter your question")
if st.button("Get Answer"):
    if question:
        response = requests.post(f"{BACKEND_URL}/query", json={"question": question})
        if response.status_code == 200:
            data = response.json()
            st.write("**Answer:**")
            st.write(data["answer"])
            st.write("**Sources:**")
            for source in data["sources"]:
                st.write(source)
        else:
            st.error(f"Error getting answer: {response.text}")
    else:
        st.warning("Please enter a question")