import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
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

    client = create_client()
    response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages)

    
    
    response_text = response.text
    prompt_tokens = response.usage_metadata.prompt_token_count
    response_tokens = response.usage_metadata.candidates_token_count


    # Output handling
    print(f"Response: {response_text}")
    if (verbose_flag):
        print(f"User prompt: {content}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")



if __name__ == "__main__":
    main()