import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info



available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client



def main():
    # Get prompt and check for correct usage
    if not (len(sys.argv) == 2 or (len(sys.argv) == 3 and sys.argv[2] == "--verbose")):
        print("Usage: uv run main.py [PROMPT]")
        sys.exit(1)
    
    content = sys.argv[1]
    verbose_flag = None

    if (len(sys.argv) == 3):
        verbose_flag = sys.argv[2]

    messages = [
    types.Content(role="user", parts=[types.Part(text=content)]),
]


    print("Hello from ai-agent!")
    # Juicy part
    client = create_client()
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )

    
    
    response_text = response.text
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    # Output handling
    print(f"Response: {response_text}")
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    if (verbose_flag):
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")



if __name__ == "__main__":
    main()