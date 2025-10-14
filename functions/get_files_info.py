import os

def get_files_info(working_directory, directory="."):
    abs_work = os.path.abspath(working_directory)
    full_path = os.path.abspath(os.path.join(abs_work, directory))
    if not full_path.startswith(abs_work):
        return(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(full_path):
        return(f'Error: "{directory}" is not a directory')
    try:
        return_string = []
        list_of_files = os.listdir(full_path)
        for file in list_of_files:
            is_dir = False
            if not os.path.isfile(os.path.join(full_path, file)):
                is_dir = True
            return_string.append(f'-{file}: file_size={os.path.getsize(full_path)} bytes, is_dir={is_dir}\n')

        return("".join(return_string))
    except Exception as e:
        return f"Error listing files: {e}"

