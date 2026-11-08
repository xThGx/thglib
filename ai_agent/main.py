import os
from dotenv import load_dotenv
import argparse


def main():
    print("Hello from ai-agent!")
    
    load_dotenv()

    # Get the API key from environment variables
    api_key = os.environ.get("OPENROUTER_API_KEY")

    # Check if the API key is present
    if not api_key:
        raise Exception("API KEY not found!")

    from openai import OpenAI

    # Set up argument parser to accept user prompt from command line
    parser = argparse.ArgumentParser(description="AI-Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Initialize the OpenAI client with the API key
    client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            )

    # Make a request to the OpenRouter API with the user prompt
    messages = [
        {
            "role": "user",
            "content": args.user_prompt,
        }
    ]
    response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages
            )

    # Check if the response is valid
    if not response:
        raise RuntimeError("No response from the API.")

    if args.verbose:
        print("User prompt:", args.user_prompt)
        print("Prompt tokens:", response.usage.prompt_tokens)
        print("Response tokens:", response.usage.completion_tokens)
    print(response.choices[0].message.content)


if __name__ == "__main__":
    main()
