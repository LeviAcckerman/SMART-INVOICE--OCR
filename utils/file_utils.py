import os
from datetime import datetime

def save_uploaded_file(uploaded_file, upload_dir="uploads"):
    """
    Save the uploaded file to the specified directory.
    Returns the full path to the saved file.
    """
    # Ensure the upload directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Generate a unique file name using timestamp to avoid overwrite
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{uploaded_file.name}"
    file_path = os.path.join(upload_dir, filename)

    # Write the file to disk
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path
