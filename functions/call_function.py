from google.genai import types


from functions.run_python import run_python_file
from functions.get_file_content import get_file_content
from functions.get_files_info import get_files_info
from functions.write_file_content import write_file


def call_function(function_call_part, verbose=False):

    functions_by_name = {"get_file_content": get_file_content, "get_files_info": get_files_info, "write_file": write_file, "run_python_file": run_python_file}
    func = functions_by_name.get(function_call_part.name)

    if not func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_call_part.name,
                    response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )

    merged_args = dict(function_call_part.args)
    merged_args["working_directory"] = "./calculator"

    result = func(**merged_args)
   
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({merged_args})")
    else:
        print(f" - Calling function: {function_call_part.name}")


    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": result},
            )
        ],
    )
