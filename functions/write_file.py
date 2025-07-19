import os

def write_file(working_directory, file_path, content):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)

    if not abs_full_path.startswith(abs_path):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    if not os.path.exists(abs_full_path):
        # Get just the directory part (without the filename)
        directory_path = os.path.dirname(abs_full_path)
        # Create the directory structure if it doesn't exist
        try:
            os.makedirs(directory_path, exist_ok=True)
        except Exception as e:
            return f"Error: {e}"

    with open(abs_full_path, "w") as f:
        f.write(content)
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'