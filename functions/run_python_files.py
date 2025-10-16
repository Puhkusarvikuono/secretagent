import subprocess
import os

def run_python_file(working_directory, file_path, args=[]):
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_work, file_path))
    if not abs_file.startswith(abs_work):
        return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_file):
        return(f'Error: File "{file_path}" not found.')
    if not abs_file.endswith('.py'):
        return(f'Error: "{file_path}" is not a Python file.')
    try:
        process = subprocess.run(["python3"] + [file_path] + args, cwd=working_directory, timeout=30, capture_output=True, text=True)
        if process.stdout == "" and process.stderr == "":
            return("No output produced")
        returnstring = (f'STDOUT: {process.stdout}, \nSTDERR: {process.stderr}')
        if process.returncode != 0:
            returnstring += (f'\nProcess exited with code {process.returncode}')
        return returnstring
    except Exception as e:
        return(f"Error: executing Python file: {e}")
    


