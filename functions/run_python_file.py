import os
import subprocess


def run_python_file(working_directory, file_path, args=[]):
    full_path = os.path.join(working_directory, file_path)
    abs_path = os.path.abspath(working_directory)
    abs_full_path = os.path.abspath(full_path)
    if not abs_full_path.startswith(abs_path):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(abs_full_path):
        return f'Error: File "{file_path}" not found.'
    if not abs_full_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        completed_process = subprocess.run(["python", abs_full_path] + args, capture_output=True, timeout=30, text=True, cwd=abs_path)
    except Exception as e:
        return f"Error: executing Python file: {e}"

    output = f"STDOUT:\n {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

    if not completed_process.stderr and not completed_process.stdout:
        return "No output produced."
    if completed_process.returncode != 0:
        output += f"\nProcess exited with code {completed_process.returncode}"
    
    return output