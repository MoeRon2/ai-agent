import os
from google.genai import types
from config import MAX_CHARS

def get_files_info(working_directory, directory=None):
    full_path = os.path.join(working_directory, directory)
    abs_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    if not abs_full_path.startswith(abs_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    elif not os.path.isdir(abs_full_path):
        return f'Error: "{directory}" is not a directory'
    
    try:
        path_contents = os.listdir(abs_full_path)
        line = []
        for content in path_contents:
                path_for_content = os.path.join(abs_full_path, content )
                line.append(f" - {content}: file_size={os.path.getsize(path_for_content)} bytes, is_dir={os.path.isdir(path_for_content)}")
    except Exception as e:
         return f"Error: {e}"
        

    return "\n".join(line)



schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

