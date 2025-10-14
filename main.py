import os
import sys
from dotenv import load_dotenv
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

from google import genai

client = genai.Client(api_key=api_key)



def main():
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

    response = client.models.generate_content(
        model='gemini-2.0-flash-001',
        contents=messages,
    )

    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count
    print(response.text)
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

if __name__ == "__main__":
    main()
