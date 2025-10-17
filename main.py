import os
import sys
from dotenv import load_dotenv
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python import schema_run_python_file
from functions.write_file_content import schema_write_file
from functions.call_function import call_function


load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)



def main():
    system_prompt = """
    You are a helpful AI coding agent.
    
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    args = sys.argv[1:]
    verbose = False
    prompt_parts = []

    if not args:
        print("This is the secret agent")
        print('\nUsage: python main.py "Your prompt here" [--verbose]')
        print("\nExample: pyhton main.py 'What is the capital of Liechtenstein?'")
        sys.exit(1)
    
    if '--verbose' in args:
        verbose = True

    if verbose:
        for arg in args:
            if arg != "--verbose":
                prompt_parts.append(arg)
        user_prompt = " ".join(prompt_parts)
    else:
        user_prompt = " ".join(args)


    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )
       
    count = 0

    while count < 20:
        
        try:
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                )
            )
        except Exception as e:
            print(f"Error: {e}")
            break

     
        for candidate in response.candidates:
            messages.append(candidate.content)

        prompt_tokens = response.usage_metadata.prompt_token_count
        response_tokens = response.usage_metadata.candidates_token_count
        function_responses = []

        if not response.function_calls:
            print(response.text)
            break

        for call in response.function_calls:
            function_call_result = call_function(call, verbose)
            if not function_call_result.parts[0].function_response.response:
                raise ValueError(
                    f"Malformed function response for '{call.name}': missing parts[0].function_response.response"
                )
            if verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            function_responses.append(function_call_result.parts[0])
            if not function_responses:
                raise Exception("no function responses generated, exiting.")
        messages.append(types.Content(role="user", parts=function_responses))
        count += 1
    
    if count == 20:
        print("Maximum iterations reached. Terminating agent.")
    
    if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {prompt_tokens}")
                print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
