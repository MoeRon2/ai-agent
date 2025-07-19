import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content

from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file





available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ]
)


system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""


callable_functions = {
    'get_files_info': get_files_info,
    'get_file_content': get_file_content,
    'write_file': write_file,
    'run_python_file': run_python_file
}



def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name

    function_args = dict(function_call_part.args)
    
    function_args["working_directory"] = "./calculator"
    if verbose:
        print(f"Calling function: {function_name}({function_args})")
    else:
        print(f" - Calling function: {function_name}")
    
    try:
        function_result = callable_functions[function_name](**(function_args))
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )
    ],
)
    except KeyError:
        return types.Content(
    role="tool",
    parts=[
        types.Part.from_function_response(
            name=function_name,
            response={"error": f"Unknown function: {function_name}"},
        )
    ],

    
)
    
    

def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    return client



def main():
    # Get prompt and check for correct usage
    verbose_flag = "--verbose" in sys.argv
    args = []
    for arg in sys.argv[1:]:
        if not arg.startswith("--"):
            args.append(arg)

    if not args:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I fix the calculator?"')
        sys.exit(1)

     
    if args:
        user_prompt = " ".join(args)


    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    print("Hello from ai-agent!")
    # Juicy part
    client = create_client()
    response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=messages,
    config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
    )
    for candidate in response.candidates:
        messages.append(candidate.content)
    
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    # Output handling
    if not response.function_calls:
        return response.text

    for function_call_part in response.function_calls:
        result = call_function(function_call_part, verbose=verbose_flag)
        if not result.parts[0].function_response.response:
            raise Exception("No response found")
        messages.append(result)
        if verbose_flag:
            print(f"-> {result.parts[0].function_response.response['result']}")
        else:
             print(result.parts[0].function_response.response["result"])

            

    if verbose_flag:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")



if __name__ == "__main__":
    main()