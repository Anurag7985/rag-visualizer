def save_file(file_path, uploaded_file):
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())