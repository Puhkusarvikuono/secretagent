import os

def write_file(working_directory, file_path, content):
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_work, file_path))
    file_name = os.path.split(abs_file)[1]
    file_dir = os.path.split(abs_file)[0]
    if not abs_file.startswith(abs_work):
        return(f'Error: Cannot write "{file_path}" as it is outside the permitted working directory')
    if not os.path.exists(abs_file):
        try:
            os.makedirs(os.path.dirname(file_dir), exist_ok=True)
        except Exception as e:
            return f"Error creating files: {e}"
    try:
        with open(file_name, "w") as f:
            f.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
    except Exception as e:
        return f"Error creating files: {e}"

