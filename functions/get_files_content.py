import os

def get_file_content(working_directory, file_path):
    abs_work = os.path.abspath(working_directory)
    abs_file = os.path.abspath(os.path.join(abs_work, file_path))
    if not abs_file.startswith(abs_work):
        return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
    if not os.path.isfile(abs_file):
        return(f'Error: File not found or is not a regular file: "{file_path}')

    try:
        MAX_CHARS = 10000
        with open(abs_file, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_file) > MAX_CHARS:
                file_content_string = file_content_string + f'[...File "{file_path}" truncated at {MAX_CHARS} characters].'
            return file_content_string

    except Exception as e:
        return f"Error reading file: {e}"

